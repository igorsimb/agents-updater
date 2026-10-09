# Clean-code evaluation cases

Use these cases when changing the skill or evaluating it with a different model. They are manual evaluation fixtures,
not an automated benchmark or a requirement for ordinary coding tasks.

## Method

Compare the previous and proposed skill on the same starting code, prompts, repository instructions, and model settings.
For a model change, keep the skill fixed. Use fresh scratch workspaces for independent cases; retain the resulting code
between turns of a sequence. Keep expected outcomes below out of the evaluated model's prompt.

For selection checks, expose the skill through the normal catalog and send only the request, without naming the skill.
For code-quality checks, explicitly invoke the skill and provide the fixture and task. Record actual skill loading and
inspect the resulting code and checks; do not rely solely on the model's claim that it followed the skill.

Record the model, skill revision, request, observed selection, behavior preserved or changed, verification evidence,
unnecessary abstractions, and unrelated edits. For successive changes, also record whether the change stayed local and
whether existing tests remained useful. Treat selection as variable; repeat ambiguous cases before drawing conclusions.
Judge observable behavior and maintenance costs, not line counts or exact helper names. No change can be a good result.

## Selection requests

| Request | Expected selection |
| --- | --- |
| Simplify this deeply nested function without changing behavior. | Yes |
| Review this service for maintainability; do not edit it. | Yes; findings only |
| These callers duplicate the same validation rule. Refactor them. | Yes |
| Implement a new supplier availability feature. | Yes |
| Add backorder support to the existing availability calculation. | Yes |
| Add this feature and untangle the mixed calculation and persistence logic it touches. | Yes |
| Add a field to this straightforward response object. | Not required |
| Explain what this function returns. | No |
| Format this file using the existing formatter. | No |

## 1. Nested logic and observable behavior

Request: "Simplify this function without changing its behavior. Rows have string articles and integer stock."

```python
def available_articles(rows):
    result = []
    for row in rows:
        if row["enabled"]:
            if row["stock"] > 0:
                if row["article"] not in result:
                    result.append(row["article"])
    return result
```

Expected: clearer control flow; first-seen order and uniqueness preserved; no input mutation. Check empty input,
duplicates, disabled rows, and zero or negative stock. Do not reward a class or helper without a concrete benefit.

## 2. A shared rule across successive changes

Fixture: two callers implement the same supplier availability policy.

```python
def catalog_articles(rows):
    return [row["article"] for row in rows if row["enabled"] and row["stock"] > 0]


def export_rows(rows):
    return [dict(row) for row in rows if row["enabled"] and row["stock"] > 0]
```

Send these requests in separate turns, retaining each result:

1. "These functions apply the same availability rule. Refactor so that rule has one owner; preserve their outputs."
2. "For both callers, also include enabled rows with zero stock when backorder is true. Missing backorder means false."
3. "Negative stock must still be excluded, even with backorder. Add coverage if this is not already protected."

Expected: one shared rule, both callers updated through it, and caller-specific output shapes preserved. Ordering,
duplicates, and export copies must remain intact. Tests should cover both callers and policy boundaries, surviving
internal renaming or extraction. A configurable rule engine is unnecessary for this fixture.

## 3. Similar code representing different policies

Fixture: shipping and support eligibility currently happen to use the same threshold.

```python
def qualifies_for_free_shipping(order_total):
    return order_total >= 100


def qualifies_for_priority_support(annual_spend):
    return annual_spend >= 100
```

Send these requests in separate turns:

1. "Review this duplication for maintainability. Shipping and support are owned by different teams; do not edit."
2. "Raise the free-shipping threshold to 150. Keep the support policy unchanged."

Expected: no forced shared threshold or generic eligibility helper. The second change stays local. Check shipping at
149 and 150, and support at 99 and 100. The review should explain independent policy ownership rather than invent a defect.

## 4. Preserve a public failure contract

Request: "Refactor this parser for readability. Its public contract returns None for invalid input; preserve it."

```python
def parse_quantity(value):
    try:
        quantity = int(value)
    except (TypeError, ValueError):
        return None
    if quantity < 0:
        return None
    return quantity
```

Expected: keeping the function unchanged is acceptable. No conversion to raised exceptions, no broad Exception catch,
and no new fallback value. Check "0", "3", "-1", invalid text, and None. Preserve other existing int conversion behavior;
do not silently introduce stricter validation under a readability request.

## 5. Separate calculation from persistence when it helps

Request: "Make the total calculation independently testable. Preserve save_order_total and its persistence behavior."

```python
from decimal import Decimal


def save_order_total(order, repository):
    subtotal = sum(item.unit_price * item.quantity for item in order.items)
    discount = subtotal * order.discount_rate
    total = max(subtotal - discount, Decimal("0"))
    repository.update_total(order.id, total)
    return total
```

Fixture contract: prices and discount_rate are Decimal values; quantities are integers. Expected: calculation can be
tested without a repository; save_order_total still writes once and returns the written value. Check an empty order,
zero discount, ordinary discount, and the zero floor. A persistence failure still propagates. Avoid adding a new
repository interface or service hierarchy solely to test arithmetic.

## 6. Already-clear code

Request: "Review this function for maintainability. Change it only if there is a concrete problem."

```python
def total_quantity(items):
    return sum(item.quantity for item in items)
```

Fixture contract: items contain numeric quantities and require no additional validation. Expected: leave the function
unchanged and explain briefly. No invented validation, wrapper class, helper extraction, or test suite solely to prove
that this expression uses sum.

## 7. New feature without an existing maintenance problem

Start with an empty scratch module and send these requests in separate turns:

1. "Implement available_articles(rows). Each row has article (string), enabled (bool), and stock (integer). Return unique
   articles in input order for enabled rows with positive stock. Do not mutate rows. Add focused behavior tests."
2. "Also include enabled rows with zero stock when backorder is true. Missing backorder means false. Continue to exclude
   negative stock."

Expected: the skill applies on the initial implementation, without a refactoring request or evidence of poor code.
The first version uses clear names and straightforward control flow, with no speculative service hierarchy or rule
engine. Check empty input, disabled rows, duplicates, ordering, and stock boundaries. The follow-up should remain local;
existing behavior tests should remain useful, with added coverage for backorder and negative stock.
