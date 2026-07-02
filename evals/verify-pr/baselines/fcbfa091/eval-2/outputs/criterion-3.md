# Criterion 3: `GET /api/v2/sbom/{id}/advisory-summary?threshold=invalid` returns 400 Bad Request

## Verdict: FAIL

## Analysis

The PR does not validate the threshold query parameter. Invalid values are silently accepted instead of returning a 400 Bad Request error.

### Code Under Review

```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .unwrap_or(0);
```

### Defect: Silent acceptance of invalid threshold values

The `position()` call returns `None` when the threshold string does not match any entry in `severity_order`. The `.unwrap_or(0)` fallback silently treats any unrecognized threshold value as index `0` (equivalent to "critical"), instead of returning a 400 Bad Request error.

For example, `?threshold=invalid`, `?threshold=xyz`, or `?threshold=` would all silently map to threshold index 0, producing a filtered response as though `?threshold=critical` were requested.

### Expected Behavior

Per the task description's Implementation Notes: "Reuse `common/src/error.rs::AppError` for validation errors (return 400 for invalid threshold values)". The code should:

1. Check whether the threshold value matches a valid severity level
2. If not, return `Err(AppError::BadRequest(...))` or equivalent 400 response
3. Only proceed with filtering if the threshold is valid

### Evidence

- File: `modules/fundamental/src/advisory/endpoints/get.rs`, line 45-46 of the diff
- The `unwrap_or(0)` on line 46 is the specific location where invalid values are silently accepted
- No `AppError::BadRequest` or equivalent error return exists anywhere in the threshold handling code
- The task's Implementation Notes explicitly reference `common/src/error.rs::AppError` for validation errors, but no such import or usage appears in the diff for threshold validation
