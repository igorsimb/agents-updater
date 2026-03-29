# agents-updater

Small dependency-free CLI tool that keeps your global OpenCode `AGENTS.md` file synchronized with a canonical version stored in GitHub.

## What it does

Run `agents-update` to:

- download the canonical `AGENTS.md`
- compare it with `~/.config/opencode/AGENTS.md`
- create or overwrite the global file only when content differs
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

## Uninstalling

Uninstall with pip:

```bash
pip uninstall agents-updater
```

Uninstall using uv:

```bash
uv pip uninstall agents-updater
```

## Usage

From anywhere:

```bash
agents-update
```

The command downloads the canonical `AGENTS.md`, updates `~/.config/opencode/AGENTS.md` if needed, and prints either:

- `AGENTS.md updated`
- `AGENTS.md already up to date`

## FAQ

### Can I still have a project-level `AGENTS.md`?

Yes. OpenCode supports both:

- global rules in `~/.config/opencode/AGENTS.md`
- project rules in `AGENTS.md` at the project root

Project-level rules take priority over the global file when they conflict. The global file still applies as the default baseline, and the project file adds more specific instructions for that repository.
