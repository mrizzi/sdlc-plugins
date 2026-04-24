## Criterion 3: Invalid threshold value returns 400 Bad Request

**Criterion**: `GET /api/v2/sbom/{id}/advisory-summary?threshold=invalid` returns 400 Bad Request.

**Result**: FAIL

**Reasoning**:

The diff shows the following logic for looking up the threshold value:

```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .unwrap_or(0);
```

When an invalid threshold value (e.g., `?threshold=invalid`) is provided, `.position()` returns `None`, and `.unwrap_or(0)` silently defaults to index 0 (which corresponds to "critical"). This means invalid input is treated as `?threshold=critical` rather than returning a 400 Bad Request error.

The task explicitly requires returning 400 Bad Request for invalid threshold values, and the implementation notes reference using `common/src/error.rs::AppError` for validation errors. The code should instead check for `None` from `.position()` and return an `AppError` with a 400 status code.

The correct approach would be something like:

```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .ok_or_else(|| AppError::BadRequest(format!("Invalid threshold value: {}", threshold)))?;
```

**Verdict**: FAIL -- Invalid threshold values are silently accepted and defaulted to "critical" instead of returning a 400 Bad Request response. This is a validation gap that could cause confusing behavior for API consumers.
