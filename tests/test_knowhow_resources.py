import json
import re
import unittest
from pathlib import Path


SUITE = Path(__file__).resolve().parents[1]
SKILLS = SUITE / "skills"
INDEX = SKILLS / "short-drama/references/knowhow-index.md"

CLASSES = {
    "structural_invariant",
    "reviewed_invariant",
    "craft_default",
    "taste_option",
}

PREFIX_OWNERS = {
    "STY": ("short-drama-develop",),
    "SCR": ("short-drama-write",),
    "AST": ("short-drama-assets",),
    "IMG": ("short-drama-image-prompts",),
    "SHT": ("short-drama-storyboard",),
    "VID": ("short-drama-video-prompts",),
    # Assets own inter-scene state deltas; storyboard owns shot boundaries; motion
    # must compare its projection with both, so continuity guidance may live in any.
    "CON": (
        "short-drama-assets",
        "short-drama-storyboard",
        "short-drama-video-prompts",
    ),
    "REV": ("short-drama-review",),
}

LAYER_RESOURCES = {
    "story": {
        "skill": "short-drama-develop",
        "template_dir": "assets",
        "rubric": "rubric-story-script.md",
    },
    "script": {
        "skill": "short-drama-write",
        "template_dir": "assets",
        "rubric": "rubric-story-script.md",
    },
    "asset": {
        "skill": "short-drama-assets",
        "template_dir": "templates",
        "rubric": "rubric-assets-prompts.md",
    },
    "image_prompt": {
        "skill": "short-drama-image-prompts",
        "template_dir": "templates",
        "rubric": "rubric-assets-prompts.md",
    },
    "shot": {
        "skill": "short-drama-storyboard",
        "template_dir": "assets",
        "rubric": "rubric-visual-motion.md",
    },
    "video_prompt": {
        "skill": "short-drama-video-prompts",
        "template_dir": "templates",
        "rubric": "rubric-visual-motion.md",
    },
    "continuity": {
        "skill": "short-drama-assets",
        "template_dir": "templates",
        "template_name": "continuity.example.jsonl",
        "rubric": "rubric-assets-prompts.md",
    },
    "review": {
        "skill": "short-drama-review",
        "template_dir": "assets",
        "rubric": "review-method.md",
    },
}


def parse_index() -> dict[str, str]:
    rules: dict[str, str] = {}
    pattern = re.compile(
        r"^\| ((?:STY|SCR|AST|IMG|SHT|VID|CON|REV)-\d{2}) "
        r"\| ([a-z_]+) \|",
        re.MULTILINE,
    )
    for rule_id, classification in pattern.findall(INDEX.read_text(encoding="utf-8")):
        if rule_id in rules:
            raise AssertionError(f"duplicate know-how ID: {rule_id}")
        rules[rule_id] = classification
    return rules


def resource_files(skill_name: str) -> list[Path]:
    skill = SKILLS / skill_name
    files: list[Path] = []
    for directory in ("references", "templates", "assets"):
        root = skill / directory
        if root.is_dir():
            files.extend(path for path in root.rglob("*") if path.is_file())
    return files


class KnowHowResourceTests(unittest.TestCase):
    def test_index_has_unique_rules_in_all_eight_layers(self) -> None:
        rules = parse_index()
        self.assertTrue(rules)
        self.assertEqual({rule.split("-", 1)[0] for rule in rules}, set(PREFIX_OWNERS))
        self.assertEqual(set(rules.values()), CLASSES)

    def test_every_rule_is_grounded_in_an_owning_skill_resource(self) -> None:
        """The index is navigation; the transferable method must live in a resource."""

        missing: list[str] = []
        for rule_id in parse_index():
            prefix = rule_id.split("-", 1)[0]
            candidates = [
                path
                for owner in PREFIX_OWNERS[prefix]
                for path in resource_files(owner)
            ]
            if not any(rule_id in path.read_text(encoding="utf-8") for path in candidates):
                missing.append(
                    f"{rule_id} -> {', '.join(PREFIX_OWNERS[prefix])} "
                    "reference/template/rubric"
                )
        self.assertEqual(missing, [], "unmapped know-how IDs:\n" + "\n".join(missing))

    def test_each_layer_ships_reference_template_rubric_and_fixture(self) -> None:
        fixture_root = SUITE / "tests/fixtures"
        fixtures = list(fixture_root.rglob("*.json"))
        covered: set[str] = set()
        for path in fixtures:
            document = json.loads(path.read_text(encoding="utf-8"))
            if isinstance(document.get("layer"), str):
                covered.add(document["layer"])
            covered.update(document.get("coverage_layers", []))

        review_root = SKILLS / "short-drama-review/references"
        for layer, matrix in LAYER_RESOURCES.items():
            with self.subTest(layer=layer):
                skill = SKILLS / matrix["skill"]
                self.assertTrue(any((skill / "references").glob("*.md")))
                template_root = skill / matrix["template_dir"]
                if "template_name" in matrix:
                    self.assertTrue((template_root / matrix["template_name"]).is_file())
                else:
                    self.assertTrue(any(path.is_file() for path in template_root.rglob("*")))
                self.assertTrue((review_root / matrix["rubric"]).is_file())
                self.assertIn(layer, covered)

    def test_craft_owner_references_name_all_governance_classes(self) -> None:
        owners = {matrix["skill"] for matrix in LAYER_RESOURCES.values()}
        for owner in sorted(owners):
            reference_text = "\n".join(
                path.read_text(encoding="utf-8")
                for path in (SKILLS / owner / "references").glob("*.md")
            )
            with self.subTest(owner=owner):
                for classification in CLASSES:
                    self.assertIn(classification, reference_text)


