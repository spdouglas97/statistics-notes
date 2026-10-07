from __future__ import annotations

import io
import sys
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from unit_disk_sampling import (
    benchmark_sampler,
    main,
    sample_unit_disk_rejection,
    sample_unit_disk_transform,
)


class UnitDiskSamplingTests(unittest.TestCase):
    def test_rejection_sampling_returns_requested_points_in_disk(self) -> None:
        mock_generator = unittest.mock.Mock()
        scale = float(1 << 32)
        mock_generator.temper.side_effect = [
            int(1.0 * scale),
            int(1.0 * scale),
            int(0.75 * scale),
            int(0.75 * scale),
            int(0.375 * scale),
            int(0.625 * scale),
        ]

        with patch("unit_disk_sampling._create_generator", return_value=mock_generator):
            samples = sample_unit_disk_rejection(2)

        self.assertEqual(samples, [(0.5, 0.5), (-0.25, 0.25)])
        self.assertTrue(all(x * x + y * y <= 1.0 for x, y in samples))

    def test_transform_sampling_matches_expected_points(self) -> None:
        mock_generator = unittest.mock.Mock()
        scale = float(1 << 32)
        mock_generator.temper.side_effect = [
            int(0.25 * scale),
            int(0.0 * scale),
            int(1.0 * scale),
            int(0.25 * scale),
        ]

        with patch("unit_disk_sampling._create_generator", return_value=mock_generator):
            samples = sample_unit_disk_transform(2)

        self.assertEqual(len(samples), 2)
        self.assertAlmostEqual(samples[0][0], 0.5)
        self.assertAlmostEqual(samples[0][1], 0.0)
        self.assertAlmostEqual(samples[1][0], 0.0, places=12)
        self.assertAlmostEqual(samples[1][1], 1.0)
        self.assertTrue(all(x * x + y * y <= 1.0 + 1e-12 for x, y in samples))

    def test_sampling_rejects_negative_counts(self) -> None:
        with self.assertRaises(ValueError):
            sample_unit_disk_rejection(-1)

        with self.assertRaises(ValueError):
            sample_unit_disk_transform(-1)

    def test_benchmark_sampler_returns_average_and_best_times(self) -> None:
        sampler = unittest.mock.Mock(side_effect=[[(0.0, 0.0)], [(0.0, 0.0)], [(0.0, 0.0)]])

        with patch(
            "unit_disk_sampling.time.perf_counter",
            side_effect=[10.0, 10.3, 20.0, 20.4, 30.0, 30.2],
        ):
            sample_total, average_elapsed, best_elapsed = benchmark_sampler(sampler, 1, 2)

        self.assertEqual(sample_total, 1)
        self.assertAlmostEqual(average_elapsed, 0.35)
        self.assertAlmostEqual(best_elapsed, 0.3)
        self.assertEqual(sampler.call_count, 3)

    def test_main_prints_timing_lines(self) -> None:
        buffer = io.StringIO()

        with patch(
            "unit_disk_sampling.benchmark_sampler",
            side_effect=[(200_000, 0.25, 0.2), (200_000, 0.5, 0.45)],
        ):
            with redirect_stdout(buffer):
                exit_code = main()

        self.assertEqual(exit_code, 0)
        self.assertEqual(
            buffer.getvalue().splitlines(),
            [
                "Benchmarking 200000 samples per run over 5 runs.",
                "Rejection sampling produced 200000 samples per run with average time 0.250000 seconds (best 0.200000 seconds).",
                "Transform sampling produced 200000 samples per run with average time 0.500000 seconds (best 0.450000 seconds).",
            ],
        )


if __name__ == "__main__":
    unittest.main()
