#!/usr/bin/env python3
"""Build a self-contained Codex plugin from canonical repository sources."""

from __future__ import annotations

import argparse
import os
import shutil
import tempfile
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PLUGIN_SOURCE = PROJECT_ROOT / "plugins" / "swe-harness"


def ignored(_directory: str, names: list[str]) -> set[str]:
    return {
        name
        for name in names
        if name == "__pycache__" or name == ".DS_Store" or name.endswith(".pyc")
    }


def build(output: Path) -> None:
    output = output.resolve()
    if output.exists():
        raise SystemExit(f"Refusing to replace existing output: {output}")

    output.parent.mkdir(parents=True, exist_ok=True)
    staging_parent = Path(tempfile.mkdtemp(prefix="swe-harness-plugin-", dir=output.parent))
    staging = staging_parent / output.name
    try:
        shutil.copytree(PLUGIN_SOURCE, staging, ignore=ignored)
        shutil.copytree(
            PROJECT_ROOT / "swe_harness",
            staging / "lib" / "swe_harness",
            ignore=ignored,
        )
        shutil.copytree(
            PROJECT_ROOT / "templates",
            staging / "templates",
            ignore=ignored,
        )
        os.replace(staging, output)
    finally:
        shutil.rmtree(staging_parent, ignore_errors=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=PROJECT_ROOT / "dist" / "swe-harness",
        help="new directory to create (default: dist/swe-harness)",
    )
    args = parser.parse_args()
    build(args.output)
    print(f"Built plugin: {args.output.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
