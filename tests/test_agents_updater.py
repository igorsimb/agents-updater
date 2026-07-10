from __future__ import annotations

import io
import json
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path, PurePosixPath
from unittest.mock import patch

import agents_updater


class ParseArgsTests(unittest.TestCase):
    def test_defaults_to_all_scopes(self) -> None:
        self.assertEqual(agents_updater.parse_args([]), agents_updater.ALL_SCOPES)

    def test_selects_requested_scopes(self) -> None:
        self.assertEqual(
            agents_updater.parse_args(["--agents", "--skills"]),
            frozenset((agents_updater.AGENTS, agents_updater.SKILLS)),
        )

    def test_rejects_all_with_specific_scope(self) -> None:
        with redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit):
                agents_updater.parse_args(["--all", "--agents"])


class UpdateSelectedScopesTests(unittest.TestCase):
    def test_discovers_only_selected_directory_files(self) -> None:
        manifest = {
            "tree": [
                {"type": "blob", "path": "opencode/agents/tester.md"},
                {"type": "blob", "path": "opencode/skills/clean-code/SKILL.md"},
                {"type": "blob", "path": "README.md"},
            ]
        }
        with patch.object(agents_updater, "fetch_url", return_value=json.dumps(manifest)):
            paths = agents_updater.fetch_directory_files(frozenset((agents_updater.AGENTS,)))

        self.assertEqual(paths, [PurePosixPath("opencode", "agents", "tester.md")])

    def test_updates_selected_files_in_global_opencode_directory(self) -> None:
        source_paths = [
            PurePosixPath("opencode", "AGENTS.md"),
            PurePosixPath("opencode", "agents", "tester.md"),
            PurePosixPath("opencode", "skills", "clean-code", "SKILL.md"),
        ]

        with tempfile.TemporaryDirectory() as directory:
            global_path = Path(directory)
            with (
                patch.object(agents_updater, "get_source_files", return_value=source_paths),
                patch.object(
                    agents_updater,
                    "fetch_remote_file",
                    side_effect=("instructions", "agent", "skill"),
                ),
                patch.object(agents_updater, "get_global_opencode_path", return_value=global_path),
            ):
                output = io.StringIO()
                with redirect_stdout(output):
                    agents_updater.update_selected_scopes(agents_updater.ALL_SCOPES)

            self.assertEqual((global_path / "AGENTS.md").read_text(encoding="utf-8"), "instructions")
            self.assertEqual((global_path / "agents" / "tester.md").read_text(encoding="utf-8"), "agent")
            self.assertEqual(
                (global_path / "skills" / "clean-code" / "SKILL.md").read_text(encoding="utf-8"), "skill"
            )
            self.assertIn("Summary: 3 updated, 0 already up to date.", output.getvalue())

    def test_download_failure_does_not_update_any_file(self) -> None:
        source_paths = [
            PurePosixPath("opencode", "AGENTS.md"),
            PurePosixPath("opencode", "agents", "tester.md"),
        ]

        with tempfile.TemporaryDirectory() as directory:
            global_path = Path(directory)
            agents_path = global_path / "AGENTS.md"
            agents_path.write_text("existing instructions", encoding="utf-8")
            with (
                patch.object(agents_updater, "get_source_files", return_value=source_paths),
                patch.object(
                    agents_updater,
                    "fetch_remote_file",
                    side_effect=("new instructions", RuntimeError("download failed")),
                ),
                patch.object(agents_updater, "get_global_opencode_path", return_value=global_path),
            ):
                with self.assertRaisesRegex(RuntimeError, "download failed"):
                    agents_updater.update_selected_scopes(agents_updater.ALL_SCOPES)

            self.assertEqual(agents_path.read_text(encoding="utf-8"), "existing instructions")

    def test_does_not_rewrite_current_file(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            local_path = Path(directory) / "AGENTS.md"
            local_path.write_text("instructions", encoding="utf-8")
            output = io.StringIO()

            with redirect_stdout(output):
                updated = agents_updater.update_file(local_path, "instructions", "AGENTS.md")

            self.assertFalse(updated)
            self.assertIn("already up to date", output.getvalue())


if __name__ == "__main__":
    unittest.main()
