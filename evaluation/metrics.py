def evaluate_performance(requests):

    total = len(requests)

    successful = sum(
        1 for r in requests if r["slo_met"]
    )

    failed = total - successful

    slo_attainment = (successful / total) * 100
    violation_rate = (failed / total) * 100

    goodput = sum(
        r["tokens"] for r in requests if r["slo_met"]
    )

    total_tokens = sum(
        r["tokens"] for r in requests
    )

    total_time = sum(
        r["latency"] for r in requests
    )

    avg_latency = (
        total_time / total_tokens
        if total_tokens else 0
    )

    throughput = (
        total_tokens / total_time
        if total_time else 0
    )

    return {
        "SLO Attainment (%)": slo_attainment,
        "SLO Violation Rate (%)": violation_rate,
        "Goodput (tokens)": goodput,
        "Per-token Latency (seconds)": avg_latency,
        "Throughput (tokens/sec)": throughput
    }
