import re
import unittest
from pathlib import Path


SUITE = Path(__file__).resolve().parents[1]
SHIPPED_SKILLS = SUITE / "skills"


def shipped_text_files() -> list[Path]:
    allowed_suffixes = {".md", ".json", ".jsonl", ".yaml", ".py"}
    return [
        path
        for path in SHIPPED_SKILLS.rglob("*")
        if path.is_file()
        and path.suffix.lower() in allowed_suffixes
        and "__pycache__" not in path.parts
    ]


def local_forbidden_terms() -> frozenset[str]:
    # Maintainer-specific source vocabulary lives outside the repository so the
    # shipped tree never carries the terms it screens for. One term per line.
    local = Path(__file__).resolve().parent / "local-terms.txt"
    if not local.is_file():
        return frozenset()
    return frozenset(
        stripped
        for line in local.read_text(encoding="utf-8").splitlines()
        if (stripped := line.strip()) and not stripped.startswith("#")
    )


class ShippingBoundaryTests(unittest.TestCase):
    def test_release_manifest_contains_no_cache_or_binary_artifact(self) -> None:
        import json

        manifest = json.loads(
            (SHIPPED_SKILLS / "short-drama/suite-manifest.json").read_text(encoding="utf-8")
        )
        forbidden = {".pyc", ".pyo", ".so", ".dylib", ".dll", ".exe"}
        findings = [
            relative
            for relative in manifest["files"]
            if "__pycache__" in Path(relative).parts
            or Path(relative).suffix.lower() in forbidden
        ]
        self.assertEqual(findings, [])

    def test_shipped_tree_contains_no_urls(self) -> None:
        url = re.compile(r"https?://[^\s)>\]}`\"']+", re.IGNORECASE)
        leaks: list[str] = []
        for path in shipped_text_files():
            for found in url.findall(path.read_text(encoding="utf-8")):
                leaks.append(f"{path.relative_to(SUITE)}: {found}")
        self.assertEqual(leaks, [], "URLs shipped in skills tree:\n" + "\n".join(leaks))

    def test_shipping_tree_has_no_private_source_or_provider_task_vocabulary(self) -> None:
        # Assemble source-specific terms so the privacy test itself cannot become
        # a fingerprint hit if the maintainer tree is scanned separately.
        forbidden = {
            "mongo" + "db",
            "private" + " corpus",
            "provider" + "task",
            "provider" + "_task",
            "project" + "token",
            "backup" + "_project",
            "entity" + "_collections",
        }
        forbidden |= local_forbidden_terms()
        findings: list[str] = []
        for path in shipped_text_files():
            text = path.read_text(encoding="utf-8").casefold()
            for term in sorted(forbidden):
                if term.casefold() in text:
                    findings.append(f"{path.relative_to(SUITE)}: {term}")
        self.assertEqual(
            findings,
            [],
            "private schema/source or provider task vocabulary shipped:\n"
            + "\n".join(findings),
        )

    def test_shipping_tree_has_no_machine_absolute_paths(self) -> None:
        patterns = {
            "unix": re.compile(r"(?<![\w.])/(?:Users|home|private|var|tmp)/"),
            "windows": re.compile(r"\b[A-Za-z]:[\\/]"),
            "file_url": re.compile(r"\bfile://", re.IGNORECASE),
        }
        findings: list[str] = []
        for path in shipped_text_files():
            text = path.read_text(encoding="utf-8")
            for name, pattern in patterns.items():
                if pattern.search(text):
                    findings.append(f"{path.relative_to(SUITE)}: {name}")
        self.assertEqual(findings, [], "machine paths shipped:\n" + "\n".join(findings))

    def test_deterministic_scripts_do_not_import_network_or_private_runtime_clients(self) -> None:
        forbidden_imports = re.compile(
            r"^\s*(?:from|import)\s+(?:socket|urllib|httpx?|requests|aiohttp|pymongo)\b",
            re.MULTILINE,
        )
        runtime_lookup = re.compile(
            r"(?:connect|query|lookup|fetch|download).{0,32}(?:database|corpus|backup|provider)",
            re.IGNORECASE,
        )
        findings: list[str] = []
        for path in SHIPPED_SKILLS.rglob("*.py"):
            if "__pycache__" in path.parts:
                continue
            text = path.read_text(encoding="utf-8")
            if forbidden_imports.search(text):
                findings.append(f"{path.relative_to(SUITE)}: outbound/private import")
            if runtime_lookup.search(text):
                findings.append(f"{path.relative_to(SUITE)}: runtime source lookup")
        self.assertEqual(findings, [], "runtime boundary violations:\n" + "\n".join(findings))


if __name__ == "__main__":
    unittest.main()
