# Criterion 3: `GET /api/v2/sbom/{id}/advisory-summary?threshold=invalid` returns 400 Bad Request

## Result: FAIL

## What was checked

Verified whether the endpoint returns a 400 Bad Request response when an invalid threshold value (e.g., `?threshold=invalid`) is provided.

## Evidence from the diff

The threshold parsing logic in `modules/fundamental/src/advisory/endpoints/get.rs` uses `unwrap_or(0)`:

```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .unwrap_or(0);
```

The `severity_order` array contains `["critical", "high", "medium", "low"]`. When `threshold=invalid` is passed, `.position()` returns `None` because "invalid" is not in the array. The `.unwrap_or(0)` then silently defaults to index 0 (critical), treating any unrecognized threshold value as if `?threshold=critical` were specified.

## Gap identified

Invalid threshold values are **silently accepted** and treated as `critical` instead of producing a 400 Bad Request error response. The implementation should validate the threshold value against the known severity levels and return `AppError` (which maps to a 400 status code) when the value is not recognized.

The task's Implementation Notes specifically state: "Reuse `common/src/error.rs::AppError` for validation errors (return 400 for invalid threshold values)." This guidance was not followed.

Expected behavior:
```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .ok_or_else(|| AppError::BadRequest(format!("Invalid threshold value: {}", threshold)))?;
```

Actual behavior: `unwrap_or(0)` silently converts invalid input to a valid index.
