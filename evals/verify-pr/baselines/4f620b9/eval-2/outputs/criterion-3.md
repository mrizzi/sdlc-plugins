# Criterion 3: threshold=invalid returns 400 Bad Request

## Verdict: FAIL

## Reasoning

The acceptance criterion requires that `GET /api/v2/sbom/{id}/advisory-summary?threshold=invalid` returns a 400 Bad Request response when an invalid threshold value is provided.

### Code Analysis

In `modules/fundamental/src/advisory/endpoints/get.rs`, the threshold validation logic is:

```rust
let severity_order = ["critical", "high", "medium", "low"];
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .unwrap_or(0);
```

The `position()` method returns `None` when the threshold value does not match any entry in the `severity_order` array. However, instead of detecting this invalid input and returning a 400 error, the code uses `.unwrap_or(0)` to silently default to index 0 (which corresponds to "critical").

This means that any invalid threshold value (e.g., `?threshold=invalid`, `?threshold=foo`, `?threshold=extreme`) is silently treated as `threshold=critical` instead of being rejected with a 400 Bad Request response.

### Expected Behavior

The task's Implementation Notes specify: "Reuse `common/src/error.rs::AppError` for validation errors (return 400 for invalid threshold values)". The correct implementation should:

1. Check whether `position()` returns `None`
2. If `None`, return an `AppError` that maps to HTTP 400 Bad Request
3. Only proceed with the valid threshold index if `position()` returns `Some(idx)`

### Conclusion

The implementation fails to validate the threshold parameter. Invalid values are silently accepted and treated as "critical" instead of being rejected with a 400 Bad Request response. This criterion is NOT satisfied.
