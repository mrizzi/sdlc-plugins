# Criterion 3: Invalid threshold returns 400 Bad Request

**Criterion:** `GET /api/v2/sbom/{id}/advisory-summary?threshold=invalid` returns 400 Bad Request

**Verdict:** FAIL

## Analysis

The diff in `modules/fundamental/src/advisory/endpoints/get.rs` handles the threshold lookup as follows:

```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .unwrap_or(0);
```

The `.position()` call returns `None` when the threshold value does not match any of `["critical", "high", "medium", "low"]`. However, instead of returning a 400 Bad Request error, the code uses `.unwrap_or(0)` which silently defaults invalid values to index 0 (equivalent to "critical").

This means:
- `?threshold=invalid` silently behaves as `?threshold=critical`
- `?threshold=banana` silently behaves as `?threshold=critical`
- `?threshold=` (empty string) silently behaves as `?threshold=critical`
- Any unrecognized threshold value is silently accepted

The task description explicitly states in the Implementation Notes: "Reuse `common/src/error.rs::AppError` for validation errors (return 400 for invalid threshold values)." The acceptance criterion requires a 400 Bad Request response for invalid threshold values.

**What should have been implemented:**

The code should check whether `.position()` returns `None` and, if so, return an `Err(AppError::BadRequest(...))` or equivalent 400 response. For example:

```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .ok_or_else(|| AppError::BadRequest(format!("Invalid threshold: {}", threshold)))?;
```

**Evidence:**
- Line in diff: `.unwrap_or(0)` -- silently defaults invalid values instead of returning an error
- `AppError` is imported (`use common::error::AppError;`) but never used for threshold validation
- The task's Implementation Notes explicitly reference `AppError` for this purpose
- No validation error path exists anywhere in the handler for invalid threshold values

This criterion is clearly NOT satisfied. Invalid threshold values are silently accepted rather than rejected with 400 Bad Request.
