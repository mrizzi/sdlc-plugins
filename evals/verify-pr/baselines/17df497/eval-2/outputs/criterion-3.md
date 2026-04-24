## Criterion 3: `GET /api/v2/sbom/{id}/advisory-summary?threshold=invalid` returns 400 Bad Request

### Result: FAIL

### Analysis

The code does not validate the threshold parameter value. When an invalid value is provided (e.g., `threshold=invalid`), the following logic executes:

```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .unwrap_or(0);
```

The `.position()` call returns `None` for an unrecognized threshold value, and `.unwrap_or(0)` silently converts that to index 0 (which corresponds to "critical"). This means an invalid threshold value is silently treated as `threshold=critical` rather than returning a 400 Bad Request error.

The task explicitly requires returning 400 for invalid threshold values and the implementation notes reference using `common/src/error.rs::AppError` for validation errors. The correct implementation should:

1. Check if the threshold value is one of the recognized severity levels
2. If not, return `Err(AppError::BadRequest("Invalid threshold value".into()))` or equivalent
3. Only proceed with filtering if the threshold is valid

The current implementation provides no input validation whatsoever, making this criterion a clear failure.
