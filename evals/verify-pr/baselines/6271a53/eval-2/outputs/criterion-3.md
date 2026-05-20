# Criterion 3: `GET /api/v2/sbom/{id}/advisory-summary?threshold=invalid` returns 400 Bad Request

## Verdict: FAIL

## Analysis

The acceptance criterion requires that an invalid threshold value (e.g., `?threshold=invalid`) returns a 400 Bad Request response. The implementation does NOT validate the threshold value. Instead, it silently accepts any input by using `.unwrap_or(0)`:

```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .unwrap_or(0);
```

When `threshold=invalid`, `.position()` returns `None` because "invalid" does not match any entry in `["critical", "high", "medium", "low"]`. The `.unwrap_or(0)` then defaults to index 0, which corresponds to "critical". This means an invalid threshold is silently treated as `threshold=critical` rather than returning a 400 error.

The task's Implementation Notes explicitly state: "Reuse `common/src/error.rs::AppError` for validation errors (return 400 for invalid threshold values)." The `AppError` type is already imported in the file but is not used for threshold validation.

The correct implementation should check whether `.position()` returns `None` and, if so, return an `AppError` with a 400 status code, for example:

```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .ok_or_else(|| AppError::bad_request(format!("Invalid threshold value: {}", threshold)))?;
```

## Evidence

- File: `modules/fundamental/src/advisory/endpoints/get.rs`
- Line in diff: `.unwrap_or(0)` on the `.position()` call (line 46 of the diff)
- `AppError` is imported (`use common::error::AppError;`) but never used for validation
- Task Implementation Notes: "Reuse `common/src/error.rs::AppError` for validation errors (return 400 for invalid threshold values)"
