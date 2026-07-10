# Global OpenCode Instructions

## Priorities And Scope

Apply instructions in this order:

1. Direct user request
2. This file
3. Existing code and test conventions in the touched area
4. General engineering practice

When instructions conflict, follow the higher priority. For an ambiguous request, use the safest reasonable
interpretation and state a material assumption; ask only when the ambiguity changes product behavior or the action is
risky, destructive, expensive to reverse, or cannot be inferred from the repository.

## Authority

For requests to answer, explain, review, diagnose, or plan, inspect relevant materials and report the result. Do not
implement changes unless also asked.

For requests to change, build, or fix, make the requested in-scope local changes and run relevant non-destructive
validation without asking first. Reading files, searching, inspecting logs, editing in-scope code, and running
non-destructive tests are authorized.

Require confirmation before external writes, destructive actions, purchases, or material expansion of scope. Do not undo
unrelated worktree changes.

## Working Method

- Inspect the relevant code path and local conventions before changing code.
- Make the smallest change that meets the requested outcome. Do not add unrequested features, abstractions,
  configuration, or unrelated refactors.
- Preserve public behavior unless the request changes it.
- Prefer deterministic, focused tests over live, API, or LLM tests when they cover the risk.
- Validate the requested behavior at the narrowest useful layer, then broaden checks only when risk warrants it.
- Do not claim a result is verified unless a relevant check passed. State material validation gaps.

For work with several independent steps or meaningful risk, use a brief plan with the intended verification. Do not
create a plan for straightforward edits.

## Editing

- Follow conventions already used in the touched file or module; reuse established helpers and patterns.
- Keep diffs surgical. Avoid incidental formatting churn, symbol renames, moves, or API reshaping unless required.
- Remove code, imports, variables, tests, or comments made unused by the change. Leave unrelated dead code untouched.
- Comment only to explain non-obvious intent, constraints, or tradeoffs.
- Do not reflow existing lines at or under 120 characters. Prefer a soft 120-character limit for new or changed lines.

## Testing And Commands

- Start with the closest relevant test, test file, lint/type check, or focused manual reproduction.
- Test a unit's main observable behavior. Avoid asserting incidental text or formatting such as exact log, docstring, or
  logging-format wording unless that wording is the required public behavior.
- Use the existing virtual environment when present. Prefer `".venv/Scripts/python.exe" -m pytest` on Windows and
  `".venv/bin/python" -m pytest` on POSIX.
- Prefer module execution (`python -m ...`) when appropriate.

## Code Conventions

### Python

- Prefer clear, straightforward control flow over cleverness.
- Add helpers only when they remove real duplication or make the code meaningfully clearer.
- Use PEP 604 unions (`X | Y`, `X | None`) and match existing annotation conventions.
- Handle realistic failures at the appropriate boundary. Prefer precise exceptions and messages over broad catches.
- Add logging only when it aids real operational diagnosis; follow existing logging patterns.

### Frontend

- Reuse the existing UI patterns and components.
- Use dark/light theme-aware utility classes; prefer `bg-body`, `text-body`, and `*-subtle` over fixed colors.
- Keep user-facing UI text in Russian unless the request specifies another language.
- For new interfaces, prioritize clear hierarchy, usable responsive layout, and the product's established visual
  language.

### Django

- Keep settings in `config/settings.py` and routes in `config/urls.py` or per-app `urls.py`.
- Prefer class-based views when they fit existing reusable patterns.
- Use Django forms or serializers for validation where appropriate.
- Keep secrets out of settings. Read environment values with `os.environ` or `os.getenv` and extend the existing
  configuration pattern.
- Avoid importing settings in models. Keep database configuration in `DATABASES` with explicit keys.

### Dependencies

- Prefer the standard library and existing dependencies.
- Add a dependency only when necessary for the request; choose the smallest suitable option and state why.

## Git And Responses

- Do not commit, amend, push, or create pull requests unless explicitly asked.
- When asked for a commit message, use Conventional Commits with a concise imperative subject and a brief body
  explaining the change and why.
- For reviews, lead with findings ordered by severity and file reference. State if no findings were discovered and
  identify material test gaps.
- Lead completed-work reports with the outcome. Include the changed location, verification performed, and only material
  assumptions, caveats, or next actions. Omit generic introductions, repetition, and optional background.
