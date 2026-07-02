# Criterion 4: Severity ordering is correct: critical > high > medium > low

## Verdict: FAIL

## Analysis

While the severity order array itself is correctly defined, the comparison logic that uses it is inverted, meaning the ordering is not correctly applied in practice.

### Correct Definition

The `severity_order` array is defined as:
```rust
let severity_order = ["critical", "high", "medium", "low"];
```

This correctly encodes the ranking: critical (index 0, highest) > high (index 1) > medium (index 2) > low (index 3, lowest). A lower index means higher severity.

### Incorrect Application

The filtering conditions check `threshold_idx <= N` instead of `N <= threshold_idx`:

```rust
high: if threshold_idx <= 1 { summary.high } else { 0 },
medium: if threshold_idx <= 2 { summary.medium } else { 0 },
low: if threshold_idx <= 3 { summary.low } else { 0 },
```

The intent is to include a severity level only if it is at or above the threshold. For a severity at index `S` to be "at or above" a threshold at index `T`, we need `S <= T` (the severity's rank is numerically less than or equal to the threshold's rank, meaning it is at least as severe). The code checks `T <= S` instead, which inverts the condition.

### Demonstration

For threshold="critical" (T=0), the correct behavior is to include only critical. But:
- high: `0 <= 1` = true -> INCLUDED (wrong, high is below critical)
- medium: `0 <= 2` = true -> INCLUDED (wrong)
- low: `0 <= 3` = true -> INCLUDED (wrong)

For threshold="medium" (T=2), the correct behavior is to include critical, high, and medium. But:
- high: `2 <= 1` = false -> EXCLUDED (wrong, high is above medium)
- medium: `2 <= 2` = true -> INCLUDED (correct)
- low: `2 <= 3` = true -> INCLUDED (wrong)

### Additional Note

The task specification mentions defining a `Severity` enum with `Ord` implementation. Instead, the PR uses a raw string array with index-based comparison, and the comparison is inverted. A proper `Severity` enum with `Ord` would have made this logic clearer and less error-prone.

### Conclusion

The severity ordering definition is correct, but its application in the filtering logic is inverted, making the feature produce incorrect results for every threshold value. This criterion is not met.
