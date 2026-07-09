## Criterion 3: `GET /api/v2/sbom/{id}/advisory-summary?threshold=invalid` returns 400 Bad Request

**Result: FAIL**

### Analysis

The task requires that invalid threshold values (values other than "critical", "high", "medium", "low") return a 400 Bad Request error. The implementation notes specify: "Reuse `common/src/error.rs::AppError` for validation errors (return 400 for invalid threshold values)."

The diff does not validate the threshold value at all. Instead, it silently handles invalid values via `unwrap_or(0)`:

```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .unwrap_or(0);
```

When `position()` returns `None` (because the threshold string does not match any of "critical", "high", "medium", "low"), the code falls through to `unwrap_or(0)`, which silently treats the invalid value as if `threshold=critical` (index 0) were specified.

### Evidence

There is no error path in the handler for invalid threshold values. The code lacks:
- Any call to `AppError::BadRequest` or equivalent
- Any early return with a 400 status code
- Any validation of the threshold parameter before use

The `common/src/error.rs::AppError` type is imported (`use common::error::AppError;`) and used for the 404 case on the SBOM lookup, but is never used for threshold validation. An invalid threshold like `?threshold=foobar` would silently produce a response as if `?threshold=critical` were given, which is incorrect behavior that could confuse API consumers.
