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
CONTENT_DIRECTORY = "content"
AGENTS_MD = "agents_md"
AGENTS = "agents"
SKILLS = "skills"
ALL_SCOPES = frozenset((AGENTS_MD, AGENTS, SKILLS))
DIRECTORY_SCOPES = frozenset((AGENTS, SKILLS))
PLATFORM_LABELS = {CODEX: "Codex", OPENCODE: "OpenCode"}


def get_global_opencode_path() -> Path:
    return Path.home() / ".config" / "opencode"


def get_global_codex_path() -> Path:
    return Path.home() / ".codex"


def get_global_platform_path(platform: str) -> Path:
    if platform == OPENCODE:
        return get_global_opencode_path()
    if platform == CODEX:
        return get_global_codex_path()
    raise ValueError(f"invalid platform: {platform}")


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

    source_directories = set()
    if SKILLS in scopes:
        source_directories.add(PurePosixPath(CONTENT_DIRECTORY, SKILLS))
    if AGENTS in scopes:
        source_directories.update(PurePosixPath(AGENTS, platform) for platform in platforms)

    paths = []
    for entry in entries:
        if entry.get("type") != "blob":
            continue

        path = PurePosixPath(entry["path"])
        if any(source_directory in path.parents for source_directory in source_directories):
            paths.append(path)

    return sorted(paths)


def get_source_files(scopes: frozenset[str], platforms: frozenset[str]) -> list[PurePosixPath]:
    paths = []
    if AGENTS_MD in scopes:
        paths.append(PurePosixPath(CONTENT_DIRECTORY, "AGENTS.md"))
    paths.extend(fetch_directory_files(scopes, platforms))
    return paths


def get_destinations(source_path: PurePosixPath, platforms: frozenset[str]) -> list[tuple[str, Path]]:
    source_root = source_path.parts[0] if source_path.parts else None
    if source_root == CONTENT_DIRECTORY:
        try:
            relative_path = source_path.relative_to(CONTENT_DIRECTORY)
        except ValueError as exc:
            raise ValueError(f"invalid source path: {source_path}") from exc
        return [
            (platform, get_global_platform_path(platform).joinpath(*relative_path.parts))
            for platform in sorted(platforms)
        ]

    if source_root != AGENTS or len(source_path.parts) < 3:
        raise ValueError(f"invalid source path: {source_path}")

    platform = source_path.parts[1]
    if platform not in ALL_PLATFORMS:
        raise ValueError(f"invalid source path: {source_path}")

    try:
        relative_path = source_path.relative_to(PurePosixPath(AGENTS, platform))
    except ValueError as exc:
        raise ValueError(f"invalid source path: {source_path}") from exc
    return [(platform, get_global_platform_path(platform).joinpath(AGENTS, *relative_path.parts))]


def get_source_item(source_path: PurePosixPath) -> tuple[str, str]:
    if source_path == PurePosixPath(CONTENT_DIRECTORY, "AGENTS.md"):
        return AGENTS_MD, "AGENTS.md"

    if len(source_path.parts) >= 3 and source_path.parts[:2] == (CONTENT_DIRECTORY, SKILLS):
        return SKILLS, source_path.parts[2]

    if len(source_path.parts) >= 3 and source_path.parts[0] == AGENTS:
        relative_path = source_path.relative_to(PurePosixPath(AGENTS, source_path.parts[1]))
        name = relative_path.parts[0]
        return AGENTS, PurePosixPath(name).stem if len(relative_path.parts) == 1 else name

    raise ValueError(f"invalid source path: {source_path}")


def update_file(local_path: Path, remote_content: str) -> bool:
    local_path.parent.mkdir(parents=True, exist_ok=True)
    local_content = local_path.read_text(encoding="utf-8") if local_path.exists() else None

    if local_content == remote_content:
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

    return True


def print_update_results(results: dict[str, dict[str, dict[str, bool]]], platforms: frozenset[str]) -> None:
    updated_count = 0
    current_count = 0

    for platform in sorted(platforms):
        print(f"{PLATFORM_LABELS[platform]} -> {get_global_platform_path(platform)}")
        for scope in (AGENTS_MD, AGENTS, SKILLS):
            items = results[platform].get(scope, {})
            for updated in (True, False):
                names = sorted(name for name, was_updated in items.items() if was_updated == updated)
                if not names:
                    continue

                status = "updated" if updated else "current"
                label = f"{scope}: " if scope != AGENTS_MD else ""
                print(f"  [{status}] {label}{', '.join(names)}")
                if updated:
                    updated_count += len(names)
                else:
                    current_count += len(names)
        print()

    print(f"{updated_count} updated, {current_count} current.")


def update_selected_scopes(scopes: frozenset[str], platforms: frozenset[str]) -> None:
    source_paths = get_source_files(scopes, platforms)
    downloaded_files = [(path, fetch_remote_file(str(path))) for path in source_paths]
    results: dict[str, dict[str, dict[str, bool]]] = {platform: {} for platform in platforms}

    for source_path, content in downloaded_files:
        scope, name = get_source_item(source_path)
        for platform, destination_path in get_destinations(source_path, platforms):
            updated = update_file(destination_path, content)
            scope_results = results[platform].setdefault(scope, {})
            scope_results[name] = scope_results.get(name, False) or updated

    print_update_results(results, platforms)


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
