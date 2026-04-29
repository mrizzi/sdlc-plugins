# Criterion 3: `GET /api/v2/sbom/{id}/advisory-summary?threshold=invalid` returns 400 Bad Request

## Verdict: FAIL

## Analysis

The PR handles unknown threshold values using `unwrap_or(0)`:

```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .unwrap_or(0);
```

When an invalid threshold value like `"invalid"` is provided:

1. `threshold.to_lowercase()` produces `"invalid"`
2. `severity_order.iter().position(...)` searches `["critical", "high", "medium", "low"]` for `"invalid"`
3. The search finds no match, returning `None`
4. `.unwrap_or(0)` converts `None` to `0` (the index for "critical")
5. The filtering proceeds as if `threshold=critical` was specified

### What should happen

According to the acceptance criterion, an invalid threshold value must return an HTTP 400 Bad Request response. The implementation notes in the task description specify: "Reuse `common/src/error.rs::AppError` for validation errors (return 400 for invalid threshold values)."

### What actually happens

Invalid threshold values are silently accepted and treated as `threshold=critical` (index 0). No validation error is returned. The user receives a 200 OK response with filtered data, with no indication that their input was invalid.

### Missing implementation

The correct approach would be to:
1. Check if the threshold value exists in the valid severity list
2. If not, return `Err(AppError::BadRequest("Invalid threshold value: ..."))` or similar
3. This would produce the required 400 Bad Request response

The task's Implementation Notes explicitly reference `common/src/error.rs::AppError` for this purpose, but the PR does not use it for threshold validation.

## Conclusion

This criterion is NOT satisfied. Invalid threshold values are silently accepted instead of returning a 400 Bad Request error.
