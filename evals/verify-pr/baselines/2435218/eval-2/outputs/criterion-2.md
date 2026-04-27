# Criterion 2: Backward compatibility without threshold parameter

**Criterion:** `GET /api/v2/sbom/{id}/advisory-summary` without threshold returns all severity counts (backward compatible)

**Verdict:** PASS

## Analysis

The PR diff in `modules/fundamental/src/advisory/endpoints/get.rs` shows that the `SummaryParams` struct defines `threshold` as `Option<String>`:

```rust
#[derive(Debug, Deserialize)]
pub struct SummaryParams {
    pub threshold: Option<String>,
}
```

In the handler, when `params.threshold` is `None` (no threshold query parameter provided), the code falls through to the `None` arm of the match:

```rust
let filtered = match &params.threshold {
    Some(threshold) => {
        // ... filtering logic ...
    }
    None => summary,
};
```

When no threshold is provided, the original `summary` is returned unmodified, which contains all four severity counts (critical, high, medium, low) as produced by `AdvisoryService::aggregate_severities()`.

This preserves backward compatibility -- the endpoint behaves identically to before when no threshold parameter is supplied. The `Option<String>` type with Axum's `Query` extractor means the parameter is truly optional and the endpoint continues to function without it.

**Conclusion:** This criterion is satisfied. The endpoint returns all severity counts when no threshold parameter is provided.
