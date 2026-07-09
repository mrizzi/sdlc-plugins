## Criterion 2: `GET /api/v2/sbom/{id}/advisory-summary` without threshold returns all severity counts (backward compatible)

**Result: PASS**

### Analysis

When no `threshold` query parameter is provided, the `SummaryParams.threshold` field is `None` (it is declared as `Option<String>`). The match arm for `None` returns the unmodified summary:

```rust
None => summary,
```

This preserves the original behavior exactly -- the `summary` object returned by `AdvisoryService::aggregate_severities()` is passed through unchanged.

### Evidence

The diff shows the original handler returned `Ok(Json(summary))`. The new code wraps this in a match expression where the `None` branch assigns `summary` to `filtered`, and then returns `Ok(Json(filtered))`. The response payload is identical to the pre-change behavior when no threshold is specified.

The `SummaryParams` struct uses `Option<String>` for the threshold field, which means axum's `Query` extractor will set it to `None` when the parameter is absent from the URL, following standard serde deserialization behavior for optional fields.

### Caveat

While backward compatibility is maintained for the existing fields, criterion 5 requires a new `threshold_applied` boolean field in the response. If that field were implemented, it should be `false` in this case. Its absence means the response shape is unchanged from the original -- technically backward compatible, but missing the new field the spec requires.
