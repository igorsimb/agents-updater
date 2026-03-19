## Highest Priority Formatting Rule (Overrides Other Style Preferences)

- Do not reflow or rewrap existing lines that are <= 120 characters.
- Only wrap when a line exceeds 120 characters.
- If multiple formatting rules conflict, preserve existing wrapping and apply minimal edits.
- Do not introduce extra line breaks for readability/style if line length is <= 120.
- Keep `if` conditions in one line when they fit within 120 characters.
- Avoid multi-line walrus layouts unless the single-line variant exceeds 120 characters.
- Prefer readable alternatives over wrapped walrus forms (assign first, then `if`) when that keeps lines <= 120.
- Keep function signature in one line if possible, e.g. 
`def validate_sql(query: str, tool_runtime: ToolRuntime) -> Command | dict[str, object]:`

Examples:
- Good (single-line fits):
  `if allowlist_check_error := check_allowlist(table_name_normalization_error):`
- Good (assignment then if):
  `allowlist_check_error = check_allowlist(table_name_normalization_error)`
  `if allowlist_check_error:`
- Bad (unnecessary wrapping while <= 120):
  ```
  if (
      allowlist_check_error
      := check_allowlist(table_name_normalization_error)
  ):
  ```

## Virtual Environment
- use existing .venv to execute related commands, e.g. `".venv/Scripts/python.exe" -m pytest`

## 1. Think Before Coding

**Don't assume. Don't hide confusion. Surface tradeoffs.**

Before implementing:
- State how you will verify the change before writing code (test command, browser check, script, etc.).
- Write the verification step first when possible (for example, the failing test for a bug fix).
- Implement only after the verification step exists.
- Run verification, read the full result, and keep iterating until it passes.
- State your assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them - don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.

## 2. Simplicity First

**Minimum code that solves the problem. Nothing speculative.**

- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible scenarios.
- If you write 200 lines and it could be 50, rewrite it.

Ask yourself: "Would a senior engineer say this is overcomplicated?" If yes, simplify.

## 3. Surgical Changes

**Touch only what you must. Clean up only your own mess.**

When editing existing code:
- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- If you notice unrelated dead code, mention it - don't delete it.

When your changes create orphans:
- Remove imports/variables/functions that YOUR changes made unused.
- Don't remove pre-existing dead code unless asked.

The test: Every changed line should trace directly to the user's request.

## 4. Goal-Driven Execution

**Define success criteria. Loop until verified.**

Transform tasks into verifiable goals:
- "Add validation" → "Write tests for invalid inputs, then make them pass"
- "Fix the bug" → "Write a test that reproduces it, then make it pass"
- "Refactor X" → "Ensure tests pass before and after"

For multi-step tasks, state a brief plan:
```
1. [Step] → verify: [check]
2. [Step] → verify: [check]
3. [Step] → verify: [check]
```

**When planning larger changes:**
- Prefer phased plans over one-shot plans.
- Make each phase small, concrete, and independently verifiable.
- Write the plan to `docs/plans/<name_of_file>.md`.
- After writing the plan, stop and wait for explicit user approval.
- For larger or multi-session tasks, maintain `docs/plans/progress.md` with completed work,
  next steps, blockers, and verification status.
- When resuming work, read `docs/plans/<name_of_file>.md`, `docs/plans/progress.md`, and recent git
  history before making changes.
- After approval, implement one phase at a time.
- After each phase, stop and wait for user review/approval unless the user explicitly says not to.
- After implementing a phase, send the phase for review if a reviewer subagent is available.
- Apply the review feedback, re-verify, and only then move to the next phase.
- Follow a tight loop: plan from the task spec, build with verification in mind, verify
  by running relevant tests and reading the full output, then fix against the original spec.
- Do not treat re-reading your own code as verification; compare the result against what
  was asked.
- Once the task is complete, ask the user before deleting `docs/plans/progress.md`.

Strong success criteria let you loop independently. Weak criteria ("make it work") require constant clarification.

## Code Style Guidelines

### Line Length
- Prefer a soft line limit of **120 characters**.
- If a line fits within 120 characters, do not wrap it just to create extra line breaks.
- If a line exceeds 120 characters, wrap it sensibly (especially in Markdown lists, long function calls, and long strings).

### Django Conventions (for django-based apps)
- Keep settings in `config/settings.py`.
- Keep URL routing in `config/urls.py` or per-app `urls.py`.
- Prefer class-based views for reusable logic.
- Use Django forms/serializers for validation.
- Keep secrets out of settings; use env vars or `python-dotenv` if added.

### Configuration
- Read environment variables with `os.environ` or `os.getenv`.
- Keep base configuration in settings; override per environment via env vars (for django-based apps).
- Avoid importing settings in models to prevent app loading cycles (for django-based apps).
- Keep database config in `DATABASES` with explicit keys (for django-based apps).

### Docstrings
- Prefer clear docstrings for new helpers and non-trivial functions.
- Include short examples in docstrings when they make behavior or edge cases easier to understand.
- Keep docstrings practical and compact; do not add them to trivial code just for coverage.

## Commit Messages

- Always provide commit messages in Conventional Commits format with scope and body.
- Use this template when user asks for a commit message:
```
<type>(<scope>): <subject>

- <change 1>
- <change 2>

Why: <short reason>
```
- Keep the subject imperative and concise.
- Allowed scopes: function name, file name/path, or thematic scope like `ui`, `ux`, `backend`, `tests`.
- Keep body bullets concise and focused on what changed and why.
