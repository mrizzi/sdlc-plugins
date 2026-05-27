## Criterion 2: `GET /api/v2/sbom/{id}/advisory-summary` without threshold returns all severity counts (backward compatible)

**Verdict: PASS**

### Analysis

The diff handles the `None` case for the threshold parameter correctly:

```rust
None => summary,
```

When no `threshold` query parameter is provided, `params.threshold` is `None`, and the original unfiltered `summary` is returned directly. This preserves the existing behavior -- all severity counts (critical, high, medium, low) are returned as-is from the `aggregate_severities` call.

The `SummaryParams` struct correctly declares `threshold` as `Option<String>`, meaning it is not required:

```rust
#[derive(Debug, Deserialize)]
pub struct SummaryParams {
    pub threshold: Option<String>,
}
```

### Evidence

The `match` expression falls through to `None => summary`, returning the complete aggregated result without any modification. This is backward compatible with the pre-change behavior where `Ok(Json(summary))` was returned directly.
