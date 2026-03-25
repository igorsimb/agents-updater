from __future__ import annotations

import sys
import tempfile
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import urlopen

SOURCE_URL = "https://raw.githubusercontent.com/igorsimb/agents-updater/main/AGENTS.md"


def get_global_agents_path() -> Path:
    return Path.home() / ".config" / "opencode" / "AGENTS.md"


def format_agents_path(path: Path) -> str:
    return str(path)


def fetch_remote_agents() -> str:
    try:
        with urlopen(SOURCE_URL, timeout=15) as response:
            status = getattr(response, "status", 200)
            if status != 200:
                raise RuntimeError(f"failed to download AGENTS.md: HTTP {status}")
            return response.read().decode("utf-8")
    except HTTPError as exc:
        raise RuntimeError(f"failed to download AGENTS.md: HTTP {exc.code}") from exc
    except URLError as exc:
        raise RuntimeError(f"failed to download AGENTS.md: {exc.reason}") from exc


def update_agents_file() -> None:
    local_path = get_global_agents_path()
    local_path.parent.mkdir(parents=True, exist_ok=True)
    remote_content = fetch_remote_agents()
    local_content = (
        local_path.read_text(encoding="utf-8") if local_path.exists() else None
    )
    display_path = format_agents_path(local_path)

    if local_content == remote_content:
        print(f"AGENTS.md already up to date: {display_path}")
        return

    tmp_file: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=local_path.parent,
            delete=False,
            prefix="AGENTS.",
            suffix=".tmp",
        ) as handle:
            handle.write(remote_content)
            tmp_file = Path(handle.name)
        tmp_file.replace(local_path)
    finally:
        if tmp_file is not None and tmp_file.exists():
            tmp_file.unlink()

    print(f"AGENTS.md updated: {display_path}")


def main() -> None:
    try:
        update_agents_file()
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc


if __name__ == "__main__":
    main()
