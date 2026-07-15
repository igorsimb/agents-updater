from __future__ import annotations

import argparse
import json
import sys
import tempfile
from pathlib import Path, PurePosixPath
from urllib.error import HTTPError, URLError
from urllib.request import urlopen

REPOSITORY_URL = "https://github.com/igorsimb/agents-updater"
RAW_SOURCE_URL = "https://raw.githubusercontent.com/igorsimb/agents-updater/main"
TREE_SOURCE_URL = "https://api.github.com/repos/igorsimb/agents-updater/git/trees/main?recursive=1"
OPENCODE = "opencode"
CODEX = "codex"
ALL_PLATFORMS = frozenset((OPENCODE, CODEX))
AGENTS_MD = "agents_md"
AGENTS = "agents"
SKILLS = "skills"
ALL_SCOPES = frozenset((AGENTS_MD, AGENTS, SKILLS))
DIRECTORY_SCOPES = frozenset((AGENTS, SKILLS))


def get_global_opencode_path() -> Path:
    return Path.home() / ".config" / "opencode"


def get_global_codex_path() -> Path:
    return Path.home() / ".codex"


def fetch_url(url: str, description: str) -> str:
    try:
        with urlopen(url, timeout=15) as response:
            status = getattr(response, "status", 200)
            if status != 200:
                raise RuntimeError(f"failed to download {description}: HTTP {status}")
            return response.read().decode("utf-8")
    except HTTPError as exc:
        raise RuntimeError(f"failed to download {description}: HTTP {exc.code}") from exc
    except URLError as exc:
        raise RuntimeError(f"failed to download {description}: {exc.reason}") from exc


def fetch_remote_file(source_path: str) -> str:
    return fetch_url(f"{RAW_SOURCE_URL}/{source_path}", source_path)


def fetch_directory_files(scopes: frozenset[str], platforms: frozenset[str]) -> list[PurePosixPath]:
    if not scopes.intersection(DIRECTORY_SCOPES):
        return []

    try:
        source_tree = json.loads(fetch_url(TREE_SOURCE_URL, "source manifest"))
        entries = source_tree["tree"]
    except (json.JSONDecodeError, KeyError, TypeError) as exc:
        raise RuntimeError("failed to read source manifest") from exc

    paths = []
    for entry in entries:
        if entry.get("type") != "blob":
            continue

        path = PurePosixPath(entry["path"])
        for platform in platforms:
            for scope in scopes.intersection(DIRECTORY_SCOPES):
                scope_path = PurePosixPath(platform, scope)
                if scope_path in path.parents:
                    paths.append(path)
                    break

    return sorted(paths)


def get_source_files(scopes: frozenset[str], platforms: frozenset[str]) -> list[PurePosixPath]:
    paths = []
    if AGENTS_MD in scopes:
        paths.extend(PurePosixPath(platform, "AGENTS.md") for platform in sorted(platforms))
    paths.extend(fetch_directory_files(scopes, platforms))
    return paths


def get_destination_path(source_path: PurePosixPath) -> Path:
    platform = source_path.parts[0] if source_path.parts else None
    if platform not in ALL_PLATFORMS:
        raise ValueError(f"invalid source path: {source_path}")

    try:
        relative_path = source_path.relative_to(platform)
    except ValueError as exc:
        raise ValueError(f"invalid source path: {source_path}") from exc

    global_path = get_global_opencode_path() if platform == OPENCODE else get_global_codex_path()
    return global_path.joinpath(*relative_path.parts)


def update_file(local_path: Path, remote_content: str, label: str) -> bool:
    local_path.parent.mkdir(parents=True, exist_ok=True)
    local_content = local_path.read_text(encoding="utf-8") if local_path.exists() else None

    if local_content == remote_content:
        print(f"{label} already up to date: {local_path}")
        return False

    tmp_file = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=local_path.parent,
            delete=False,
            prefix=f"{local_path.name}.",
            suffix=".tmp",
        ) as handle:
            handle.write(remote_content)
            tmp_file = Path(handle.name)
        tmp_file.replace(local_path)
    finally:
        if tmp_file is not None and tmp_file.exists():
            tmp_file.unlink()

    print(f"{label} updated: {local_path}")
    return True


def update_selected_scopes(scopes: frozenset[str], platforms: frozenset[str]) -> None:
    source_paths = get_source_files(scopes, platforms)
    downloaded_files = [(path, fetch_remote_file(str(path))) for path in source_paths]
    updated_count = 0

    for source_path, content in downloaded_files:
        if update_file(get_destination_path(source_path), content, str(source_path)):
            updated_count += 1

    current_count = len(downloaded_files) - updated_count
    print(f"Summary: {updated_count} updated, {current_count} already up to date.")


def parse_args(argv: list[str] | None = None) -> tuple[frozenset[str], frozenset[str]]:
    parser = argparse.ArgumentParser(
        description="Update global OpenCode and Codex instructions, agents, and skills from the canonical repository."
    )
    parser.add_argument("--opencode", action="store_true", help="Update only OpenCode content.")
    parser.add_argument("--codex", action="store_true", help="Update only Codex content.")
    parser.add_argument("--agents-md", action="store_true", help="Update only AGENTS.md.")
    parser.add_argument("--agents", action="store_true", help="Update only global agents.")
    parser.add_argument("--skills", action="store_true", help="Update only global skills.")
    parser.add_argument("--all", action="store_true", help="Update all managed content (the default).")
    args = parser.parse_args(argv)

    selected_scopes = frozenset(
        scope
        for scope, selected in ((AGENTS_MD, args.agents_md), (AGENTS, args.agents), (SKILLS, args.skills))
        if selected
    )
    if args.all and selected_scopes:
        parser.error("--all cannot be combined with --agents-md, --agents, or --skills")

    selected_platforms = frozenset(
        platform for platform, selected in ((OPENCODE, args.opencode), (CODEX, args.codex)) if selected
    )
    scopes = ALL_SCOPES if args.all or not selected_scopes else selected_scopes
    platforms = selected_platforms or ALL_PLATFORMS
    return scopes, platforms


def main(argv: list[str] | None = None) -> None:
    try:
        scopes, platforms = parse_args(argv)
        update_selected_scopes(scopes, platforms)
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc


if __name__ == "__main__":
    main()
