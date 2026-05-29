# Criterion 2: Backward compatibility without threshold parameter

**Criterion:** `GET /api/v2/sbom/{id}/advisory-summary` without threshold returns all severity counts (backward compatible)

**Verdict:** PASS

## Analysis

The diff in `modules/fundamental/src/advisory/endpoints/get.rs` introduces the `SummaryParams` struct with `threshold: Option<String>`. When no `threshold` query parameter is provided, `params.threshold` will be `None`.

The filtering logic handles this case:

```rust
let filtered = match &params.threshold {
    Some(threshold) => { /* filtering logic */ }
    None => summary,
};
```

When `params.threshold` is `None`, the original `summary` (containing all severity counts) is returned unmodified via `Ok(Json(filtered))`.

This preserves backward compatibility -- the endpoint returns all severity counts when no threshold parameter is supplied. The `SummaryParams` struct uses `Option<String>` which correctly makes the parameter optional.

**Evidence:**
- `SummaryParams` has `pub threshold: Option<String>` -- optional query parameter
- `None => summary` -- returns unfiltered summary when no threshold is provided
- The function signature change only adds `Query(params): Query<SummaryParams>` as a new parameter, which does not break existing callers since the query parameter is optional

This criterion is satisfied.
