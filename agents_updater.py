from __future__ import annotations

import sys
import tempfile
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import urlopen

SOURCE_URL = "https://raw.githubusercontent.com/igorsimb/agents-updater/main/AGENTS.md"


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
    local_path = Path.cwd() / "AGENTS.md"
    remote_content = fetch_remote_agents()
    local_content = (
        local_path.read_text(encoding="utf-8") if local_path.exists() else None
    )

    if local_content == remote_content:
        print("AGENTS.md already up to date")
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

    print("AGENTS.md updated")


def main() -> None:
    try:
        update_agents_file()
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc


if __name__ == "__main__":
    main()
