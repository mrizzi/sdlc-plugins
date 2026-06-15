# Criterion 2: `GET /api/v2/sbom/{id}/advisory-summary` without threshold returns all severity counts (backward compatible)

## Verdict: PASS

## Analysis

When the `threshold` query parameter is not provided, `params.threshold` is `None` (since it is declared as `Option<String>` in the `SummaryParams` struct).

The filtering logic uses a `match` expression:

```rust
let filtered = match &params.threshold {
    Some(threshold) => { /* filtering logic */ }
    None => summary,
};
```

When `threshold` is `None`, the code falls through to the `None` arm, which returns the original `summary` unmodified. This preserves the existing behavior exactly -- all severity counts (critical, high, medium, low) and the total are returned as-is from the `aggregate_severities` call.

The backward compatibility is maintained because:
1. The new `SummaryParams` query parameter struct uses `Option<String>`, so the parameter is optional
2. When omitted, the original response is returned without any modification
3. No fields are added to or removed from the response in the `None` case

## Evidence

- File: `modules/fundamental/src/advisory/endpoints/get.rs`
- The `None => summary` arm passes through the unmodified aggregation result
- The `SummaryParams` struct uses `Option<String>` for threshold, making it optional
