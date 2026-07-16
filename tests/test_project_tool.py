import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


SUITE = Path(__file__).resolve().parents[1]
SCRIPT = SUITE / "skills/short-drama/scripts/project_tool.py"
SPEC = importlib.util.spec_from_file_location("short_drama_project_tool", SCRIPT)
assert SPEC and SPEC.loader
project_tool = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(project_tool)


class ProjectToolTests(unittest.TestCase):
    def test_initializes_minimal_project_without_creative_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "项目 空格"
            result = project_tool.initialize_project(
                root,
                title="复检记录",
                language="zh-CN",
                aspect_ratio="9:16",
                suite_root=SUITE / "skills/short-drama",
            )

            self.assertEqual(result["project"]["title"], "复检记录")
            self.assertTrue((root / "short-drama.json").is_file())
            self.assertTrue((root / ".short-drama/state.json").is_file())
            self.assertFalse((root / "episodes/EP001/screenplay.md").exists())
            self.assertEqual(project_tool.find_project(root / "episodes"), root.resolve())

    def test_rerun_never_overwrites_existing_project(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "project"
            project_tool.initialize_project(
                root,
                title="原题",
                language="zh-CN",
                aspect_ratio="9:16",
                suite_root=SUITE / "skills/short-drama",
            )
            before = (root / "short-drama.json").read_bytes()

            with self.assertRaises(FileExistsError):
                project_tool.initialize_project(
                    root,
                    title="覆盖题",
                    language="en-US",
                    aspect_ratio="16:9",
                    suite_root=SUITE / "skills/short-drama",
                )

            self.assertEqual((root / "short-drama.json").read_bytes(), before)

    def test_status_exposes_summary_not_creative_text(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "project"
            project_tool.initialize_project(
                root,
                title="档案室",
                language="zh-CN",
                aspect_ratio="9:16",
                suite_root=SUITE / "skills/short-drama",
            )
            state_path = root / ".short-drama/state.json"
            state = json.loads(state_path.read_text(encoding="utf-8"))
            state["artifacts"] = {
                "screenplay": {"build_state": "materialized", "hash": "secret-hash"}
            }
            state_path.write_text(json.dumps(state), encoding="utf-8")

            status = project_tool.project_status(root)

            self.assertEqual(status["artifact_build_states"], {"materialized": 1})
            self.assertNotIn("hash", status)

    def test_lifecycle_axes_are_independent_and_strictly_validated(self) -> None:
        axes = project_tool.default_lifecycle()
        self.assertEqual(
            set(axes),
            {
                "build_state",
                "validation_state",
                "creator_acceptance",
                "independent_review",
                "delivery_gate",
            },
        )

        updated = project_tool.apply_lifecycle_changes(
            axes,
            {"creator_acceptance": "accepted"},
        )
        self.assertEqual(updated["creator_acceptance"], "accepted")
        self.assertEqual(updated["build_state"], "absent")
        with self.assertRaises(ValueError):
            project_tool.apply_lifecycle_changes(axes, {"accepted": True})
        with self.assertRaises(ValueError):
            project_tool.apply_lifecycle_changes(
                axes,
                {"delivery_gate": "accepted"},
            )

    def test_status_summarizes_all_axes_and_recovery_without_hashes_or_text(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "project"
            project_tool.initialize_project(
                root,
                title="夜班审计",
                language="zh-CN",
                aspect_ratio="9:16",
                suite_root=SUITE / "skills/short-drama",
            )
            state_path = root / ".short-drama/state.json"
            state = json.loads(state_path.read_text(encoding="utf-8"))
            state["artifacts"] = {
                "screenplay": {
                    **project_tool.default_lifecycle(),
                    "build_state": "materialized",
                    "creator_acceptance": "accepted",
                    "creative_text": "不得出现在状态摘要里的台词",
                    "accepted_targets": {"episodes/EP001/screenplay.md": "abc"},
                }
            }
            project_tool.atomic_json(state_path, state)

            status = project_tool.project_status(root)

            self.assertEqual(status["artifact_build_states"], {"materialized": 1})
            self.assertEqual(
                status["lifecycle"]["creator_acceptance"], {"accepted": 1}
            )
            serialized = json.dumps(status, ensure_ascii=False)
            self.assertNotIn("台词", serialized)
            self.assertNotIn("abc", serialized)


if __name__ == "__main__":
    unittest.main()
