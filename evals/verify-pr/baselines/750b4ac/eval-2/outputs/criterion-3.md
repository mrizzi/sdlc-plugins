# Criterion 3: `GET /api/v2/sbom/{id}/advisory-summary?threshold=invalid` returns 400 Bad Request

## Verdict: FAIL

## Analysis

The PR does not validate the threshold parameter value. When an invalid threshold is provided (e.g., `?threshold=invalid`), the code uses `unwrap_or(0)`:

```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .unwrap_or(0);
```

When `position()` returns `None` (because "invalid" is not in the severity_order array), `unwrap_or(0)` silently defaults to index 0, which corresponds to "critical". This means an invalid threshold value is silently treated as `threshold=critical` instead of returning a 400 Bad Request error.

The task's Implementation Notes explicitly state: "Reuse `common/src/error.rs::AppError` for validation errors (return 400 for invalid threshold values)". The implementation ignores this guidance entirely.

The correct implementation should check whether `position()` returns `None` and, if so, return an `AppError` that maps to a 400 Bad Request response. For example:

```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .ok_or(AppError::BadRequest("Invalid threshold value".into()))?;
```

## Evidence

- File: `modules/fundamental/src/advisory/endpoints/get.rs`
- `.unwrap_or(0)` on the position lookup silently accepts any string as a valid threshold.
- No `AppError` or `Err` return for invalid values anywhere in the threshold handling code.
- The `AppError` type is imported (`use common::error::AppError`) but never used for threshold validation.
