from __future__ import annotations

import argparse

from mersenne_twister import MersenneTwister, MersenneTwisterParams


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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create a Mersenne Twister and print random numbers."
    )
    parser.add_argument("--seed", type=int, default=5489)
    parser.add_argument("--count", type=int, default=5)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    generator = MersenneTwister(seed=args.seed, params=MT19937_PARAMS)
    for number in generator.rand(args.count):
        print(number)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
