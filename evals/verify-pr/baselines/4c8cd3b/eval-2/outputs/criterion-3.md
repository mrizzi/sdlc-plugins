# Criterion 3: `GET /api/v2/sbom/{id}/advisory-summary?threshold=invalid` returns 400 Bad Request

## Verdict: FAIL

## Analysis

The PR does NOT validate the threshold parameter value. When an invalid threshold is provided, the code silently falls back to a default behavior instead of returning a 400 Bad Request error.

The relevant code:

```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .unwrap_or(0);
```

When `threshold=invalid` is provided:
1. `severity_order.iter().position(|&s| s == "invalid")` returns `None` because "invalid" is not in `["critical", "high", "medium", "low"]`
2. `.unwrap_or(0)` converts the `None` to `0`, meaning the invalid threshold silently behaves as if `threshold=critical` was provided
3. No error is returned to the client

The task's Implementation Notes explicitly state: "Reuse `common/src/error.rs::AppError` for validation errors (return 400 for invalid threshold values)". The PR does not follow this guidance.

The correct implementation would be:

```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .ok_or_else(|| AppError::bad_request(format!("Invalid threshold value: {}", threshold)))?;
```

This would use the `?` operator to return an `AppError` that maps to a 400 Bad Request response.

## Evidence

- File: `modules/fundamental/src/advisory/endpoints/get.rs`, line with `.unwrap_or(0)`
- No validation error path exists in the code
- `AppError` is imported but not used for threshold validation
- The `unwrap_or(0)` silently treats any unrecognized threshold as "critical"

## Conclusion

This criterion is NOT met. Invalid threshold values are silently accepted instead of returning a 400 Bad Request error. This is a significant correctness issue -- clients sending invalid values will receive misleading filtered results rather than being informed of their error.
