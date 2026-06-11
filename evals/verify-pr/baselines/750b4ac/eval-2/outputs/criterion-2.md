# Criterion 2: `GET /api/v2/sbom/{id}/advisory-summary` without threshold returns all severity counts (backward compatible)

## Verdict: PASS

## Analysis

The PR handles the no-threshold case with a `None` match arm:

```rust
let filtered = match &params.threshold {
    Some(threshold) => { /* filtering logic */ }
    None => summary,
};
```

When no `threshold` query parameter is provided, `params.threshold` is `None`, and the original unfiltered `summary` is returned directly. This preserves backward compatibility -- the response contains all severity counts exactly as the existing endpoint returned them before this change.

The `SummaryParams` struct uses `Option<String>` for the threshold field:

```rust
pub struct SummaryParams {
    pub threshold: Option<String>,
}
```

This correctly makes the parameter optional in the query string.

## Evidence

- File: `modules/fundamental/src/advisory/endpoints/get.rs`
- The `None => summary` branch passes through the original aggregated summary unchanged.
- The `SummaryParams.threshold` field is `Option<String>`, making it an optional query parameter.