class GovernanceSemanticsTests(unittest.TestCase):
    def test_relationship_templates_separate_same_artifact_ids_from_cross_artifact_refs(self) -> None:
        contract = (
            SKILLS / "short-drama/references/contract-and-ownership.md"
        ).read_text(encoding="utf-8")
        for phrase in (
            "`*_ids`",
            "`*_refs`",
            "circular hashes",
            "coverage `shot_refs`",
            "`text_treatment_refs`",
        ):
            self.assertIn(phrase, contract)

        beat = json.loads(
            (SKILLS / "short-drama-write/assets/beats.jsonl")
            .read_text(encoding="utf-8")
            .strip()
        )
        for field in (
            "because_of_ids",
            "because_of_refs",
            "setup_ids",
            "setup_refs",
            "payoff_ids",
            "payoff_refs",
        ):
            self.assertIn(field, beat)

        episode = json.loads(
            (SKILLS / "short-drama-develop/assets/episode-map.jsonl")
            .read_text(encoding="utf-8")
            .strip()
        )
        self.assertIn("setup_ids", episode)
        self.assertIn("payoff_ids", episode)
        self.assertNotIn("setup_refs", episode)
        self.assertNotIn("payoff_refs", episode)

        coverage = json.loads(
            (SKILLS / "short-drama-storyboard/assets/coverage-template.json")
            .read_text(encoding="utf-8")
        )
        shot_ref = coverage["dispositions"][0]["shot_refs"][0]
        self.assertTrue({"owner", "artifact", "hash", "record_id"}.issubset(shot_ref))

        for name in ("shot-template.jsonl", "keyframe-template.jsonl"):
            document = json.loads(
                (SKILLS / "short-drama-storyboard/assets" / name)
                .read_text(encoding="utf-8")
                .strip()
            )
            text_ref = document["text_treatment_refs"][0]
            self.assertTrue(
                {"owner", "artifact", "hash", "record_id", "field"}.issubset(text_ref)
            )
            self.assertEqual(text_ref["artifact"], "bible/props.jsonl")
            self.assertEqual(text_ref["field"], "/text_policy")

    def test_proposed_asset_decisions_never_publish_accepted_bindings(self) -> None:
        import json

        fixture = SKILLS / "short-drama-assets/templates/decisions.example.jsonl"
        for line_number, line in enumerate(fixture.read_text(encoding="utf-8").splitlines(), 1):
            document = json.loads(line)
            status = document.get("creator_acceptance", {}).get("status")
            if status != "accepted":
                self.assertNotIn("accepted_binding", document, f"line {line_number}")
                self.assertIn("proposed_binding", document, f"line {line_number}")

    def test_end_to_end_preview_does_not_impersonate_creator_acceptance(self) -> None:
        workflow = (
            SKILLS / "short-drama/references/creator-workflow.md"
        ).read_text(encoding="utf-8")
        for phrase in (
            "provisional preview chain",
            "authority: candidate",
            "creator acceptance stays pending",
            "delivery stays blocked",
            "Never manufacture creator-decision records",
        ):
            self.assertIn(phrase, workflow)

    def test_diagnostic_catalogs_declare_complete_enforcement_metadata(self) -> None:
        catalogs = list(SKILLS.glob("*/references/*review*.md"))
        rows_checked = 0
        for catalog in catalogs:
            lines = catalog.read_text(encoding="utf-8").splitlines()
            for line in lines:
                cells = [cell.strip().strip("`") for cell in line.strip().strip("|").split("|")]
                if len(cells) < 6 or cells[1] not in CLASSES:
                    continue
                code, classification, enforcer, severity, owner = cells[:5]
                with self.subTest(catalog=catalog.name, code=code):
                    self.assertRegex(code, r"^[A-Z][A-Z0-9_]+$")
                    self.assertIn(enforcer, {"validator", "reviewer", "creator"})
                    self.assertTrue(severity)
                    self.assertTrue(owner)
                    if classification == "structural_invariant":
                        self.assertEqual(enforcer, "validator")
                    elif classification == "reviewed_invariant":
                        self.assertEqual(enforcer, "reviewer")
                    else:
                        self.assertNotEqual(enforcer, "validator")
                        self.assertNotIn(severity, {"fatal", "error", "revise"})
                rows_checked += 1
        self.assertGreaterEqual(rows_checked, 8, "no usable diagnostic catalog was found")

    def test_lexical_heuristics_are_not_described_as_deterministic_blockers(self) -> None:
        lexical = re.compile(
            r"(?:regex|正则|关键词|word\s*count|词数|字数|动词数|形容词比例|固定每秒)",
            re.IGNORECASE,
        )
        blocking = re.compile(r"(?:block|阻断|fail|失败|reject|拒绝|error|错误)", re.IGNORECASE)
        negated = re.compile(
            r"(?:不|非|禁止|不得|不要|不能|never|not|isn.t|is not|without|避免)",
            re.IGNORECASE,
        )
        violations: list[str] = []
        for path in SKILLS.rglob("*.md"):
            for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
                if lexical.search(line) and blocking.search(line) and not negated.search(line):
                    violations.append(f"{path.relative_to(SUITE)}:{line_number}: {line.strip()}")
        self.assertEqual(
            violations,
            [],
            "lexical/quantity heuristics must stay reviewer evidence, not blockers:\n"
            + "\n".join(violations),
        )


if __name__ == "__main__":
    unittest.main()
