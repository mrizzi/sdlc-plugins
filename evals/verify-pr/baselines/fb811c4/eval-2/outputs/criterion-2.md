# Criterion 2: Backward Compatibility

**Criterion:** `GET /api/v2/sbom/{id}/advisory-summary` without threshold returns all severity counts (backward compatible)

**Verdict:** PASS

## Analysis

The `match` expression on `params.threshold` includes a `None` arm that returns the original unfiltered `summary` directly:

```rust
None => summary,
```

When no `threshold` query parameter is provided, `params.threshold` is `None` (since the field is `Option<String>`), and the original `AdvisorySummary` from `aggregate_severities()` is returned unchanged. This preserves the existing behavior -- all severity counts (critical, high, medium, low, total) are returned as they were before this change.

## Evidence

From the diff in `get.rs`:
```rust
let filtered = match &params.threshold {
    Some(threshold) => {
        // filtering logic
    }
    None => summary,
};

Ok(Json(filtered))
```

The `None` arm passes through the original `summary` unchanged, maintaining backward compatibility.
