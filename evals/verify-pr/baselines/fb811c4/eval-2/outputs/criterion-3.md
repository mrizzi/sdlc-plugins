# Criterion 3: Invalid Threshold Validation

**Criterion:** `GET /api/v2/sbom/{id}/advisory-summary?threshold=invalid` returns 400 Bad Request

**Verdict:** FAIL

## Analysis

The code does NOT validate the threshold parameter value. When an invalid threshold string is provided (e.g., `?threshold=invalid`), the `position()` iterator method fails to find a match in the `severity_order` array and returns `None`. The `.unwrap_or(0)` then silently defaults the index to 0, which corresponds to "critical".

This means:
- `?threshold=invalid` is silently treated as `?threshold=critical`
- `?threshold=foo` is silently treated as `?threshold=critical`
- `?threshold=123` is silently treated as `?threshold=critical`

No 400 Bad Request error is ever returned. The task requires using `common/src/error.rs::AppError` for validation errors, but the code does not import or use `AppError` for this purpose. There is no validation branch, no error return, and no 400 status code generation for invalid input.

## Evidence

From the diff in `get.rs`:
```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .unwrap_or(0);
```

The `.unwrap_or(0)` silently converts any invalid threshold string to index 0. The implementation notes in the task explicitly state: "Reuse `common/src/error.rs::AppError` for validation errors (return 400 for invalid threshold values)." This guidance was not followed.

The correct implementation would check the result of `position()`, and if `None`, return an `Err(AppError::BadRequest("Invalid threshold value"))` or similar error.
