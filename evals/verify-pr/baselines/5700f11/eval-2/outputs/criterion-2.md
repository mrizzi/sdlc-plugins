# Criterion 2: `GET /api/v2/sbom/{id}/advisory-summary` without threshold returns all severity counts (backward compatible)

## Result: PASS

## Analysis

The `advisory_summary` handler accepts `Query(params): Query<SummaryParams>` where `SummaryParams` has `threshold: Option<String>`. When no `threshold` query parameter is provided, `params.threshold` is `None`.

The `None` branch of the match statement returns the original `summary` object unmodified:

```rust
None => summary,
```

This preserves all four severity counts (critical, high, medium, low) and the total, maintaining full backward compatibility with the existing endpoint behavior. The `SummaryParams` struct uses `Option<String>`, so the parameter is not required, and requests without it proceed through the existing aggregation path unchanged.

This criterion is satisfied.
