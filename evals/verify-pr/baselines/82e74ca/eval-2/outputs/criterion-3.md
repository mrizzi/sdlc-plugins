## Criterion 3: `GET /api/v2/sbom/{id}/advisory-summary?threshold=invalid` returns 400 Bad Request

### Result: FAIL

### Analysis

The implementation does not validate the threshold parameter value at all. When an invalid value like `threshold=invalid` is provided, the following code executes:

```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .unwrap_or(0);
```

The `.position()` call searches the severity order array for the lowercased threshold value. For `"invalid"`, it finds no match and returns `None`. The `.unwrap_or(0)` then silently converts `None` to index 0, which corresponds to `"critical"`.

This means that any invalid threshold value (e.g., `"invalid"`, `"foo"`, `"extreme"`, empty string) is silently treated as if the user had passed `threshold=critical`. No error is returned to the client.

The task acceptance criteria explicitly require returning HTTP 400 Bad Request for invalid threshold values. The implementation notes also reference using `common/src/error.rs::AppError` for validation errors. The correct implementation should:

1. Attempt to match the threshold value against the known severity levels
2. If no match is found, return `Err(AppError::BadRequest(...))` or equivalent 400 error
3. Only proceed with filtering when the threshold value is valid

No input validation exists in the current implementation, making this a clear failure of the criterion.
