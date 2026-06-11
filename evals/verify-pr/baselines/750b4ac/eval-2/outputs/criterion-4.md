# Criterion 4: Severity ordering is correct: critical > high > medium > low

## Verdict: FAIL

## Analysis

The severity ordering array is correctly defined:

```rust
let severity_order = ["critical", "high", "medium", "low"];
```

This places critical at index 0 (highest severity) through low at index 3 (lowest severity). The ordering definition itself is correct.

However, the filtering logic that uses this ordering is inverted (as detailed in Criterion 1), making the ordering effectively non-functional. While the array correctly encodes the severity hierarchy, the comparison logic that applies it does not produce the correct results. Severities that should be excluded by the threshold are included, and the ordering serves no useful purpose in its current form.

The `total` field computation also ignores the filtering entirely:

```rust
total: summary.critical + summary.high + summary.medium + summary.low,
```

This always sums all four unfiltered severity counts regardless of the threshold, further demonstrating that the severity ordering is not correctly applied.

## Evidence

- File: `modules/fundamental/src/advisory/endpoints/get.rs`
- The `severity_order` array is correctly defined but the comparison logic using `threshold_idx` is inverted.
- The `total` field uses unfiltered values (`summary.critical + summary.high + summary.medium + summary.low`) instead of the filtered values, which would need to be `filtered.critical + filtered.high + filtered.medium + filtered.low` (or computed from the filtered struct fields).
