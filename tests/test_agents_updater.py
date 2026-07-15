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
    def test_defaults_to_all_scopes_and_platforms(self) -> None:
        self.assertEqual(agents_updater.parse_args([]), (agents_updater.ALL_SCOPES, agents_updater.ALL_PLATFORMS))

    def test_selects_requested_scopes_for_all_platforms(self) -> None:
        self.assertEqual(
            agents_updater.parse_args(["--agents", "--skills"]),
            (frozenset((agents_updater.AGENTS, agents_updater.SKILLS)), agents_updater.ALL_PLATFORMS),
        )

    def test_selects_requested_platform_with_all_scopes(self) -> None:
        self.assertEqual(
            agents_updater.parse_args(["--codex"]),
            (agents_updater.ALL_SCOPES, frozenset((agents_updater.CODEX,))),
        )

    def test_combines_platform_and_scope_filters(self) -> None:
        self.assertEqual(
            agents_updater.parse_args(["--opencode", "--skills"]),
            (frozenset((agents_updater.SKILLS,)), frozenset((agents_updater.OPENCODE,))),
        )

    def test_combines_all_scopes_with_platform_filter(self) -> None:
        self.assertEqual(
            agents_updater.parse_args(["--codex", "--all"]),
            (agents_updater.ALL_SCOPES, frozenset((agents_updater.CODEX,))),
        )

    def test_rejects_all_with_specific_scope(self) -> None:
        with redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit):
                agents_updater.parse_args(["--all", "--agents"])


class UpdateSelectedScopesTests(unittest.TestCase):
    def test_discovers_only_selected_directory_files(self) -> None:
        manifest = {
            "tree": [
                {"type": "blob", "path": "agents/opencode/tester.md"},
                {"type": "blob", "path": "agents/codex/tester.toml"},
                {"type": "blob", "path": "content/skills/clean-code/SKILL.md"},
                {"type": "blob", "path": "README.md"},
            ]
        }
        with patch.object(agents_updater, "fetch_url", return_value=json.dumps(manifest)):
            paths = agents_updater.fetch_directory_files(
                frozenset((agents_updater.AGENTS,)), frozenset((agents_updater.CODEX,))
            )

        self.assertEqual(paths, [PurePosixPath("agents", "codex", "tester.toml")])

    def test_discovers_shared_skills_once(self) -> None:
        manifest = {
            "tree": [
                {"type": "blob", "path": "content/skills/grill-me/SKILL.md"},
                {"type": "blob", "path": "agents/codex/reviewer.toml"},
            ]
        }
        with patch.object(agents_updater, "fetch_url", return_value=json.dumps(manifest)):
            paths = agents_updater.fetch_directory_files(
                frozenset((agents_updater.SKILLS,)), frozenset((agents_updater.CODEX,))
            )

        self.assertEqual(
            paths,
            [PurePosixPath("content", "skills", "grill-me", "SKILL.md")],
        )

    def test_updates_selected_files_in_platform_directories(self) -> None:
        source_paths = [
            PurePosixPath("content", "AGENTS.md"),
            PurePosixPath("content", "skills", "clean-code", "SKILL.md"),
            PurePosixPath("agents", "opencode", "tester.md"),
            PurePosixPath("agents", "codex", "tester.toml"),
        ]

        with tempfile.TemporaryDirectory() as directory:
            opencode_path = Path(directory) / "opencode"
            codex_path = Path(directory) / "codex"
            with (
                patch.object(agents_updater, "get_source_files", return_value=source_paths),
                patch.object(
                    agents_updater,
                    "fetch_remote_file",
                    side_effect=("instructions", "skill", "opencode agent", "codex agent"),
                ),
                patch.object(agents_updater, "get_global_opencode_path", return_value=opencode_path),
                patch.object(agents_updater, "get_global_codex_path", return_value=codex_path),
            ):
                output = io.StringIO()
                with redirect_stdout(output):
                    agents_updater.update_selected_scopes(agents_updater.ALL_SCOPES, agents_updater.ALL_PLATFORMS)

            self.assertEqual((opencode_path / "AGENTS.md").read_text(encoding="utf-8"), "instructions")
            self.assertEqual(
                (opencode_path / "skills" / "clean-code" / "SKILL.md").read_text(encoding="utf-8"), "skill"
            )
            self.assertEqual((opencode_path / "agents" / "tester.md").read_text(encoding="utf-8"), "opencode agent")
            self.assertEqual((codex_path / "AGENTS.md").read_text(encoding="utf-8"), "instructions")
            self.assertEqual(
                (codex_path / "skills" / "clean-code" / "SKILL.md").read_text(encoding="utf-8"), "skill"
            )
            self.assertEqual((codex_path / "agents" / "tester.toml").read_text(encoding="utf-8"), "codex agent")
            self.assertIn("Summary: 6 updated, 0 already up to date.", output.getvalue())

    def test_download_failure_does_not_update_any_file(self) -> None:
        source_paths = [
            PurePosixPath("content", "AGENTS.md"),
            PurePosixPath("agents", "opencode", "tester.md"),
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
                    agents_updater.update_selected_scopes(
                        agents_updater.ALL_SCOPES, frozenset((agents_updater.OPENCODE,))
                    )

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
