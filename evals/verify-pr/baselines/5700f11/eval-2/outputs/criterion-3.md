# Criterion 3: `GET /api/v2/sbom/{id}/advisory-summary?threshold=invalid` returns 400 Bad Request

## Result: FAIL

## Analysis

The task requires that an invalid threshold value (anything other than "critical", "high", "medium", or "low") returns a 400 Bad Request response. The implementation does NOT validate the threshold value.

The relevant code:

```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .unwrap_or(0);
```

When an invalid value like `"invalid"` is passed, `.position()` returns `None`, and `.unwrap_or(0)` silently falls back to index 0 (which corresponds to "critical"). This means an invalid threshold value is treated identically to `threshold=critical` -- no error is returned to the client.

The task explicitly requires using `common/src/error.rs::AppError` for validation errors and returning 400 for invalid threshold values. The implementation should check for `None` from `.position()` and return `Err(AppError::BadRequest(...))` or equivalent.

This criterion is not satisfied. Invalid input is silently accepted rather than rejected with a 400 status code.
