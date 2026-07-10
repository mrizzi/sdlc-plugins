## Criterion 2: `GET /api/v2/sbom/{id}/advisory-summary` without threshold returns all severity counts (backward compatible)

### Verdict: PASS

### Analysis

The diff correctly handles the no-threshold case. When `params.threshold` is `None`, the code falls through to the `None =>` match arm and returns the original `summary` unchanged:

```rust
let filtered = match &params.threshold {
    Some(threshold) => {
        // filtering logic
    }
    None => summary,
};

Ok(Json(filtered))
```

The `SummaryParams` struct defines `threshold` as `Option<String>`, meaning the query parameter is optional. When omitted, Axum's `Query` extractor will deserialize it as `None`. The original `summary` object from `AdvisoryService::aggregate_severities()` is returned without modification, preserving all four severity counts exactly as they were before the change.

This maintains backward compatibility -- clients not using the threshold parameter will receive the same response format and data as before.

### Evidence

- File: `modules/fundamental/src/advisory/endpoints/get.rs`, diff lines showing `None => summary`
- The `threshold` field is `Option<String>`, making the parameter optional
- The original summary is returned unchanged when no threshold is specified
