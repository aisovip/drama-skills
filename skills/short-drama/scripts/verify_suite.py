#!/usr/bin/env python3
"""Verify one installed, version-consistent short-drama skill suite."""

from __future__ import annotations

import json
import hashlib
import sys
from pathlib import Path
from typing import Any


CHILD_REF_KEYS = {
    "suite",
    "suite_version",
    "contract_version",
    "core_skill",
    "core_manifest",
    "recipe_version",
    "core_manifest_sha256",
}


def load_json(path: Path) -> dict[str, Any]:
    document = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(document, dict):
        raise ValueError(f"expected JSON object: {path}")
    return document


def verify_suite(core: Path) -> dict[str, Any]:
    core = core.resolve()
    manifest_path = core / "suite-manifest.json"
    manifest = load_json(manifest_path)
    manifest_hash = hashlib.sha256(manifest_path.read_bytes()).hexdigest()
    skills_root = core.parent
    expected = manifest.get("public_skills")
    if not isinstance(expected, list) or not all(isinstance(name, str) for name in expected):
        raise ValueError("suite-manifest public_skills must be a string list")
    core_skill = manifest.get("core_skill")
    if not isinstance(core_skill, str) or core_skill not in expected:
        raise ValueError("suite-manifest core_skill must name one public skill")
    child_refs = {
        f"{name}/suite-ref.json" for name in expected if name != core_skill
    }
    files = manifest.get("files")
    if not isinstance(files, dict) or not all(
        isinstance(path, str) and isinstance(digest, str)
        for path, digest in files.items()
    ):
        raise ValueError("suite-manifest files must map relative paths to SHA-256")

    actual_files: set[str] = set()
    for path in skills_root.rglob("*"):
        # Local bytecode caches are development noise, never release content;
        # update_suite_manifest.py excludes them from the inventory the same way.
        if not path.is_file() or path == manifest_path or "__pycache__" in path.parts:
            continue
        relative = path.relative_to(skills_root).as_posix()
        if relative not in child_refs:
            actual_files.add(relative)
    unexpected = sorted(actual_files - set(files))
    missing = sorted(set(files) - actual_files)
    if unexpected:
        raise ValueError(f"unexpected suite files: {', '.join(unexpected)}")
    if missing:
        raise ValueError(f"missing manifest files: {', '.join(missing)}")
    for relative, expected_hash in files.items():
        actual_hash = hashlib.sha256((skills_root / relative).read_bytes()).hexdigest()
        if actual_hash != expected_hash:
            raise ValueError(f"content hash mismatch: {relative}")

    checked: list[str] = []
    for name in expected:
        skill = skills_root / name
        if not (skill / "SKILL.md").is_file():
            raise FileNotFoundError(f"missing skill: {name}")
        if name != core_skill:
            reference = load_json(skill / "suite-ref.json")
            if set(reference) != CHILD_REF_KEYS:
                raise ValueError(f"{name} suite-ref keys are invalid")
            for key in (
                "suite",
                "suite_version",
                "contract_version",
                "recipe_version",
                "core_skill",
            ):
                if reference.get(key) != manifest.get(key):
                    raise ValueError(f"{name} mixed {key}: {reference.get(key)!r}")
            if reference.get("core_manifest_sha256") != manifest_hash:
                raise ValueError(f"{name} core manifest hash mismatch")
            resolved = (skill / str(reference.get("core_manifest"))).resolve()
            if resolved != manifest_path.resolve():
                raise ValueError(f"{name} resolves the wrong core manifest")
        checked.append(name)
    return {
        "suite": manifest.get("suite"),
        "suite_version": manifest.get("suite_version"),
        "contract_version": manifest.get("contract_version"),
        "recipe_version": manifest.get("recipe_version"),
        "core_manifest_sha256": manifest_hash,
        "checked_skills": checked,
        "checked_files": len(files),
    }


def main(argv: list[str] | None = None) -> int:
    core = Path(argv[0]) if argv else Path(__file__).resolve().parents[1]
    try:
        print(json.dumps(verify_suite(core), ensure_ascii=False, sort_keys=True))
        return 0
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"{type(error).__name__}: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
