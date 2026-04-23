# Criterion 3: `GET /api/v2/sbom/{id}/advisory-summary?threshold=invalid` returns 400 Bad Request

## Result: FAIL

## Reasoning

The diff does not validate the threshold parameter value. When an invalid threshold value is provided (e.g., `?threshold=invalid`), the code uses:

```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .unwrap_or(0);
```

The `.unwrap_or(0)` silently falls back to index 0 (which corresponds to "critical") when the value is not found in the severity order array. This means an invalid threshold like `?threshold=invalid` would silently behave the same as `?threshold=critical` instead of returning a 400 Bad Request error.

The task explicitly requires returning 400 for invalid threshold values, and the Implementation Notes specify reusing `common/src/error.rs::AppError` for validation errors. Neither of these requirements is met. There is no validation, no error return, and no use of `AppError` for bad input.
