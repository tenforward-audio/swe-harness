#!/usr/bin/env python3
"""Run SWE Harness from a source checkout or a built plugin."""

from __future__ import annotations

import sys
from pathlib import Path


plugin_root = Path(__file__).resolve().parents[1]
candidate_roots = (plugin_root / "lib", plugin_root.parents[1])

for candidate in candidate_roots:
    if (candidate / "swe_harness").is_dir():
        sys.path.insert(0, str(candidate))
        break
else:
    raise SystemExit("SWE Harness runtime is missing from this plugin")

from swe_harness.cli import main  # noqa: E402


if __name__ == "__main__":
    raise SystemExit(main())
