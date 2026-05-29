# Criterion 2: Without threshold, returns all severity counts (backward compatible)

**Criterion:** `GET /api/v2/sbom/{id}/advisory-summary` without threshold returns all severity counts (backward compatible)

**Verdict: PASS**

## Analysis

In the PR diff for `modules/fundamental/src/advisory/endpoints/get.rs`, the `SummaryParams` struct defines `threshold` as `Option<String>`:

```rust
#[derive(Debug, Deserialize)]
pub struct SummaryParams {
    pub threshold: Option<String>,
}
```

The filtering logic uses a `match` on `&params.threshold`:

```rust
let filtered = match &params.threshold {
    Some(threshold) => {
        // ... filtering logic ...
    }
    None => summary,
};
```

When no `threshold` query parameter is provided, `params.threshold` is `None`, and the code falls through to the `None =>` arm which returns the unmodified `summary` directly. This preserves the original behavior exactly -- all four severity counts (critical, high, medium, low) plus the total are returned as-is from the `aggregate_severities` call.

The backward compatibility is maintained because:
1. The `threshold` parameter is optional (`Option<String>`)
2. When absent, the response is identical to the pre-change behavior
3. No structural changes were made to the `AdvisorySummary` type itself in the service layer (the `advisory.rs` diff shows no changes to the struct or aggregation logic)

**Evidence:**
- `SummaryParams.threshold` is `Option<String>` -- optional
- `None => summary` branch returns the unfiltered aggregation result
- No changes to `AdvisorySummary` struct fields in the service layer

This criterion is satisfied.
