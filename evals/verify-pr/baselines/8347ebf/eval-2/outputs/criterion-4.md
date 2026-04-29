# Criterion 4: Severity ordering is correct: critical > high > medium > low

## Verdict: FAIL

## Analysis

The severity ordering is defined in the code as an array:

```rust
let severity_order = ["critical", "high", "medium", "low"];
```

This array correctly represents the ordering from most severe (index 0) to least severe (index 3): critical > high > medium > low. The ordering definition itself is correct.

However, the criterion requires not just that the ordering is correctly defined, but that it is correctly applied in the filtering logic. The ordering is used to determine which severities to include when a threshold is set -- severities at or above the threshold should be included.

### How the ordering is applied

The filtering uses comparisons of `threshold_idx` against hardcoded severity indices:

```rust
critical: summary.critical,                                    // always included
high: if threshold_idx <= 1 { summary.high } else { 0 },      // included when threshold_idx <= 1
medium: if threshold_idx <= 2 { summary.medium } else { 0 },  // included when threshold_idx <= 2
low: if threshold_idx <= 3 { summary.low } else { 0 },        // included when threshold_idx <= 3
```

The intent is: "include this severity if it is at or above the threshold." In the array, lower indices are more severe. A severity should be included if its index is less than or equal to the threshold index. But the conditions check if the `threshold_idx` is less than or equal to the severity's index, which is the reverse.

### Concrete example: `threshold=medium` (idx=2)

| Severity | Index | Condition | Expected | Actual |
|----------|-------|-----------|----------|--------|
| critical | 0 | always | INCLUDED | INCLUDED |
| high | 1 | `2 <= 1` = false | INCLUDED | EXCLUDED |
| medium | 2 | `2 <= 2` = true | INCLUDED | INCLUDED |
| low | 3 | `2 <= 3` = true | EXCLUDED | INCLUDED |

With `threshold=medium`, the expected result is critical + high + medium. The actual result is critical + medium + low. High is incorrectly excluded and low is incorrectly included.

### Assessment

While the severity ordering array is correctly defined, the comparison logic that uses this ordering to filter results is inverted. The ordering is not correctly applied in practice. Since the criterion is about the ordering being "correct" in the context of the filtering functionality, and the filtering produces wrong results due to the inverted comparison, this criterion fails.

Additionally, the task's Implementation Notes specify "Define a `Severity` enum with `Critical`, `High`, `Medium`, `Low` variants implementing `Ord`." No such enum was created -- the code uses raw strings and array index comparisons instead. A proper `Ord`-implementing enum would make the ordering semantics clearer and less error-prone.

## Conclusion

This criterion is NOT satisfied. Although the ordering array is correctly defined, the comparison logic that applies it is inverted, producing incorrect filtering results for all threshold values except "critical" and the no-threshold case.
