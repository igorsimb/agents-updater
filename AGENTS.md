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

Strong success criteria let you loop independently. Weak criteria ("make it work") require constant clarification.

## Code Style Guidelines

### Line Length
- Prefer a soft line limit of **120 characters**.
- If a line fits within 120 characters, do not wrap it just to create extra line breaks.
- If a line exceeds 120 characters, wrap it sensibly (especially in Markdown lists, long function calls, and long strings).

### Frontend
- Use Bootstrap utility classes that are dark/light theme aware (avoid fixed
  colors like `bg-white` and prefer `bg-body`, `text-body`, `*-subtle`).
- Keep user-facing UI text in Russian unless explicitly asked otherwise.

### Django Conventions (for django-based apps)
- Keep settings in `config/settings.py`.
- Keep URL routing in `config/urls.py` or per-app `urls.py`.
- Prefer class-based views for reusable logic.
- Use Django forms/serializers for validation.
- Keep secrets out of settings; use env vars or `python-dotenv` if added.

### Configuration
- Read environment variables with `os.environ` or `os.getenv`.
- Keep base configuration in settings; override per environment via env vars.
- Avoid importing settings in models to prevent app loading cycles.
- Keep database config in `DATABASES` with explicit keys.

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
