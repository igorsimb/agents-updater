---
name: clean-code
description: Use when refactoring, reviewing, or improving code quality. Focus on clear, maintainable code without
  changing required behavior.
---

# Clean Code

Use this skill to resolve concrete readability, maintainability, or design problems in existing code. Preserve required
behavior and follow the repository's established conventions.

## Approach

- Inspect the relevant code and tests before proposing or making a change.
- Make the smallest change that resolves the identified problem. Do not refactor adjacent code without a concrete
  benefit.
- Prefer clear names, straightforward control flow, and local code over cleverness or speculative abstractions.
- Preserve the existing public API unless the task explicitly changes it.
- Treat principles as heuristics, not quotas. Avoid arbitrary limits on lines, parameters, functions, or classes.

## Code Quality Heuristics

- Choose names that reveal purpose and distinguish concepts clearly.
- Keep each function or class focused on one coherent responsibility.
- Keep related behavior together; extract a helper only when it removes real duplication or clarifies a meaningful
  concept.
- Keep abstractions at a consistent level. Do not introduce interfaces, patterns, or layers without a present need.
- Avoid hidden side effects. Make state changes, mutation, and I/O apparent at the appropriate boundary.
- Prefer explicit error handling with useful context over error codes, broad catches, or silent failures.
- Use comments for non-obvious intent, constraints, or tradeoffs. Improve code instead of commenting on obvious
  mechanics.

## Verification

- Test the main observable behavior and changed edge cases, not implementation details or incidental formatting.
- Preserve and extend focused regression coverage when it directly protects the change.
- Run the narrowest relevant verification and report material gaps.

## Review Output

Lead with the most important finding or completed improvement. Include the evidence needed to support it, material
caveats, and the next action. Omit generic introductions, repeated guidance, and optional background.
