# Criterion 3: Invalid threshold returns 400 Bad Request

**Criterion:** `GET /api/v2/sbom/{id}/advisory-summary?threshold=invalid` returns 400 Bad Request

**Verdict:** FAIL

## Analysis

The PR diff in `modules/fundamental/src/advisory/endpoints/get.rs` shows the following threshold validation logic:

```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .unwrap_or(0);
```

When an invalid threshold value is provided (e.g., `?threshold=invalid`), the `.position()` call returns `None` because "invalid" is not found in the `severity_order` array. The code then uses `.unwrap_or(0)` which silently maps the invalid value to index 0, effectively treating it as "critical".

This means:
- `?threshold=invalid` is silently treated as `?threshold=critical`
- No error response is returned to the client
- The client receives a 200 OK with filtered data, unaware their threshold value was invalid

The task explicitly requires that invalid threshold values return a **400 Bad Request** response. The implementation should validate the threshold value against the known severity levels and return an `AppError` (which the task notes maps to 400 for validation errors via `common/src/error.rs::AppError`) when the value is not one of "critical", "high", "medium", or "low".

The correct implementation would look something like:

```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .ok_or_else(|| AppError::BadRequest(format!("Invalid threshold: {}", threshold)))?;
```

The implementation notes in the task explicitly call out: "Reuse `common/src/error.rs::AppError` for validation errors (return 400 for invalid threshold values)."

**Conclusion:** This criterion is NOT satisfied. Invalid threshold values are silently accepted instead of returning 400 Bad Request.
