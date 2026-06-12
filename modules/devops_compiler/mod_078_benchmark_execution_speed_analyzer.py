import time
import timeit
from statistics import stdev


def benchmark_function(func, *args, iterations: int = 1000) -> dict:
    timings = []
    func_to_call = func

    for _ in range(iterations):
        start = time.perf_counter()
        func_to_call(*args)
        elapsed = time.perf_counter() - start
        timings.append(elapsed)

    avg = sum(timings) / len(timings)
    min_t = min(timings)
    max_t = max(timings)
    std = stdev(timings) if len(timings) > 1 else 0.0

    return {
        "function": func.__name__,
        "iterations": iterations,
        "avg_seconds": avg,
        "min_seconds": min_t,
        "max_seconds": max_t,
        "std_dev": std,
        "avg_ms": avg * 1000,
        "min_ms": min_t * 1000,
        "max_ms": max_t * 1000,
        "std_ms": std * 1000,
        "ops_per_second": 1.0 / avg if avg > 0 else float("inf"),
    }


def benchmark_string(code_string: str, setup: str = "", iterations: int = 1000) -> dict:
    t = timeit.Timer(stmt=code_string, setup=setup)
    timings = t.repeat(repeat=5, number=iterations)
    avg = sum(timings) / len(timings)
    min_t = min(timings)
    max_t = max(timings)
    std = stdev(timings) if len(timings) > 1 else 0.0

    return {
        "code": code_string[:50] + "...",
        "iterations": iterations,
        "avg_seconds": avg,
        "min_seconds": min_t,
        "max_seconds": max_t,
        "std_dev": std,
        "avg_ms": avg * 1000,
    }
