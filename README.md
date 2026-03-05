# agents-updater

Small dependency-free CLI tool that keeps a local `AGENTS.md` file synchronized with a canonical version stored in GitHub.

## What it does

Run `agents-update` inside any repository to:

- download the canonical `AGENTS.md`
- compare it with the local `AGENTS.md`
- create or overwrite the local file only when content differs
- print whether it was updated or already up to date

## Installation

Install with pip directly from GitHub:

```bash
pip install git+https://github.com/igorsimb/agents-updater
```

Install using uv:

```bash
uv pip install git+https://github.com/igorsimb/agents-updater
```

## Usage

From the root of any project:

```bash
agents-update
```

The command downloads the canonical `AGENTS.md`, updates your local file if needed, and prints either:

- `AGENTS.md updated`
- `AGENTS.md already up to date`
