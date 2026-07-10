## Criterion 3: `GET /api/v2/sbom/{id}/advisory-summary?threshold=invalid` returns 400 Bad Request

### Verdict: FAIL

### Analysis

The task requires that invalid threshold values (values other than "critical", "high", "medium", "low") return a 400 Bad Request response. The implementation does NOT satisfy this requirement.

The code uses `.unwrap_or(0)` when looking up the threshold value in the severity order array:

```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .unwrap_or(0);
```

When an invalid threshold value is provided (e.g., `?threshold=invalid`):
1. `.position()` returns `None` because "invalid" is not found in `["critical", "high", "medium", "low"]`
2. `.unwrap_or(0)` silently converts `None` to index 0
3. The code proceeds as if `threshold=critical` was specified
4. No error is returned to the client

The implementation should instead detect the invalid value and return an `AppError` that maps to HTTP 400 Bad Request. The task's Implementation Notes explicitly reference using `common/src/error.rs::AppError` for validation errors.

A correct implementation would look something like:
```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .ok_or(AppError::BadRequest("Invalid threshold value".into()))?;
```

### Evidence

- File: `modules/fundamental/src/advisory/endpoints/get.rs`, diff lines showing `.unwrap_or(0)`
- Invalid threshold values are silently treated as "critical" (index 0)
- No 400 Bad Request response is returned for invalid values
- The `AppError` type is already imported but not used for threshold validation
