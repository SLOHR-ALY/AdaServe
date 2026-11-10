import torch
import time

def speculative_decoding_v3(
    prompt,
    draft_model,
    target_model,
    tokenizer,
    speculation_depth=4,
    max_new_tokens=80
):
    messages = [{"role": "user", "content": prompt}]

    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )

    input_ids = tokenizer(
        text, return_tensors="pt"
    ).input_ids.to("cuda")

    generated = []
    proposed = 0
    accepted = 0
    rounds = 0

    eos = target_model.generation_config.eos_token_id
    if eos is None:
        eos = tokenizer.eos_token_id
    eos_ids = set(eos if isinstance(eos, list) else [eos])

    start = time.time()

    while len(generated) < max_new_tokens:
        rounds += 1
        prefix = input_ids
        draft_sequence = prefix
        candidates = []

        # 1. Draft candidate generation
        with torch.inference_mode():
            for _ in range(min(
                speculation_depth,
                max_new_tokens - len(generated)
            )):
                logits = draft_model(
                    input_ids=draft_sequence
                ).logits[:, -1, :]

                token = logits.argmax(dim=-1).item()
                candidates.append(token)

                draft_sequence = torch.cat([
                    draft_sequence,
                    torch.tensor([[token]], device="cuda")
                ], dim=1)

                if token in eos_ids:
                    break

            proposed += len(candidates)

            # 2. Target verifies candidate sequence
            candidate_tensor = torch.tensor(
                [candidates], device="cuda"
            )

            verify_ids = torch.cat(
                [prefix, candidate_tensor], dim=1
            )

            target_logits = target_model(
                input_ids=verify_ids
            ).logits

            prefix_len = prefix.shape[1]
            new_tokens = []
            all_accepted = True

            # 3. Compare each candidate with target prediction
            for j, candidate in enumerate(candidates):

                target_token = target_logits[
                    0, prefix_len - 1 + j, :
                ].argmax().item()

                if candidate == target_token:
                    new_tokens.append(candidate)
                    accepted += 1

                    if candidate in eos_ids:
                        break

                else:
                    all_accepted = False
                    new_tokens.append(target_token)
                    break

            # 4. Add bonus token only if ALL candidates match
            if (
                all_accepted
                and len(new_tokens) == len(candidates)
                and new_tokens
                and new_tokens[-1] not in eos_ids
                and len(generated) + len(new_tokens) < max_new_tokens
            ):
                bonus = target_logits[
                    0, prefix_len + len(candidates) - 1, :
                ].argmax().item()

                new_tokens.append(bonus)

            # Limit output to requested length
            remaining = max_new_tokens - len(generated)
            new_tokens = new_tokens[:remaining]

            if not new_tokens:
                break

            generated.extend(new_tokens)

            # 5. Update prefix
            input_ids = torch.cat([
                prefix,
                torch.tensor([new_tokens], device="cuda")
            ], dim=1)

            # Stop on EOS
            if new_tokens[-1] in eos_ids:
                break

    return {
        "token_ids": generated,
        "response": tokenizer.decode(
            generated, skip_special_tokens=True
        ),
        "accepted_tokens": accepted,
        "proposed_tokens": proposed,
        "acceptance_rate": accepted / proposed if proposed else 0,
        "rounds": rounds,
        "latency": time.time() - start
    }
