---
name: clean-code
description: >-
  Write, modify, refactor, or review code for readability and maintainability. Use for implementation work involving
  business logic, control flow, dependencies, or module boundaries, including new features, and for focused refactors
  or code-quality reviews. Skip formatting-only changes and simple explanations.
---

# Clean Code

Apply these rules from the start when implementing new features or modifying code, as well as during refactors and
code-quality reviews. An existing maintenance problem is not required.
Follow the user's requested scope: a review does not authorize edits. Preserve required behavior, public interfaces,
and the repository's established conventions unless the requested change calls for an adjustment.

## Approach

- Inspect relevant implementation, nearby tests, and established patterns before writing code. For new code, inspect
  its intended callers and integration points where they exist. Read more only when the result depends on it.
- Identify the behavior that must remain stable, including return values, ordering, mutation, failure contracts, and
  externally visible side effects where relevant. Inspect callers when those contracts are unclear.
- Make the smallest coherent implementation that satisfies the requested behavior. Do not refactor adjacent code
  without a present benefit.
- Ground new structures and structural changes in current requirements or a concrete maintenance problem, such as a rule
  duplicated across callers, a dependency that prevents focused testing, or a change that requires unrelated modules to
  move together. Prefer the smallest coherent solution, not merely the fewest changed lines.
- Prefer clear names, straightforward control flow, local code, and explicit side effects over cleverness or speculative
  abstractions.
- Treat principles as heuristics, not quotas. Avoid arbitrary limits on lines, parameters, functions, or classes.

## Code quality

- Keep each function or class focused on one coherent responsibility and keep related behavior together.
- Keep business rules with the code that owns them. Make dependencies explicit and avoid coupling unrelated policies.
- Share code when it represents the same rule and should change together. Keep similar code separate when it represents
  different policies. Prefer small duplication over an abstraction with unrelated modes or flags.
- Extract a helper when it clarifies a meaningful concept, centralizes a shared rule, or separates logic from I/O for
  useful testing. Keep abstractions at a consistent level; introduce interfaces or layers only for a present need.
- Choose names that reveal purpose and distinguish concepts clearly.
- Make mutation, state changes, and I/O apparent at the appropriate boundary. Avoid hidden side effects.
- Follow the established error contract. Catch failures where meaningful recovery or useful context is possible. Avoid
  silent fallback, broad catches that hide defects, and changes to public failure behavior during a refactor.
- Use comments for non-obvious intent, constraints, or trade-offs. Improve the code instead of commenting on obvious
  mechanics.

## Verification

Test the main observable behavior and changed edge cases, not implementation details or incidental formatting. Preserve
or extend focused regression coverage when it directly protects the change. Run the narrowest useful verification and
required repository checks. Repeat or broaden checks only when changes, failures, or unresolved risks justify it, and
report material gaps.

Review the final diff for unnecessary indirection, duplicated policy, hidden side effects, and unrelated edits.

For reviews, lead with the highest-impact evidence-based finding. Separate concrete correctness, compatibility, security,
performance, or maintenance risks from style preferences.

When evaluating changes to this skill or the model using it, use [evaluation cases](references/evaluation-cases.md).
These cases are for skill maintenance; do not load or run them during ordinary coding tasks.
