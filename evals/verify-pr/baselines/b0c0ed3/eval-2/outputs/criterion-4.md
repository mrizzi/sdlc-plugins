## Criterion 4: Severity ordering is correct: critical > high > medium > low

### Result: FAIL

### Analysis

The severity ordering is correctly defined in the array:

```rust
let severity_order = ["critical", "high", "medium", "low"];
```

This correctly represents critical (index 0, highest severity) > high (index 1) > medium (index 2) > low (index 3, lowest severity).

However, while the ordering definition is correct, its application in the filtering logic is inverted. The condition `threshold_idx <= N` means "include this severity if the threshold index is less than or equal to the severity's position," which effectively includes severities at or below the threshold rather than at or above it. See Criterion 1 for the detailed walkthrough of how this inversion manifests.

The task's implementation notes also recommend defining a `Severity` enum with `Ord` implementation, which would encode the ordering in the type system and make comparisons type-safe. Instead, the implementation uses raw string matching and manual index comparisons, which is fragile and directly led to the logic inversion bug.

Because the criterion asks whether the severity ordering is correct in practice (not merely defined correctly), and the ordering is misapplied during filtering, this criterion fails.
