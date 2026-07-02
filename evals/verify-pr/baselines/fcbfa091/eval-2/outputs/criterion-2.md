# Criterion 2: `GET /api/v2/sbom/{id}/advisory-summary` without threshold returns all severity counts (backward compatible)

## Verdict: PASS

## Analysis

The PR preserves backward compatibility when no `threshold` query parameter is provided.

### Code Under Review

```rust
let filtered = match &params.threshold {
    Some(threshold) => {
        // ... filtering logic ...
    }
    None => summary,
};

Ok(Json(filtered))
```

### Evidence

- When `params.threshold` is `None`, the original `summary` value is returned directly without any modification
- The `SummaryParams` struct defines `threshold` as `Option<String>`, so omitting the query parameter results in `None`
- The existing `aggregate_severities` call and its return value are unchanged
- The `AdvisorySummary` struct fields (critical, high, medium, low, total) are preserved in the `None` branch
- File: `modules/fundamental/src/advisory/endpoints/get.rs`, lines 41-58 of the diff

### Note

While the response is backward compatible in the `None` case, the `threshold_applied` boolean field required by criterion 5 is absent from the response struct entirely. This means the response shape has not been extended as required, but the existing data fields are preserved for backward compatibility purposes. The missing field is tracked under criterion 5.
