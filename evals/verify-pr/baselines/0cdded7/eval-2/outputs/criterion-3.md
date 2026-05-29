## Criterion 3

**Text**: `GET /api/v2/sbom/{id}/advisory-summary?threshold=invalid` returns 400 Bad Request

**Verdict**: FAIL

**Reasoning**:

The implementation does NOT return 400 Bad Request for invalid threshold values. Instead, invalid values are silently accepted via the `unwrap_or(0)` fallback.

In `modules/fundamental/src/advisory/endpoints/get.rs`, the threshold value is looked up in the severity ordering array:

```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .unwrap_or(0);
```

When `threshold=invalid` is provided:
1. `"invalid"` does not match any entry in `["critical", "high", "medium", "low"]`.
2. `.position()` returns `None`.
3. `.unwrap_or(0)` converts the `None` to index `0`.
4. The endpoint proceeds as if `threshold=critical` was specified and returns a 200 OK response with filtered data.

This is incorrect behavior. The acceptance criterion explicitly requires a 400 Bad Request response for invalid threshold values. The task's implementation notes also state: "Reuse `common/src/error.rs::AppError` for validation errors (return 400 for invalid threshold values)."

The correct implementation should detect the `None` from `.position()` and return a validation error:

```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .ok_or(AppError::BadRequest("Invalid threshold value".into()))?;
```

The `AppError` enum is already imported in this file (`use common::error::AppError;`), so the infrastructure for proper 400 responses is available but unused for this validation case.

This is a clear acceptance criteria failure. The endpoint silently swallows invalid input rather than rejecting it, which violates both the acceptance criterion and the explicit implementation note about using AppError for validation.
