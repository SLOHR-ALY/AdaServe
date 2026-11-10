def optimize_throughput(requests, remaining_budget):

    allocations = []

    # Allocate remaining budget to requests
    # that can use additional verification tokens

    for request in requests:

        if remaining_budget <= 0:
            break

        additional_tokens = min(
            request["extra_capacity"],
            remaining_budget
        )

        if additional_tokens > 0:
            allocations.append({
                "request": request["name"],
                "additional_tokens": additional_tokens
            })

            remaining_budget -= additional_tokens

    return allocations, remaining_budget
