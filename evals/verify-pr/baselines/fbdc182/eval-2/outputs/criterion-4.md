# Criterion 4: Severity ordering is correct: critical > high > medium > low

## Result: FAIL

## Reasoning

The Implementation Notes specify defining a `Severity` enum with `Critical`, `High`, `Medium`, `Low` variants implementing `Ord`. The diff does not define such an enum. Instead, severity ordering is handled via a hardcoded string array:

```rust
let severity_order = ["critical", "high", "medium", "low"];
```

While the array itself correctly encodes the ordering (critical at index 0 is highest, low at index 3 is lowest), the filtering logic that uses this ordering is inverted. The condition `threshold_idx <= N` checks whether the threshold's position is less than or equal to the severity's position, which is the opposite of the intended semantics. The correct check should be whether the severity's position is less than or equal to the threshold's position (i.e., the severity ranks at or above the threshold).

As a result, the severity ordering is not correctly applied to filtering. For example, with `threshold=high` (index 1), all severities pass the filter because their indices (0, 1, 2, 3) are all >= 1 when checked via `threshold_idx <= severity_index`.
