## Criterion 3: `GET /api/v2/sbom/{id}/advisory-summary?threshold=invalid` returns 400 Bad Request

### Verdict: FAIL

### Reasoning

The task explicitly requires that passing an invalid threshold value (e.g., `?threshold=invalid`) should return a 400 Bad Request response. The Implementation Notes section reinforces this: "Reuse `common/src/error.rs::AppError` for validation errors (return 400 for invalid threshold values)."

Examining the diff in `modules/fundamental/src/advisory/endpoints/get.rs`, the threshold value is parsed using:

```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .unwrap_or(0);
```

The critical issue is `.unwrap_or(0)`. When `threshold` is an invalid value like `"invalid"`, the `.position()` call returns `None` because `"invalid"` is not found in `["critical", "high", "medium", "low"]`. Instead of returning a 400 Bad Request error, the code silently defaults to index `0` (which corresponds to "critical").

This means:
- `?threshold=invalid` silently behaves as `?threshold=critical`
- `?threshold=foobar` silently behaves as `?threshold=critical`
- `?threshold=123` silently behaves as `?threshold=critical`

There is **no validation** of the threshold parameter. The code never returns an error for invalid values. The `AppError` type is imported (`use common::error::AppError;`) but is never used for threshold validation.

The correct implementation should look something like:

```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .ok_or_else(|| AppError::bad_request(format!("Invalid threshold: {}", threshold)))?;
```

**Evidence from the diff:**
- Line with `.unwrap_or(0)` shows silent fallback instead of error return
- No `400`, `BadRequest`, or threshold validation error handling anywhere in the diff
- The `AppError` import exists but is only used for the SBOM 404 check, not for threshold validation

This criterion is **not satisfied**. The implementation silently accepts any string as a threshold value instead of returning 400 Bad Request for invalid inputs.
