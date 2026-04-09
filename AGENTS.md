## Instruction Priority

Apply instructions in this order:

1. Direct user request
2. Repository-specific constraints in this file
3. Existing local code/style patterns in the touched area
4. General engineering best practices

If instructions conflict, follow the higher-priority item and make the smallest reasonable change.

---

## Core Operating Principles

### Think before coding

- Do not assume unclear requirements silently.
- State important assumptions explicitly.
- If there are multiple reasonable interpretations, call them out briefly and choose the safest one unless the decision is product-defining.
- Push back on unnecessary complexity, speculative features, and unrequested abstractions.
- Prefer progress over paralysis: if the request is mostly clear, proceed and note assumptions instead of blocking.

### Simplicity first

- Write the minimum code needed to solve the actual problem.
- Do not add features, options, abstractions, or configurability that were not requested.
- Avoid indirection for single-use logic.
- Avoid handling impossible or unsupported scenarios unless they are already part of the surrounding code path.
- When in doubt, choose the solution a senior engineer would consider boring, obvious, and maintainable.

### Surgical changes

- Change only what is required for the task.
- Do not refactor unrelated code.
- Do not "clean up" adjacent code unless your change requires it.
- Match the existing style and structure in the touched area unless the user asked for a broader cleanup.
- Remove imports, variables, functions, tests, or comments that your change made unused.
- Do not remove unrelated dead code; mention it separately if relevant.

### Verification over hope

- Define success in terms that can be checked.
- Prefer reproducing bugs with a test or deterministic verification step before fixing them.
- After changes, run the narrowest useful verification first, then broaden only if needed.
- Do not claim something works unless it was verified, or explicitly state what was not verified.

---

## Execution Workflow

For non-trivial tasks, work in this order:

1. Understand the request and constraints
2. Inspect the relevant code path
3. State assumptions and risks briefly when they matter
4. Make the smallest correct change
5. Verify with the narrowest relevant check
6. Summarize what changed, how it was verified, and any remaining uncertainty

When a task naturally breaks into steps, use a brief plan in this form:

