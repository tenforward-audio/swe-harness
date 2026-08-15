#!/usr/bin/env python3
"""Compatibility wrapper for the SWE Harness doctor command."""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from swe_harness.cli import main


def compatibility_main(arguments: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="repository root (defaults to the parent of this script directory)",
    )
    args = parser.parse_args(arguments)
    return main(["doctor", str(args.root)])


if __name__ == "__main__":
    raise SystemExit(compatibility_main())
