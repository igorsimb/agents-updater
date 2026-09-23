# Global Agent Instructions

These instructions are the shared baseline for work in projects that install this repository's managed content.

## Scope and authority

- Follow the user's request first. Use these rules to resolve repository-specific ambiguity.
- For changes, carry the work through implementation, useful verification, and fixes for failures caused by the change.
- Reading, searching, editing in scope, and running local non-destructive checks are authorized. Ask before external
  writes, destructive actions, purchases, or material expansion of scope.
- For explanation, review, diagnosis, or planning requests, inspect the evidence and report findings without editing
  unless the user also asks for a change.

## Working method

- Read the code, tests, and documentation needed for the current task. Use referenced documents when their topic is
  relevant; do not load the whole repository by default.
- Make the smallest coherent change that satisfies the request and preserves unrelated behavior.
- Prefer existing patterns and dependencies. Add structure or dependencies only when the task needs them.
- Use judgment about verification. Run the narrowest useful check, broaden it when the change warrants it, and fix
  relevant failures before handing off. Do not repeat checks that add no confidence.
- Keep comments for non-obvious intent, constraints, or trade-offs. Do not add comments that restate the code.

## Editing conventions

- Preserve public behavior unless the request changes it.
- Keep new or changed lines near 120 characters and do not reflow unrelated text.
- Use regular hyphens (`-`), never em dashes.
- In Python, prefer clear control flow, precise exceptions, and PEP 604 unions where the project uses annotations.
- In frontend work, follow existing components and theme-aware utility classes. Keep user-facing UI text in Russian
  unless the request specifies another language.
- In Django work, keep settings and routes in their established modules, read secrets from the environment, and keep
  database configuration explicit.

## Repository source files

- When changing a skill, edit its canonical source under `content/skills/`.
- When changing an agent, edit its canonical definition under `agents/`.
- Change `content/AGENTS.md` for the shared global instructions distributed by this repository.
- Do not edit installed or global copies unless the user explicitly asks for those copies.

## Git and handoff

- Do not commit, amend, push, or create pull requests unless explicitly asked.
- Report the outcome, changed locations, verification performed, and material gaps or assumptions.
- When the user asks for a commit message after the requested work is complete, use a concise Conventional Commit
  subject and explain the change briefly.
