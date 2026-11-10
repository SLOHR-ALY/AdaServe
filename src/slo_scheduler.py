def select_tokens(requests, verification_budget):

    # Sort requests by their SLO priority
    # Lower latency target = higher priority

    sorted_requests = sorted(
        requests,
        key=lambda x: x["priority"]
    )

    selected = []
    remaining_budget = verification_budget

    for request in sorted_requests:

        tokens_needed = request["tokens_needed"]

        if remaining_budget <= 0:
            break

        allocated = min(
            tokens_needed,
            remaining_budget
        )

        selected.append({
            "request": request["name"],
            "priority": request["priority"],
            "allocated_tokens": allocated
        })

        remaining_budget -= allocated

    return selected, remaining_budget
