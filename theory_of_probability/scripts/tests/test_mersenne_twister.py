from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

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


class MersenneTwisterTests(unittest.TestCase):
    def test_temper_matches_mt19937_reference_output(self) -> None:
        generator = MersenneTwister(seed=5489, params=MT19937_PARAMS)

        numbers = [generator.temper() for _ in range(5)]

        self.assertEqual(
            numbers,
            [3499211612, 581869302, 3890346734, 3586334585, 545404204],
        )

    def test_rand_returns_requested_amount(self) -> None:
        generator = MersenneTwister(seed=5489, params=MT19937_PARAMS)

        numbers = generator.rand(3)

        self.assertEqual(len(numbers), 3)
        self.assertEqual(
            numbers,
            [0.8147236919030547, 0.13547700410708785, 0.9057919341139495],
        )

    def test_rand_outputs_stay_in_half_open_unit_interval(self) -> None:
        generator = MersenneTwister(seed=5489, params=MT19937_PARAMS)

        numbers = generator.rand(100)

        self.assertTrue(all(0.0 <= number < 1.0 for number in numbers))

    def test_rand_rejects_negative_n(self) -> None:
        generator = MersenneTwister(seed=1234, params=MT19937_PARAMS)

        with self.assertRaises(ValueError):
            generator.rand(-1)


if __name__ == "__main__":
    unittest.main()
