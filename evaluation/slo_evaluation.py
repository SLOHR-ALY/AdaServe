def evaluate_requests(requests):

    total_requests = len(requests)
    successful = 0
    successful_tokens = 0
    total_tokens = 0
    total_time = 0
    total_token_latency = 0

    for r in requests:

        token_latency_ms = (
            r["latency"] / r["tokens"]
        ) * 1000

        slo_met = token_latency_ms <= r["slo_ms"]

        if slo_met:
            successful += 1
            successful_tokens += r["tokens"]

        total_tokens += r["tokens"]
        total_time += r["latency"]
        total_token_latency += r["latency"]

    attainment = successful / total_requests * 100
    violation = 100 - attainment

    throughput = total_tokens / total_time
    goodput = successful_tokens / total_time
    avg_token_latency = (
        total_token_latency / total_tokens
    ) * 1000

    return {
        "SLO Attainment (%)": attainment,
        "SLO Violation (%)": violation,
        "Goodput (tokens/sec)": goodput,
        "Average Token Latency (ms)": avg_token_latency,
        "Throughput (tokens/sec)": throughput
    }
