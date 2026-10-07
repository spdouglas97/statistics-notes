from __future__ import annotations

import io
import sys
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from run_mersenne_twister import main


class RunMersenneTwisterTests(unittest.TestCase):
    def test_main_prints_requested_amount(self) -> None:
        buffer = io.StringIO()

        with patch(
            "sys.argv",
            ["run_mersenne_twister.py", "--seed", "5489", "--count", "3"],
        ):
            with redirect_stdout(buffer):
                exit_code = main()

        self.assertEqual(exit_code, 0)
        self.assertEqual(
            buffer.getvalue().splitlines(),
            [
                "0.8147236919030547",
                "0.13547700410708785",
                "0.9057919341139495",
            ],
        )


if __name__ == "__main__":
    unittest.main()
