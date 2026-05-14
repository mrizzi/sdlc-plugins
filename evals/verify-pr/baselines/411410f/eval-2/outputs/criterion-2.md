# Criterion 2: No threshold returns all severity counts (backward compatible)

**Criterion:** `GET /api/v2/sbom/{id}/advisory-summary` without threshold returns all severity counts (backward compatible)

**Verdict: PASS**

## Detailed Reasoning

The PR correctly handles the case when no `threshold` query parameter is provided. The `SummaryParams` struct defines `threshold` as `Option<String>`:

```rust
#[derive(Debug, Deserialize)]
pub struct SummaryParams {
    pub threshold: Option<String>,
}
```

In the handler, the `None` branch of the match returns the unmodified summary directly:

```rust
let filtered = match &params.threshold {
    Some(threshold) => {
        // ... filtering logic ...
    }
    None => summary,
};
```

This preserves the original behavior: when no threshold parameter is supplied, the response contains all four severity counts (critical, high, medium, low) and the total, exactly as the existing `aggregate_severities` method returns them.

The backward compatibility requirement is satisfied because:
1. The `threshold` parameter is optional (`Option<String>`)
2. Existing clients that do not send the parameter receive the same response as before
3. The `None` branch passes through the unmodified `summary` object

## Evidence

- File: `modules/fundamental/src/advisory/endpoints/get.rs`, diff lines showing `None => summary`
- The `SummaryParams.threshold` is `Option<String>`, making it optional in the query string
- No changes to the `AdvisoryService::aggregate_severities` method that would alter the unfiltered response
