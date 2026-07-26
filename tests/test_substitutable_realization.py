"""Content-risk guidance is the easiest thing in this suite to get wrong.

Written badly it becomes a topic ban list, or a claim to know standards that
change by platform, region, and year. These tests pin the shape that keeps it
useful: separate the dramatic function from the depiction, demand a fallback
that still delivers the function, and stay inert until the creator marks a beat.
"""

import json
import re
import unittest
from pathlib import Path

SUITE = Path(__file__).resolve().parents[1]
SKILLS = SUITE / "skills"
REFERENCE = SKILLS / "short-drama-write/references/substitutable-realization.md"
BEATS = SKILLS / "short-drama-write/assets/beats.jsonl"
CONTRACT = SKILLS / "short-drama-write/references/stage-contract.md"
RUBRIC = SKILLS / "short-drama-review/references/rubric-story-script.md"
WRITE_SKILL = SKILLS / "short-drama-write/SKILL.md"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def unwrapped(path: Path) -> str:
    return read(path).replace("\n", "")


class RuleRegistrationTests(unittest.TestCase):
    def test_the_rule_is_owned_by_the_stage_that_writes_the_depiction(self) -> None:
        row = re.search(r"^\| SCR-10 \| ([a-z_]+) \|", read(CONTRACT), re.MULTILINE)
        self.assertIsNotNone(row)
        assert row is not None
        self.assertEqual(row.group(1), "reviewed_invariant")

    def test_the_reference_is_reachable_from_the_owning_skill(self) -> None:
        self.assertIn("references/substitutable-realization.md", read(WRITE_SKILL))

    def test_the_reference_stays_inside_its_own_skill_tree(self) -> None:
        self.assertNotIn("../../", read(REFERENCE))


class NotAPlatformStandardTests(unittest.TestCase):
    def test_the_suite_disclaims_carrying_any_platform_standard(self) -> None:
        text = unwrapped(REFERENCE)
        self.assertIn("不内置任何平台的审核标准", text)
        self.assertIn("不给出题材禁令", text)

    def test_the_rule_is_inert_until_the_creator_marks_a_beat(self) -> None:
        """An always-on version would make the suite guess at standards it does
        not have, which is exactly what it must not do."""

        self.assertIn("未标注时本节不生效", unwrapped(REFERENCE))
        self.assertIn("An unmarked beat leaves the rule inactive", read(CONTRACT))
        self.assertIn("An unmarked beat leaves this section", read(RUBRIC))

    def test_no_topic_ban_list_slipped_into_the_guidance(self) -> None:
        """The guidance selects by mechanism. A list of subject matter would date
        instantly and would refuse work the creator is entitled to make."""

        text = read(REFERENCE)
        for banned_shape in ("禁止出现", "不得包含", "敏感词", "违禁"):
            with self.subTest(shape=banned_shape):
                self.assertNotIn(banned_shape, text)

    def test_pre_emptive_sanding_is_named_as_the_costlier_mistake(self) -> None:
        self.assertIn("提前自我阉割", unwrapped(REFERENCE))
        self.assertIn("Report pre-emptive sanding as a finding", read(RUBRIC))
        self.assertIn("不要因此提前磨平任何内容", unwrapped(WRITE_SKILL))


class FallbackEquivalenceTests(unittest.TestCase):
    def test_function_depiction_and_fallback_are_separate_fields(self) -> None:
        record = json.loads(read(BEATS).strip())
        marked = record["replaceable_realization"]
        for key in (
            "marked_by",
            "dramatic_function",
            "current_depiction",
            "fallback_depiction",
            "cost_preserved",
            "downstream_still_satisfied",
        ):
            with self.subTest(key=key):
                self.assertIn(key, marked)

    def test_deleting_the_beat_is_refused_as_a_fallback(self) -> None:
        """Deletion removes the function, which is the one thing a fallback must
        preserve; without this the rule collapses into 'cut it'."""

        self.assertIn("「删掉这场」永远不是备选", unwrapped(REFERENCE))
        self.assertIn("Deleting the beat is never a fallback", read(CONTRACT))

    def test_equivalence_is_judged_against_downstream_dependencies(self) -> None:
        text = unwrapped(REFERENCE)
        self.assertIn("payoff_refs", text)
        self.assertIn("下一集的进入状态", text)

    def test_a_weaker_version_is_not_accepted_as_a_fallback(self) -> None:
        text = unwrapped(REFERENCE)
        self.assertIn("这是削弱不是替换", text)
        self.assertIn("代价没有消失", text)



class DecisionAuthorityTests(unittest.TestCase):
    """`decided_by` carries the whole authority model; an undefined field lets a
    skill quietly record itself as the decider."""

    WORKFLOW = SKILLS / "short-drama/references/creator-workflow.md"
    OWNERSHIP = SKILLS / "short-drama/references/contract-and-ownership.md"

    def test_a_skill_or_agent_can_never_be_the_decider(self) -> None:
        text = read(self.WORKFLOW)
        self.assertIn("An assistant, an agent, an owning skill, or a reviewer is", text)
        self.assertIn("never", text)
        self.assertIn("decided_by", read(self.OWNERSHIP))

    def test_a_delegate_needs_a_prior_creator_authorization(self) -> None:
        text = read(self.WORKFLOW)
        self.assertIn("cannot widen their own scope", text)
        self.assertIn("a delegate cannot supersede the creator", text)

    def test_no_shipped_path_still_prescribes_the_single_decisions_file(self) -> None:
        """The append-only layout silently invalidates every earlier acceptance,
        so it must not survive as an example anyone would copy."""

        offenders: list[str] = []
        for path in sorted(SKILLS.rglob("*")):
            if not path.is_file() or path.suffix not in {".md", ".json", ".jsonl"}:
                continue
            for line in read(path).splitlines():
                if "creator-decisions.jsonl" not in line:
                    continue
                # The lifecycle reference explains why the old layout is wrong.
                if "接受第二集会改变" in line:
                    continue
                offenders.append(f"{path.relative_to(SUITE)}: {line.strip()[:70]}")
        self.assertEqual(offenders, [], "\n".join(offenders))

if __name__ == "__main__":
    unittest.main()
