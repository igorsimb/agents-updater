# agents-updater

Small dependency-free CLI tool that keeps your global OpenCode and Codex configurations synchronized with canonical
content stored in GitHub.

## What it does

Run `agents-update` to update all managed OpenCode and Codex content:

- download the canonical `AGENTS.md`
- download the canonical `agents/` and `skills/` directories
- compare each file with its global counterpart
- create or overwrite files only when content differs
- preserve global agents and skills that are not managed by this repository
- print per-file results and a summary

The canonical payload lives in this repository's `opencode/` and `codex/` directories:

```text
opencode/
  AGENTS.md
  agents/
  skills/
codex/
  AGENTS.md
  agents/
  skills/
```

## Installation

Install with pip directly from GitHub:

```bash
pip install git+https://github.com/igorsimb/agents-updater
```

Upgrade an existing installation with pip:

```bash
pip install --upgrade git+https://github.com/igorsimb/agents-updater
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

The command updates all of the following by default:

- `~/.config/opencode/AGENTS.md`
- `~/.config/opencode/agents/`
- `~/.config/opencode/skills/`
- `~/.codex/AGENTS.md`
- `~/.codex/agents/`
- `~/.codex/skills/`

Select one or both platforms when needed:

```bash
agents-update --opencode
agents-update --codex
agents-update --opencode --codex
```

Select one or more content types when needed:

```bash
agents-update --agents-md
agents-update --agents
agents-update --skills
agents-update --agents --skills
agents-update --all
```

Platform and content-type filters can be combined:

```bash
agents-update --codex --agents
agents-update --opencode --skills
agents-update --codex --all
```

Without a platform flag, selected content types are updated for both platforms. Without a content-type flag, all
content types are updated for the selected platforms. `--all` explicitly selects all content types and cannot be
combined with `--agents-md`, `--agents`, or `--skills`.

The update is additive: files managed by this repository are updated, but global agents and skills not present in this
repository are not deleted.

## FAQ

### Can I still have a project-level `AGENTS.md`?

Yes. Both tools support global and project instructions:

- global rules in `~/.config/opencode/AGENTS.md` for OpenCode or `~/.codex/AGENTS.md` for Codex
- project rules in `AGENTS.md` at the project root

Project-level rules take priority over the global file when they conflict. The global file still applies as the default
baseline, and the project file adds more specific instructions for that repository.
