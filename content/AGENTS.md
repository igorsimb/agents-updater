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
- Keep business rules close to the code that owns them, make dependencies and side effects explicit, and choose
  structures that make expected changes easy to understand and test.
- Use judgment about verification. Run the narrowest useful check, broaden it when the change warrants it, and fix
  relevant failures before handing off. Do not repeat checks that add no confidence.
- Keep comments for non-obvious intent, constraints, or trade-offs. Do not add comments that restate the code.

## Editing conventions

- Preserve public behavior unless the request changes it.
- Keep new or changed lines near 120 characters and do not reflow unrelated text.
- Use regular hyphens (`-`), never em dashes.
- In Python, prefer clear control flow, precise exceptions, and PEP 604 unions where the project uses annotations.
- Write Python module-level docstrings for readers unfamiliar with the file. Start with a plain-language sentence
  explaining what the module does and why it exists. When useful, follow with a short paragraph explaining its
  responsibilities and how it fits into the surrounding workflow.
- Prefer concrete verbs and familiar language over compressed technical labels in module docstrings. For example,
  prefer "Collect supplier names for the brand/article pairs in a production run." over "Fixed canonical evidence
  query with one HTTP attempt and production-only bounds."
- Include module boundaries or constraints only when they help readers understand the module. Keep simple modules
  brief; add detail when responsibilities warrant it. Do not repeat imports, list every function, restate obvious
  code, or include temporary implementation-phase notes. Keep docstrings accurate when behavior changes.
- Apply this docstring convention to new Python modules and modules substantially changed during a task. Do not
  rewrite unrelated files solely to add docstrings.
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
- When the user asks for a commit message after the requested work is complete, use a Conventional Commit
  subject and body and explain the change briefly. Automatically suggest a Conventional Commit message only when the 
  entire user-requested task is complete and the task changed repository files. If any planned phase or required
  work remains, omit the commit message from intermediate responses, even when the current phase changed files.
