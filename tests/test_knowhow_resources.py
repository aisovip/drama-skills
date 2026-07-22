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
        "template_dir": "assets",
        "rubric": "rubric-assets-prompts.md",
    },
    "image_prompt": {
        "skill": "short-drama-image-prompts",
        "template_dir": "assets",
        "rubric": "rubric-assets-prompts.md",
    },
    "shot": {
        "skill": "short-drama-storyboard",
        "template_dir": "assets",
        "rubric": "rubric-visual-motion.md",
    },
    "video_prompt": {
        "skill": "short-drama-video-prompts",
        "template_dir": "assets",
        "rubric": "rubric-visual-motion.md",
    },
    "continuity": {
        "skill": "short-drama-assets",
        "template_dir": "assets",
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


def parse_fenced_json(path: Path) -> dict:
    match = re.search(r"```json\n(\{.*?\})\n```", path.read_text(encoding="utf-8"), re.S)
    if match is None:
        raise AssertionError(f"missing fenced JSON object: {path}")
    return json.loads(match.group(1))


class KnowHowResourceTests(unittest.TestCase):
    def test_knowhow_index_routes_topics_to_authoritative_reference_headings(self) -> None:
        text = INDEX.read_text(encoding="utf-8")
        self.assertIn("## 主题权威路由", text)
        section = text.split("## 主题权威路由", 1)[1].split("## Story", 1)[0]
        routes = re.findall(
            r"^\| [^|]+ \| \[[^]]+\]\(([^)#]+)#([^)]+)\) \| [^|]+ \| [^|]+ \|$",
            section,
            re.MULTILINE,
        )
        self.assertGreaterEqual(len(routes), 15)

        def heading_anchor(heading: str) -> str:
            value = heading.strip().lower()
            value = re.sub(r"[^\w\-\s\u4e00-\u9fff]", "", value)
            return re.sub(r"\s+", "-", value)

        for relative, fragment in routes:
            target = (INDEX.parent / relative).resolve()
            with self.subTest(target=relative, fragment=fragment):
                target.relative_to(SKILLS.resolve())
                self.assertTrue(target.is_file())
                anchors = {
                    heading_anchor(line.lstrip("# "))
                    for line in target.read_text(encoding="utf-8").splitlines()
                    if line.startswith("## ")
                }
                self.assertIn(fragment, anchors)

    def test_creator_reference_intake_recalls_mechanism_without_copying_expression(self) -> None:
        reference = (
            SKILLS
            / "short-drama-develop/references/creative-reference-intake.md"
        )
        self.assertTrue(reference.is_file())
        skill = (SKILLS / "short-drama-develop/SKILL.md").read_text(encoding="utf-8")
        self.assertIn("references/creative-reference-intake.md", skill)
        text = reference.read_text(encoding="utf-8")
        for concept in (
            "may_influence",
            "must_not_copy",
            "观众状态",
            "戏剧问题",
            "可选机制",
            "可见效果",
            "失效边界",
            "机制摘要",
            "文风",
            "原句",
            "独特情节顺序",
            "当前会话",
        ):
            with self.subTest(concept=concept):
                self.assertIn(concept, text)

    def test_interrupted_episode_writing_uses_a_disposable_handoff_capsule(self) -> None:
        reference = SKILLS / "short-drama-write/references/scene-handoff-capsule.md"
        self.assertTrue(reference.is_file())
        skill = (SKILLS / "short-drama-write/SKILL.md").read_text(encoding="utf-8")
        self.assertIn("references/scene-handoff-capsule.md", skill)
        text = reference.read_text(encoding="utf-8")
        for concept in (
            "派生",
            "不是第二份权威",
            "scene_id",
            "agenda",
            "opposition",
            "turn",
            "exit_state",
            "setup_debt",
            "information_permissions",
            "tail_locator",
            "screenplay.md",
        ):
            with self.subTest(concept=concept):
                self.assertIn(concept, text)

    def test_anti_template_review_catches_over_explanation_without_a_banlist(self) -> None:
        text = (
            SKILLS / "short-drama-review/references/anti-template-repair.md"
        ).read_text(encoding="utf-8")
        for concept in (
            "过度解释",
            "过度收口",
            "过度工整",
            "同构微动作",
            "已经表达",
            "禁词表",
            "至少两个位置",
        ):
            with self.subTest(concept=concept):
                self.assertIn(concept, text)

    def test_craft_defaults_keep_context_and_text_only_observation_boundaries(self) -> None:
        index = INDEX.read_text(encoding="utf-8")
        self.assertNotIn("within the cold open", index)
        self.assertNotIn("dialogue exchanges stay short attack-defense turns", index)
        self.assertIn("according to genre and creator intent", index)
        self.assertIn("rather than a fixed count", index)
        self.assertIn("authorized text notes", index)
        self.assertIn("keep unobserved outcomes unknown", index)

        visual_rubric = (
            SKILLS
            / "short-drama-review/references/rubric-visual-motion.md"
        ).read_text(encoding="utf-8")
        self.assertIn("不查看媒体", visual_rubric)
        self.assertIn("文字风险", visual_rubric)
        self.assertIn("授权的文字观察记录", visual_rubric)

    def test_production_form_guidance_translates_style_into_stage_decisions(self) -> None:
        reference = SKILLS / "short-drama/references/production-form-profiles.md"
        self.assertTrue(reference.is_file())
        text = reference.read_text(encoding="utf-8")
        for concept in (
            "实拍",
            "2D 动态漫",
            "风格化 3D",
            "水墨",
            "Q 版知识",
            "叙事职责",
            "运动预算",
            "来源",
            "artifact",
            "taste",
            "环境物理",
            "身份形态",
            "身份占用",
            "陆地动作词",
            "风格代码",
        ):
            with self.subTest(concept=concept):
                self.assertIn(concept, text)
        self.assertIn("风格名称、模型代码或供应商字段不能替代", text)
        self.assertIn("不把拆镜或换形态默认为已经授权的替代", text)

        linked_skills = {
            "short-drama",
            "short-drama-develop",
            "short-drama-assets",
            "short-drama-image-prompts",
            "short-drama-storyboard",
            "short-drama-video-prompts",
            "short-drama-review",
        }
        for skill in linked_skills:
            with self.subTest(skill=skill):
                self.assertIn(
                    "production-form-profiles.md",
                    (SKILLS / skill / "SKILL.md").read_text(encoding="utf-8"),
                )

    def test_genre_playbook_includes_identity_mismatch_and_small_life_stories(self) -> None:
        text = (
            SKILLS
            / "short-drama-develop/references/genre-and-hook-playbook.md"
        ).read_text(encoding="utf-8")
        for concept in (
            "身份错位",
            "外部任务",
            "身份状态",
            "设定梗",
            "生活流",
            "小目标",
            "温柔反转",
            "真人爽剧",
        ):
            with self.subTest(concept=concept):
                self.assertIn(concept, text)

    def test_review_distinguishes_current_text_authority_from_task_status(self) -> None:
        text = (
            SKILLS / "short-drama-review/references/production-quality-gates.md"
        ).read_text(encoding="utf-8")
        for concept in (
            "当前权威版本",
            "accepted artifact",
            "旧版本",
            "技术状态",
            "语义质量",
            "提示词 hash",
        ):
            with self.subTest(concept=concept):
                self.assertIn(concept, text)

    def test_index_has_unique_rules_in_all_eight_layers(self) -> None:
        rules = parse_index()
        self.assertTrue(rules)
        self.assertEqual({rule.split("-", 1)[0] for rule in rules}, set(PREFIX_OWNERS))
        self.assertEqual(set(rules.values()), CLASSES)

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

    def test_serial_contract_fields_are_projected_to_writing_templates(self) -> None:
        develop = SKILLS / "short-drama-develop"
        write = SKILLS / "short-drama-write"
        serial_fields = {
            "local_dramatic_result",
            "character_progression",
            "information_release",
            "rhythm_plan",
        }
        release_fields = {
            "visible_carrier",
            "supported_claim",
            "unresolved_inference",
        }

        episode = json.loads(
            (develop / "assets/episode-map.jsonl").read_text(encoding="utf-8").strip()
        )
        self.assertTrue(serial_fields <= episode.keys())
        self.assertTrue(release_fields <= episode["information_release"][0].keys())

        projected = json.loads(
            (write / "assets/episode-card.json").read_text(encoding="utf-8")
        )
        projected_fields = set(projected["contract_authority"]["projected_fields"])
        self.assertTrue({f"/{field}" for field in serial_fields} <= projected_fields)

        standalone = json.loads(
            (write / "assets/episode-card-standalone.json").read_text(encoding="utf-8")
        )
        owned = standalone["owned_contract"]
        self.assertTrue(serial_fields <= owned.keys())
        self.assertTrue(release_fields <= owned["information_release"][0].keys())

        beat = json.loads(
            (write / "assets/beats.jsonl").read_text(encoding="utf-8").strip()
        )
        self.assertTrue({"dramatic_result", "rhythm"} <= beat.keys())

    def test_character_example_separates_voice_identity_from_delivery_state(self) -> None:
        character = json.loads(
            (SKILLS / "short-drama-assets/assets/character-look.example.jsonl")
            .read_text(encoding="utf-8")
            .splitlines()[0]
        )
        voice = character["voice_direction"]
        self.assertTrue(
            {
                "language",
                "persistent_anchors",
                "pronunciation_notes",
                "reference_ref",
                "not_voice_identity",
            }
            <= voice.keys()
        )
        self.assertIsNone(voice["reference_ref"])
        self.assertNotIn("provider", json.dumps(voice).casefold())

    def test_adaptation_map_points_into_inputs_without_copying_source_text(self) -> None:
        mapping = json.loads(
            (SKILLS / "short-drama-develop/assets/adaptation-map.example.jsonl")
            .read_text(encoding="utf-8")
            .strip()
        )
        self.assertTrue(mapping["source_ref"]["artifact"].startswith("inputs/"))
        self.assertTrue(
            {"byte_start", "byte_end", "content_sha256"}
            <= mapping["source_span"].keys()
        )
        self.assertIn("function_summary", mapping)
        self.assertNotIn("source_text", mapping)
        self.assertEqual(mapping["status"], "candidate")

    def test_new_rules_have_reviewed_classification(self) -> None:
        self.assertEqual(parse_index().get("IMG-08"), "reviewed_invariant")
        self.assertEqual(parse_index().get("IMG-09"), "reviewed_invariant")
        self.assertEqual(parse_index().get("SHT-12"), "reviewed_invariant")
        self.assertEqual(parse_index().get("VID-11"), "reviewed_invariant")
        self.assertEqual(parse_index().get("VID-12"), "reviewed_invariant")
        self.assertEqual(parse_index().get("AST-07"), "reviewed_invariant")
        self.assertEqual(parse_index().get("SHT-13"), "reviewed_invariant")
        self.assertEqual(parse_index().get("SHT-14"), "reviewed_invariant")

    def test_reference_roles_visibility_and_pickup_scope_are_explicit(self) -> None:
        image_spec = parse_fenced_json(
            SKILLS / "short-drama-image-prompts/assets/image-prompt-spec.jsonl.md"
        )
        image_binding = image_spec["reference_bindings"][0]
        self.assertTrue(
            {
                "artifact_ref",
                "role",
                "may_control",
                "must_not_control",
                "admission_status",
                "reference_observation_ref",
                "unresolved_risks",
            }
            <= image_binding.keys()
        )
        self.assertNotIn("|", image_binding["role"])
        self.assertNotIn("+", image_binding["role"])
        self.assertEqual(
            image_binding["admission_status"],
            "unverified | creator_described | visually_inspected",
        )
        shot = json.loads(
            (SKILLS / "short-drama-storyboard/assets/shot-template.jsonl")
            .read_text(encoding="utf-8")
            .strip()
        )
        visibility = shot["audience_visibility"]
        self.assertIsInstance(visibility, list)
        self.assertTrue(visibility)
        self.assertTrue(
            {
                "source_ref",
                "fact",
                "permission",
                "carrier",
                "reveal_trigger",
                "protection_method",
                "rationale",
            }
            <= visibility[0].keys()
        )
        self.assertTrue(
            {"owner", "artifact", "hash", "record_id"}
            <= visibility[0]["source_ref"].keys()
        )
        motion = parse_fenced_json(
            SKILLS / "short-drama-video-prompts/assets/motion-spec.jsonl.md"
        )
        motion_binding = motion["reference_bindings"][0]
        self.assertTrue(
            {
                "artifact_ref",
                "role",
                "may_control",
                "must_not_control",
                "admission_status",
                "reference_observation_ref",
                "unresolved_risks",
            }
            <= motion_binding.keys()
        )
        self.assertNotIn("|", motion_binding["role"])
        self.assertNotIn("+", motion_binding["role"])
        self.assertEqual(
            motion_binding["admission_status"],
            "unverified | creator_described | visually_inspected",
        )
        audio = motion["audio"][0]
        for field in ("source_ref", "speaker_ref", "voice_direction_ref"):
            self.assertTrue(
                {"owner", "artifact", "hash", "record_id"}
                <= audio[field].keys()
            )
        self.assertEqual(audio["speaker_ref"]["owner"], "short-drama-assets")
        self.assertEqual(
            audio["voice_direction_ref"]["field"], "/voice_direction"
        )
        coverage_scope = motion["coverage_scope"]
        self.assertTrue(
            {
                "mode",
                "master_motion_id",
                "supplements_motion_ids",
                "source_obligations",
                "replacement_intent",
            }
            <= coverage_scope.keys()
        )
        self.assertTrue(coverage_scope["source_obligations"])
        obligations = coverage_scope["source_obligations"]
        self.assertEqual(
            {obligation["kind"] for obligation in obligations},
            {"action", "reaction", "dialogue", "reveal", "directive", "end_boundary"},
        )
        for obligation in obligations:
            source_ref = obligation["source_ref"]
            self.assertTrue(
                {"owner", "artifact", "hash"} <= source_ref.keys()
            )
            self.assertTrue(
                "record_id" in source_ref or "field" in source_ref,
                "JSON field refs may omit record_id; record refs must name the record",
            )
        self.assertTrue(
            {"kind", "source_ref", "disposition", "motion_field"}
            <= obligations[0].keys()
        )
        self.assertNotIn("supersession_review_ref", json.dumps(motion))
        verdict = json.loads(
            (SKILLS / "short-drama-review/assets/verdict-template.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertIn("supersession_decisions", verdict)
        supersession = json.loads(
            (SKILLS / "short-drama-review/assets/supersession-decision.example.json")
            .read_text(encoding="utf-8")
        )
        self.assertTrue(
            {"alternate_ref", "master_ref", "checked_obligations", "decision"}
            <= supersession.keys()
        )
        self.assertNotEqual(
            supersession["alternate_ref"]["hash"], supersession["master_ref"]["hash"]
        )

        observation = json.loads(
            (SKILLS / "short-drama/assets/reference-observation.example.jsonl")
            .read_text(encoding="utf-8")
            .strip()
        )
        self.assertTrue(
            {
                "reference_artifact_ref",
                "admission_status",
                "observed_media_sha256",
                "method",
                "observer",
                "observed_regions",
                "text_policy_conclusion",
                "unresolved_risks",
            }
            <= observation.keys()
        )
        self.assertEqual(
            observation["admission_status"],
            "creator_described | visually_inspected",
        )

    def test_long_references_have_early_navigation(self) -> None:
        for reference in SKILLS.glob("*/references/*.md"):
            lines = reference.read_text(encoding="utf-8").splitlines()
            if len(lines) <= 100:
                continue
            with self.subTest(reference=reference.relative_to(SUITE)):
                self.assertTrue(
                    any(
                        line.strip() in {"## 目录", "## Contents", "## Table of contents"}
                        for line in lines[:35]
                    ),
                    "references over 100 lines need an early table of contents",
                )


class GovernanceSemanticsTests(unittest.TestCase):
    def test_relationship_templates_separate_same_artifact_ids_from_cross_artifact_refs(self) -> None:
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

        fixture = SKILLS / "short-drama-assets/assets/decisions.example.jsonl"
        for line_number, line in enumerate(fixture.read_text(encoding="utf-8").splitlines(), 1):
            document = json.loads(line)
            status = document.get("creator_acceptance", {}).get("status")
            if status != "accepted":
                self.assertNotIn("accepted_binding", document, f"line {line_number}")
                self.assertIn("proposed_binding", document, f"line {line_number}")

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
                    self.assertIn(severity, {"fatal", "error", "warning", "note"})
                    self.assertTrue(owner)
                    if classification == "structural_invariant":
                        self.assertEqual(enforcer, "validator")
                    elif classification == "reviewed_invariant":
                        self.assertEqual(enforcer, "reviewer")
                    else:
                        self.assertNotEqual(enforcer, "validator")
                        self.assertNotIn(severity, {"fatal", "error"})
                rows_checked += 1
        self.assertGreaterEqual(rows_checked, 8, "no usable diagnostic catalog was found")

    def test_motion_and_review_templates_use_canonical_project_paths(self) -> None:
        motion = (
            SKILLS / "short-drama-video-prompts/assets/motion-spec.jsonl.md"
        ).read_text(encoding="utf-8")
        self.assertIn('"record_id": "BLK-<EP>-<SC>-D<nn>"', motion)
        self.assertIn('"artifact": "short-drama.json"', motion)
        self.assertIn('"field": "/creator_authority/production_profile"', motion)
        self.assertNotIn("DIALOGUE-<id>", motion)
        self.assertNotIn("project-profile.json", motion)

        supersession = json.loads(
            (SKILLS / "short-drama-review/assets/supersession-decision.example.json")
            .read_text(encoding="utf-8")
        )
        for key in ("alternate_ref", "master_ref"):
            self.assertEqual(
                supersession[key]["artifact"],
                "episodes/EP001/storyboard/motion-specs.jsonl",
            )
        verdict = json.loads(
            (SKILLS / "short-drama-review/assets/verdict-template.json")
            .read_text(encoding="utf-8")
        )
        self.assertEqual(verdict["findings_ref"]["artifact"], "reviews/findings.jsonl")

if __name__ == "__main__":
    unittest.main()