```text
1. [step] -> verify: [check]
2. [step] -> verify: [check]
3. [step] -> verify: [check]
````

Examples:

* "Fix the bug" -> reproduce it, patch it, verify the reproduction no longer fails
* "Add validation" -> add failing tests for invalid inputs, implement validation, make tests pass
* "Refactor X" -> preserve behavior with focused tests before and after

---

## Clarification Rules

Ask before proceeding only when one of these is true:

* the requirement is genuinely ambiguous in a way that changes product behavior
* the user asked for a choice and did not specify the decision criteria
* the change is risky, destructive, or expensive to reverse
* required information is missing and cannot be inferred from the repository

Otherwise, proceed with the safest reasonable interpretation and state the assumption briefly.

---

## Editing Rules

### Preserve local consistency

* Follow the conventions already used in the file or module you are editing.
* Prefer existing helpers, patterns, and utilities over introducing new ones.
* Do not rename symbols, move code, or reshape APIs unless required by the task.

### Minimize diff size

* Keep edits tightly scoped.
* Avoid incidental formatting churn.
* Do not rewrite surrounding code just to make your change look stylistically uniform.

### Comments

* Do not add comments that merely restate what the code does.
* Comment only when explaining intent, a non-obvious constraint, or a tradeoff.
* Keep existing useful comments unless they became incorrect due to your change.

---

## Formatting Rules

### Highest priority formatting rule

* Do not reflow or rewrap existing lines that are `<= 120` characters.
* Only wrap when a line exceeds `120` characters.
* If formatting rules conflict, preserve existing wrapping and apply minimal edits.
* Do not introduce extra line breaks purely for readability or style when the line fits within `120` characters.
* Keep `if` conditions on one line when they fit within `120` characters.
* Avoid multi-line walrus layouts unless the single-line form exceeds `120` characters.
* Prefer a readable non-walrus alternative over a wrapped walrus form when that keeps lines within `120` characters.
* Keep a function signature on one line if it fits within `120` characters.

Examples:

* Good:
  `if allowlist_check_error := check_allowlist(table_name_normalization_error):`

* Good:
  `allowlist_check_error = check_allowlist(table_name_normalization_error)`
  `if allowlist_check_error:`

* Bad:

  ```python
  if (
      allowlist_check_error
      := check_allowlist(table_name_normalization_error)
  ):
  ```

### General line length

* Prefer a soft line limit of `120` characters.
* If a line fits within `120` characters, do not wrap it unnecessarily.
* If a line exceeds `120` characters, wrap it sensibly and locally.

---

## Testing and Verification

* Prefer focused tests closest to the changed behavior.
* Start narrow:

  * single test
  * single test file
  * targeted lint/type check
  * focused manual reproduction
* Broaden verification only as needed based on risk.

Examples of good verification:

* bug fix -> reproduce with a failing test, then make it pass
* parser change -> targeted parser tests and affected snapshot updates
* UI change -> targeted component test, then relevant page smoke check
* data/model change -> affected unit tests, migration check, and one realistic integration path if warranted

If you could not run verification, say so explicitly and explain why.

---

## Virtual Environment and Commands

* Use the existing virtual environment when present.
* Prefer invoking tools through the project venv, for example:

  * Windows: `".venv/Scripts/python.exe" -m pytest`
  * POSIX: `".venv/bin/python" -m pytest`
* Prefer module execution (`python -m ...`) when appropriate.
* Use the narrowest command that validates the change.

---

## Code Style Guidelines

### General Python

* Prefer clarity over cleverness.
* Keep control flow straightforward.
* Use small helper functions only when they remove real duplication or make logic meaningfully clearer.
* Avoid introducing abstractions for future reuse unless that reuse already exists.
* Preserve public behavior unless the user asked to change it.

### Type hints

* Use PEP 604 unions: `X | Y`, `X | None`.
* Annotate `None` returns explicitly when useful.
* Avoid excessive annotations for trivial local variables.
* Keep type hints consistent with the existing codebase.

### Error handling

* Handle realistic failure modes at the right boundary.
* Do not add defensive code for impossible states unless the surrounding code already expects it.
* Prefer precise exceptions and clear error messages over broad catch-all handling.

### Logging

* Add logging only when it helps diagnose real operational issues.
* Do not add noisy logs in hot paths without a clear need.
* Follow existing logging patterns in the repository.

---

## Frontend

* Use utility classes that are dark/light theme aware.
* Avoid fixed colors like `bg-white`; prefer `bg-body`, `text-body`, and `*-subtle` utilities.
* Keep user-facing UI text in Russian unless explicitly asked otherwise.
* Reuse existing UI patterns and components before introducing new ones.

---

## Django Conventions

For Django-based apps:

* Keep settings in `config/settings.py`.
* Keep URL routing in `config/urls.py` or per-app `urls.py`.
* Prefer class-based views when they fit existing reusable patterns.
* Use Django forms or serializers for validation where appropriate.
* Keep secrets out of settings; use environment variables or `python-dotenv` if that pattern already exists.
* Avoid importing settings in models to prevent app loading cycles.
* Keep database configuration in `DATABASES` with explicit keys.

---

## Configuration

* Read environment variables with `os.environ` or `os.getenv`.
* Keep base configuration in settings and override per environment via env vars.
* Do not hardcode secrets, tokens, or environment-specific values.
* Prefer extending existing config patterns over creating parallel ones.

---

## Dependency Rules

* Do not add new dependencies unless they are clearly justified by the task.
* Prefer the standard library or already-installed project dependencies first.
* If a new dependency is necessary, choose the smallest appropriate one and state why.

---

## Git and Commit Messages

Only provide commit messages when the user asks.

When asked, use Conventional Commits with scope and body:

```text
<type>(<scope>): <subject>

- <change 1>
- <change 2>

Why: <short reason>
```

Rules:

* Keep the subject imperative and concise.
* Allowed scopes: function name, file path, file name, or thematic scope such as `ui`, `ux`, `backend`, `tests`.
* Keep body bullets short and focused on what changed.
* Keep the `Why:` line brief and concrete.

---

## Response Expectations

When reporting completed work, include:

* what changed
* where it changed
* how it was verified
* any assumptions, limitations, or unverified areas that matter

Do not overstate confidence. Be precise about what is known versus inferred.
