# agents-updater

Small dependency-free CLI tool that keeps your global OpenCode and Codex configurations synchronized with canonical
content stored in GitHub.

## What it does

Run `agents-update` to update all managed OpenCode and Codex content:

- download the shared canonical `AGENTS.md` and `skills/` directory
- download each selected platform's native agents
- compare each file with its global counterpart
- create or overwrite files only when content differs
- preserve global agents and skills that are not managed by this repository
- print grouped per-platform results and a summary

Shared content lives in `content/`. Native agent definitions live under `agents/` by platform:

```text
content/
  AGENTS.md
  skills/
agents/
  codex/
  opencode/
```

Update `content/AGENTS.md` or a skill under `content/skills/` once. The command writes that shared content to every
selected platform. Agent definitions stay separate because OpenCode uses Markdown with YAML frontmatter while Codex
uses TOML.

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

Example output:

```text
Codex -> C:\Users\you\.codex
  [updated] AGENTS.md
  [updated] agents: docs-writer, reviewer, tester
  [updated] skills: clean-code, grill-me, langchain-docs

OpenCode -> C:\Users\you\.config\opencode
  [updated] AGENTS.md
  [updated] agents: docs-writer, reviewer, tester
  [updated] skills: clean-code, grill-me, langchain-docs

14 updated, 0 current.
```

A skill or agent is reported as updated when at least one managed file inside it changed.

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

### How do I update a skill for all platforms?

Edit the single canonical copy under `content/skills/<skill-name>/`. After publishing the change to the canonical
repository's `main` branch, run:

```bash
agents-update --skills
```

Because no platform flag is provided, the command writes the shared skill to every supported platform.

### How do I update agents for all platforms?

Agents use platform-specific formats, so update each native definition separately. For example, update both
`agents/opencode/reviewer.md` and `agents/codex/reviewer.toml`. After publishing the changes to the canonical
repository's `main` branch, run:

```bash
agents-update --agents
```

Because no platform flag is provided, the command updates native agents for every supported platform.

### Can I still have a project-level `AGENTS.md`?

Yes. Both tools support global and project instructions:

- global rules in `~/.config/opencode/AGENTS.md` for OpenCode or `~/.codex/AGENTS.md` for Codex
- project rules in `AGENTS.md` at the project root

Project-level rules take priority over the global file when they conflict. The global file still applies as the default
baseline, and the project file adds more specific instructions for that repository.
