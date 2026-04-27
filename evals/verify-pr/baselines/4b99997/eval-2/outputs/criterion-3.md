# Criterion 3 Analysis

**Criterion:** `GET /api/v2/sbom/{id}/advisory-summary?threshold=invalid` returns 400 Bad Request

## Assessment: FAIL

### What the criterion requires
When an invalid threshold value is provided (e.g., `?threshold=invalid`), the endpoint must return a 400 Bad Request error response. The task's Implementation Notes explicitly state: "Reuse `common/src/error.rs::AppError` for validation errors (return 400 for invalid threshold values)."

### What the diff implements
The diff uses `unwrap_or(0)` when looking up the threshold value:

```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .unwrap_or(0);
```

### Analysis
When an invalid threshold like `"invalid"` is provided:
1. `severity_order.iter().position(|&s| s == "invalid")` returns `None`
2. `.unwrap_or(0)` silently converts this to index `0` (which corresponds to `"critical"`)
3. The endpoint processes the request as if `threshold=critical` was provided
4. A 200 OK response is returned instead of a 400 Bad Request

This is a **silent acceptance of invalid input**. The task explicitly requires returning 400 Bad Request for invalid threshold values, and the Implementation Notes reference using `AppError` for validation errors. The diff does not import or use `AppError` for this validation, and no error path exists for invalid values.

### Verdict: FAIL

Invalid threshold values are silently treated as `threshold=critical` instead of returning 400 Bad Request. No input validation exists.
