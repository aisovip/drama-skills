import json
import re
import unittest
from pathlib import Path

SUITE = Path(__file__).resolve().parents[1]
SKILLS = SUITE / "skills"
INDEX = SKILLS / "short-drama/references/knowhow-index.md"

CONTAINER_TEMPLATE = (
    SKILLS / "short-drama-video-prompts/assets/delivery-container.jsonl.md"
)
MOTION_TEMPLATE = SKILLS / "short-drama-video-prompts/assets/motion-spec.jsonl.md"
PREMISE = SKILLS / "short-drama-develop/references/premise-devices.md"
BLOCKING = SKILLS / "short-drama-storyboard/references/blocking-playbooks.md"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def fenced_json(path: Path) -> dict:
    match = re.search(r"```json\n(\{.*?\})\n```", read(path), re.DOTALL)
    if match is None:
        raise AssertionError(f"missing fenced JSON template: {path}")
    return json.loads(match.group(1))


def index_rules() -> dict[str, str]:
    pattern = re.compile(
        r"^\| ((?:STY|SCR|AST|IMG|SHT|VID|CON|REV)-\d{2}) \| ([a-z_]+) \|",
        re.MULTILINE,
    )
    return dict(pattern.findall(read(INDEX)))


class NewRuleRegistrationTests(unittest.TestCase):
    def test_new_rules_are_registered_with_their_intended_class(self) -> None:
        rules = index_rules()
        expected = {
            "STY-16": "craft_default",
            "STY-17": "reviewed_invariant",
            "SCR-09": "craft_default",
            "IMG-10": "reviewed_invariant",
            "SHT-15": "reviewed_invariant",
            "VID-13": "structural_invariant",
            "VID-14": "craft_default",
        }
        for rule_id, classification in expected.items():
            with self.subTest(rule=rule_id):
                self.assertEqual(rules.get(rule_id), classification)

    def test_segment_sum_rule_names_the_shot_not_the_container(self) -> None:
        """VID-04 and VID-13 apply to different objects; the text must say which."""

        self.assertIn("sums exactly to its shot's accepted duration", read(INDEX))


class DeliveryContainerRecordTests(unittest.TestCase):
    """VID-13 is structural, so a canonical record must carry its evidence."""

    def test_container_template_carries_members_durations_and_profile_ref(self) -> None:
        document = fenced_json(CONTAINER_TEMPLATE)
        self.assertEqual(document["status"], "candidate")
        for key in ("container_id", "members", "container_duration", "membership_basis"):
            with self.subTest(key=key):
                self.assertIn(key, document)

        member = document["members"][0]
        for key in ("order", "shot_ref", "motion_ref", "accepted_duration_ref"):
            with self.subTest(member_key=key):
                self.assertIn(key, member)

        self.assertEqual(member["shot_ref"]["owner"], "short-drama-storyboard")
        self.assertEqual(member["motion_ref"]["owner"], "short-drama-video-prompts")
        self.assertEqual(
            member["accepted_duration_ref"]["owner"], "short-drama-storyboard"
        )
        self.assertEqual(member["accepted_duration_ref"]["field"], "/duration")
        self.assertEqual(
            document["delivery_profile_ref"]["field"],
            "/creator_authority/production_profile",
        )

    def test_container_template_states_its_local_verification_points(self) -> None:
        text = read(CONTAINER_TEMPLATE)
        for concept in ("唯一、连续、升序", "之和", "缓存", "只读投影"):
            with self.subTest(concept=concept):
                self.assertIn(concept, text)

    def test_motion_spec_points_at_the_container_without_gaining_authority(self) -> None:
        document = fenced_json(MOTION_TEMPLATE)
        container_ref = document["container_ref"]
        self.assertEqual(
            container_ref["artifact"],
            "episodes/<EP>/storyboard/delivery-containers.jsonl",
        )
        self.assertEqual(container_ref["owner"], "short-drama-video-prompts")
        self.assertIn("只读指针", read(MOTION_TEMPLATE))

    def test_container_owner_is_registered_and_published(self) -> None:
        ownership = read(SKILLS / "short-drama/references/contract-and-ownership.md")
        self.assertIn("delivery-containers.jsonl", ownership)
        skill = read(SKILLS / "short-drama-video-prompts/SKILL.md")
        self.assertIn("delivery-containers.jsonl", skill)


