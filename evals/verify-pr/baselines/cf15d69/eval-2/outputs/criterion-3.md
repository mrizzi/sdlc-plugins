# Criterion 3: `GET /api/v2/sbom/{id}/advisory-summary?threshold=invalid` returns 400 Bad Request

## Verdict: FAIL

## Analysis

The acceptance criterion requires that providing an invalid threshold value (e.g., `?threshold=invalid`) returns a 400 Bad Request error response. The implementation does NOT satisfy this criterion.

In the diff at `modules/fundamental/src/advisory/endpoints/get.rs`, the threshold value is looked up in the severity order array:

```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .unwrap_or(0);
```

The critical issue is the use of `.unwrap_or(0)`. When an invalid threshold value is provided (one that does not match "critical", "high", "medium", or "low"), the `.position()` call returns `None`, and `.unwrap_or(0)` silently converts this to index `0` (which corresponds to "critical").

This means:
- `?threshold=invalid` silently behaves as `?threshold=critical`
- `?threshold=foo` silently behaves as `?threshold=critical`
- `?threshold=` (empty string) silently behaves as `?threshold=critical`

The task's Implementation Notes explicitly state: "Reuse `common/src/error.rs::AppError` for validation errors (return 400 for invalid threshold values)." The implementation ignores this guidance entirely.

The correct implementation should validate the threshold value and return an `AppError` (which maps to 400 Bad Request) when the value is not one of the recognized severity levels. For example:

```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .ok_or(AppError::BadRequest("Invalid threshold value".into()))?;
```

## Evidence

- File: `modules/fundamental/src/advisory/endpoints/get.rs`
- The `.unwrap_or(0)` on the `.position()` call silently accepts any input value
- No usage of `AppError` for validation errors anywhere in the threshold handling code
- The task's Implementation Notes specify using `common/src/error.rs::AppError` for validation
- No 400 status code is returned for any threshold input value
