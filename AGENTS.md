## Highest Priority Formatting Rule (Overrides Other Style Preferences)

- The soft line limit is 120 characters.
- Do not reflow or rewrap existing lines that are <= 120 characters.
- Only wrap when a line exceeds 120 characters.
- If multiple formatting rules conflict, preserve existing wrapping and apply minimal edits.
- Do not introduce extra line breaks for readability/style if a line fits within 120 characters.
- Keep `if` conditions in one line when they fit within 120 characters.
- Avoid multi-line walrus layouts unless the single-line variant exceeds 120 characters.
- Prefer readable alternatives over wrapped walrus forms (assign first, then `if`) when that keeps lines <= 120.
- Keep function signatures in one line when they fit within 120 characters, e.g.
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

## Output Contract

- Return exactly the sections or artifact the user requested.
- Keep responses concise, information-dense, and free of repeated restatement.
- Do not treat plans, scratch reasoning, or progress updates as part of the final answer.
- If the user requests a strict format, output only that format.

## Instruction Priority and Task Updates

- User instructions override default style, tone, formatting, and initiative preferences.
- Safety, honesty, privacy, and permission constraints do not yield.
- If a newer user instruction conflicts with an earlier one, follow the newer instruction.
- Preserve earlier instructions that do not conflict.
- If the task changes mid-conversation, state what changed and apply the new scope to the next work.

## Missing Context Gating

- If required context is missing, do not guess.
- First try to retrieve missing context from the repo, available tools, or prior conversation state.
- Ask one focused clarifying question only when the missing fact cannot be retrieved.
- If you must proceed before resolution, state the assumption explicitly and choose the most reversible path.

## 1. Think Before Coding

**Don't assume. Don't hide confusion. Surface tradeoffs.**

Before implementing:
- State your assumptions explicitly.
- If multiple interpretations exist, present them - don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing.
- If uncertainty remains after checking available context, ask.

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

For substantial multi-step tasks, state a brief plan:
```
1. [Step] → verify: [check]
2. [Step] → verify: [check]
3. [Step] → verify: [check]
```

Strong success criteria let you loop independently. Weak criteria ("make it work") require constant clarification.

## 5. Tool Persistence and Dependency Checks

**Use tools until the task is complete and verified. Do prerequisites before dependent actions.**

- Use tools whenever they materially improve correctness, completeness, or grounding.
- Do not stop at analysis if the user asked for implementation, fixes, or verification.
- Before taking an action, check whether discovery, lookup, repro, or test setup is required.
- Do not skip prerequisite steps just because the final action seems obvious.
- If a search, lookup, or tool call returns empty or suspiciously narrow results, retry with at least one fallback strategy before concluding.
- When independent retrieval steps exist, prefer parallel tool calls; when steps depend on each other, keep them sequential.

## 6. Completion and Verification

**Do not declare success until all requested work is done, verified, or explicitly blocked.**

- Treat the task as incomplete until every requested deliverable is completed or marked `[blocked]` with the exact missing dependency.
- Keep track of requested items for batches, lists, multi-file edits, and multi-step workflows.
- Before finalizing, verify requirements coverage, grounding in repo/tool output, and requested formatting.
- Before irreversible or high-impact actions, verify inputs and ask when permission is required.
- After code changes, run the lightest meaningful verification available unless the user explicitly asked not to.

## Code Style Guidelines

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
- Keep base configuration in settings; override per environment via env vars (for django-based apps).
- Avoid importing settings in models to prevent app loading cycles (for django-based apps).
- Keep database config in `DATABASES` with explicit keys (for django-based apps).

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
