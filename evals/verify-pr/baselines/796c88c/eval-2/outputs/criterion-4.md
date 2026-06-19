# Criterion 4: Severity ordering is correct: critical > high > medium > low

## What was checked

Inspected the PR diff for the severity ordering definition and verified it matches the required ordering.

## Evidence

The implementation defines the severity ordering as:

```rust
let severity_order = ["critical", "high", "medium", "low"];
```

This array correctly represents the ordering critical (index 0, highest) > high (index 1) > medium (index 2) > low (index 3, lowest). The ordering itself is correct.

However, as noted in Criterion 1, the filtering logic that uses this ordering is inverted -- the conditions check `threshold_idx <= severity_position` instead of `severity_position <= threshold_idx`, which means the ordering is correctly defined but incorrectly applied.

The task did not ask for a `Severity` enum with `Ord` implementation as suggested in the Implementation Notes, but the ordering constant itself is correct.

## Verdict: PASS

The severity ordering array correctly represents critical > high > medium > low. The ordering definition itself is correct, even though the filtering logic that uses it has a separate bug (covered by Criterion 1).
