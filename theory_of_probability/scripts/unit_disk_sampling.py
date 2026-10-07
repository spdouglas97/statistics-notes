from __future__ import annotations

import math
import time
from collections.abc import Callable

from mersenne_twister import MersenneTwister, MersenneTwisterParams


BENCHMARK_SAMPLE_COUNT = 200_000
BENCHMARK_REPEATS = 5
DEFAULT_SEED = 5489
MT19937_PARAMS = MersenneTwisterParams(
    w=32,
    n=624,
    m=397,
    r=31,
    a=0x9908B0DF,
    b=0x9D2C5680,
    c=0xEFC60000,
    f=1812433253,
    u=11,
    s=7,
    t=15,
    l=18,
)
MT19937_SCALE = float(1 << MT19937_PARAMS.w)


def _create_generator() -> MersenneTwister:
    return MersenneTwister(seed=DEFAULT_SEED, params=MT19937_PARAMS)


def _next_uniform(generator: MersenneTwister) -> float:
    return generator.temper() / MT19937_SCALE


def sample_unit_disk_rejection(n: int) -> list[tuple[float, float]]:
    if n < 0:
        raise ValueError("n must be non-negative")

    generator = _create_generator()
    samples: list[tuple[float, float]] = []
    while len(samples) < n:
        x = 2.0 * _next_uniform(generator) - 1.0
        y = 2.0 * _next_uniform(generator) - 1.0
        if x * x + y * y <= 1.0:
            samples.append((x, y))
    return samples


def sample_unit_disk_transform(n: int) -> list[tuple[float, float]]:
    if n < 0:
        raise ValueError("n must be non-negative")

    generator = _create_generator()
    samples: list[tuple[float, float]] = []
    for _ in range(n):
        radius = math.sqrt(_next_uniform(generator))
        theta = 2.0 * math.pi * _next_uniform(generator)
        x = radius * math.cos(theta)
        y = radius * math.sin(theta)
        samples.append((x, y))
    return samples


def benchmark_sampler(
    sampler: Callable[[int], list[tuple[float, float]]],
    sample_count: int,
    repeats: int,
) -> tuple[int, float, float]:
    if repeats <= 0:
        raise ValueError("repeats must be positive")

    sampler(min(sample_count, 1_000))

    elapsed_times: list[float] = []
    sample_total = 0
    for _ in range(repeats):
        start = time.perf_counter()
        samples = sampler(sample_count)
        elapsed_times.append(time.perf_counter() - start)
        sample_total = len(samples)

    average_elapsed = sum(elapsed_times) / repeats
    best_elapsed = min(elapsed_times)
    return sample_total, average_elapsed, best_elapsed


def main() -> int:
    sample_count = BENCHMARK_SAMPLE_COUNT
    repeats = BENCHMARK_REPEATS

    rejection_count, rejection_average, rejection_best = benchmark_sampler(
        sample_unit_disk_rejection,
        sample_count,
        repeats,
    )
    transform_count, transform_average, transform_best = benchmark_sampler(
        sample_unit_disk_transform,
        sample_count,
        repeats,
    )

    print(f"Benchmarking {sample_count} samples per run over {repeats} runs.")
    print(
        f"Rejection sampling produced {rejection_count} samples per run "
        f"with average time {rejection_average:.6f} seconds "
        f"(best {rejection_best:.6f} seconds)."
    )
    print(
        f"Transform sampling produced {transform_count} samples per run "
        f"with average time {transform_average:.6f} seconds "
        f"(best {transform_best:.6f} seconds)."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
