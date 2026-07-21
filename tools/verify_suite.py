#!/usr/bin/env python3
"""Development entrypoint for the verifier shipped with short-drama."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import ModuleType
from typing import Any


IMPLEMENTATION = (
    Path(__file__).resolve().parents[1]
    / "skills"
    / "short-drama"
    / "scripts"
    / "suite_verify.py"
)


def _load_implementation() -> ModuleType:
    spec = importlib.util.spec_from_file_location("short_drama_suite_verify", IMPLEMENTATION)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load suite verifier: {IMPLEMENTATION}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


_IMPL = _load_implementation()


def verify_suite(core: Path) -> dict[str, Any]:
    return _IMPL.verify_suite(core)


def main(argv: list[str] | None = None) -> int:
    return _IMPL.main(argv)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
