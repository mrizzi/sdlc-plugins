# Criterion 3: Invalid threshold returns 400 Bad Request

**Criterion:** `GET /api/v2/sbom/{id}/advisory-summary?threshold=invalid` returns 400 Bad Request

**Verdict:** FAIL

## Analysis

The PR diff handles the threshold value lookup as follows:

```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .unwrap_or(0);
```

When an invalid threshold value is provided (e.g., `?threshold=invalid`), the `.position()` call returns `None` because "invalid" is not found in the `severity_order` array. The `.unwrap_or(0)` then silently defaults to index 0 (which corresponds to "critical").

This means that instead of returning a 400 Bad Request error, the endpoint silently treats any invalid threshold value as `threshold=critical`. The task description explicitly requires:
- Reusing `common/src/error.rs::AppError` for validation errors
- Returning 400 for invalid threshold values

The implementation should:
1. Check if the threshold value is valid
2. If not, return an `AppError` that maps to a 400 Bad Request response

No validation is performed, and no error is returned for invalid input.

**Conclusion:** Invalid threshold values are silently accepted and defaulted to "critical" instead of returning a 400 Bad Request response. This criterion is NOT met.
