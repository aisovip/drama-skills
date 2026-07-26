"""Run the official skill-creator validator without confusing two failures.

The validator lives outside this repository and pulls in its own third-party
dependencies. When it cannot start, that says nothing about whether a skill is
valid, so the caller must be able to tell "this skill is malformed" apart from
"this machine cannot run the checker".
"""

from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path


# Recent CPython colorizes tracebacks, so the interesting token is not at the
# start of the line until the escapes are removed.
ANSI = re.compile(r"\x1b\[[0-9;]*m")


class ValidatorUnavailable(RuntimeError):
    """The validator exists but cannot run in this environment."""


def validator_path() -> Path:
    codex_home = Path(os.environ.get("CODEX_HOME", str(Path.home() / ".codex")))
    return codex_home / "skills/.system/skill-creator/scripts/quick_validate.py"


def _startup_failure(stderr: str) -> str | None:
    """Return the reason when stderr shows the validator failing to import."""

    plain = ANSI.sub("", stderr)
    if "Traceback (most recent call last)" not in plain:
        return None
    last_line = next(
        (line.strip() for line in reversed(plain.splitlines()) if line.strip()),
        "",
    )
    if last_line.startswith(("ModuleNotFoundError", "ImportError")):
        return last_line
    return None


def run_official_validator(target: Path) -> subprocess.CompletedProcess[str]:
    """Validate one skill directory.

    Raises ValidatorUnavailable when the validator itself fails to load, and
    FileNotFoundError when it is not installed at all. Every other outcome is
    returned as-is so the caller judges the skill on the validator's verdict.
    """

    validator = validator_path()
    if not validator.is_file():
        raise FileNotFoundError(str(validator))
    completed = subprocess.run(
        [sys.executable, str(validator), str(target)],
        check=False,
        capture_output=True,
        text=True,
        env={**os.environ, "NO_COLOR": "1", "PYTHON_COLORS": "0"},
    )
    if completed.returncode != 0:
        reason = _startup_failure(completed.stderr)
        if reason is not None:
            raise ValidatorUnavailable(f"{validator}: {reason}")
    return completed
