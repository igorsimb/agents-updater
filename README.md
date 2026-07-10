# agents-updater

Small dependency-free CLI tool that keeps your global OpenCode configuration synchronized with canonical content stored in
GitHub.

## What it does

Run `agents-update` to update all managed OpenCode content:

- download the canonical `AGENTS.md`
- download the canonical `agents/` and `skills/` directories
- compare each file with its global counterpart
- create or overwrite files only when content differs
- preserve global agents and skills that are not managed by this repository
- print per-file results and a summary

The canonical payload lives in this repository's `opencode/` directory:

```text
opencode/
  AGENTS.md
  agents/
  skills/
```

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

The command updates all of the following by default:

- `~/.config/opencode/AGENTS.md`
- `~/.config/opencode/agents/`
- `~/.config/opencode/skills/`

Select one or more targets when needed:

```bash
agents-update --agents-md
agents-update --agents
agents-update --skills
agents-update --agents --skills
agents-update --all
```

`--all` is equivalent to running `agents-update` with no scope flags. It cannot be combined with a specific scope flag.

The update is additive: files managed by this repository are updated, but global agents and skills not present in this
repository are not deleted.

## FAQ

### Can I still have a project-level `AGENTS.md`?

Yes. OpenCode supports both:

- global rules in `~/.config/opencode/AGENTS.md`
- project rules in `AGENTS.md` at the project root

Project-level rules take priority over the global file when they conflict. The global file still applies as the default baseline, and the project file adds more specific instructions for that repository.
