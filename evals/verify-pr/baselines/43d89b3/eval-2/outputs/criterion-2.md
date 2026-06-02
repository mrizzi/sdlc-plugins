# Criterion 2: No threshold returns all severity counts (backward compatible)

**Criterion:** `GET /api/v2/sbom/{id}/advisory-summary` without threshold returns all severity counts (backward compatible)

**Verdict:** PASS

## Analysis

The PR diff shows that when no threshold parameter is provided (`params.threshold` is `None`), the code falls through to the `None` match arm:

```rust
None => summary,
```

This returns the original `summary` object unmodified, which contains all severity counts as aggregated by `AdvisoryService::aggregate_severities()`.

The existing behavior is preserved: the endpoint handler previously returned `Ok(Json(summary))` directly, and now when no threshold is present, it returns the same unmodified summary through the `filtered` variable.

The `SummaryParams` struct uses `Option<String>` for the threshold field, so omitting the query parameter will correctly result in `None`.

**Result:** PASS -- Backward compatibility is maintained when no threshold parameter is provided.
