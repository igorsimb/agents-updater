---
name: clean-code
description: Improve existing code when a concrete readability, maintainability, or design problem is in scope.
---

# Clean Code

Use this skill for a focused refactor or code-quality review. Preserve required behavior, public interfaces, and the
repository's established conventions.

## Approach

- Inspect the affected implementation and nearby tests before editing. Read more only when the result depends on it.
- Make the smallest change that resolves the concrete problem. Do not refactor adjacent code without a present benefit.
- Prefer clear names, straightforward control flow, local code, and explicit side effects over cleverness or speculative
  abstractions.
- Treat principles as heuristics, not quotas. Avoid arbitrary limits on lines, parameters, functions, or classes.

## Code quality

- Keep each function or class focused on one coherent responsibility and keep related behavior together.
- Extract a helper when it removes real duplication or clarifies a meaningful concept. Keep abstractions at a consistent
  level and do not introduce interfaces or layers without a present need.
- Choose names that reveal purpose and distinguish concepts clearly.
- Make mutation, state changes, and I/O apparent at the appropriate boundary. Avoid hidden side effects.
- Handle realistic failures with precise exceptions and useful context rather than broad catches, error codes, or silent
  failures.
- Use comments for non-obvious intent, constraints, or trade-offs. Improve the code instead of commenting on obvious
  mechanics.

## Verification

Test the main observable behavior and changed edge cases, not implementation details or incidental formatting. Preserve
or extend focused regression coverage when it directly protects the change. Run the narrowest useful verification,
broaden it when risk warrants it, and report material gaps.

For reviews, lead with the highest-impact evidence-based finding. Separate concrete correctness, compatibility, security,
performance, or maintenance risks from style preferences.
