## Criterion 3: `GET /api/v2/sbom/{id}/advisory-summary?threshold=invalid` returns 400 Bad Request

### Analysis

The diff in `modules/fundamental/src/advisory/endpoints/get.rs` handles invalid threshold values with:

```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .unwrap_or(0);
```

When an invalid threshold value is provided (e.g., `threshold=invalid`), `.position()` returns `None`, and `.unwrap_or(0)` silently treats it as index 0 (equivalent to `threshold=critical`). The handler does NOT return a 400 Bad Request error.

The task's Implementation Notes explicitly state: "Reuse `common/src/error.rs::AppError` for validation errors (return 400 for invalid threshold values)". The diff does not use `AppError` or any error return for invalid threshold values.

The expected behavior would be to validate the threshold parameter and return an error response, for example:

```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .ok_or_else(|| AppError::BadRequest("Invalid threshold value".into()))?;
```

Instead, invalid values are silently accepted and treated as `critical`, which is a functional correctness gap.

## Verdict: FAIL

Invalid threshold values are silently accepted via `unwrap_or(0)` instead of returning 400 Bad Request. No validation error is produced. This directly contradicts the acceptance criterion and the implementation notes.