class PremiseDeviceLayerTests(unittest.TestCase):
    """STY-17 must not collapse creator contract into in-fiction disclosure."""

    def test_contract_and_disclosure_are_named_as_separate_layers(self) -> None:
        text = read(PREMISE)
        self.assertIn("装置契约（创作者层）", text)
        self.assertIn("披露状态（剧中层）", text)

    def test_partial_disclosure_is_explicitly_not_a_defect(self) -> None:
        self.assertIn("本身从不构成缺陷", read(PREMISE))
        rubric = read(SKILLS / "short-drama-review/references/rubric-story-script.md")
        self.assertIn("Never report partial disclosure as a defect", rubric)

    def test_unreliable_declarations_remain_a_legitimate_design(self) -> None:
        self.assertIn("不可靠", read(PREMISE))

    def test_blocking_condition_is_untraceable_widening(self) -> None:
        self.assertIn("追溯不到即为", read(PREMISE))


class DeliverySurfaceTests(unittest.TestCase):
    """SHT-15 must stay inactive rather than fall back to a guessed safe frame."""

    def test_undeclared_surface_leaves_the_rule_inactive(self) -> None:
        text = read(BLOCKING)
        self.assertIn("没有声明就没有这条约束", text)
        self.assertIn("不因为猜测的区域改变构图", text)

    def test_no_default_occupied_region_is_assumed(self) -> None:
        text = read(BLOCKING)
        self.assertNotIn("上下两端与一侧边缘可能被占用", text)

    def test_declaration_shape_supports_exact_citation(self) -> None:
        text = read(BLOCKING)
        for concept in ("overlay_regions", "permanence", "source_ref", "unresolved"):
            with self.subTest(concept=concept):
                self.assertIn(concept, text)


class TextOnlyReviewBoundaryTests(unittest.TestCase):
    """VID-14 review wording cannot require inspecting rendered media."""

    def test_music_gate_stops_at_prompt_text_or_authorized_observation(self) -> None:
        gates = read(
            SKILLS / "short-drama-review/references/production-quality-gates.md"
        )
        self.assertIn("不能由本环节判断", gates)
        self.assertIn("unverified", gates)
        rubric = read(SKILLS / "short-drama-review/references/rubric-visual-motion.md")
        self.assertIn("not decidable here", rubric)


class DialogueSplitExampleTests(unittest.TestCase):
    """SCR-09's repaired example must not smuggle the action back into a parenthetical."""

    def test_repaired_example_keeps_visible_action_on_its_own_line(self) -> None:
        text = read(SKILLS / "short-drama-write/references/dialogue-craft.md")
        blocks = re.findall(r"```text\n(.*?)\n```", text, re.DOTALL)
        repaired = [b for b in blocks if b.count("▲") == 1 and "【角色甲】" in b]
        self.assertTrue(repaired, "no repaired dialogue-split example found")
        for block in repaired:
            for line in block.splitlines():
                if line.startswith("▲"):
                    continue
                parenthetical = re.search(r"\(([^)]*)\)", line)
                if parenthetical is None:
                    continue
                for verb in ("摆手", "抬手", "转头", "翻", "递", "推开", "指"):
                    with self.subTest(verb=verb):
                        self.assertNotIn(verb, parenthetical.group(1))


class SelfContainedReferenceTests(unittest.TestCase):
    """References added by this work must not reach into a sibling skill's tree."""

    def test_new_references_carry_no_cross_skill_links(self) -> None:
        for path in (PREMISE, CONTAINER_TEMPLATE):
            with self.subTest(path=path.name):
                self.assertNotIn("../../", read(path))


if __name__ == "__main__":
    unittest.main()
