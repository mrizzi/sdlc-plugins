# Criterion 3: `GET /api/v2/sbom/{id}/advisory-summary?threshold=invalid` returns 400 Bad Request

## Result: FAIL

## Analysis

The diff in `modules/fundamental/src/advisory/endpoints/get.rs` handles the threshold parameter lookup as follows:

```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .unwrap_or(0);
```

When an invalid threshold value is provided (e.g., `?threshold=invalid`), the `.position()` call returns `None` because "invalid" does not match any of `["critical", "high", "medium", "low"]`. The `.unwrap_or(0)` then silently defaults to index 0, which corresponds to "critical".

This means that any invalid threshold value (e.g., "invalid", "foo", "123", "extreme") is silently treated as `threshold=critical` instead of returning a 400 Bad Request error.

The task's Implementation Notes explicitly state: "Reuse `common/src/error.rs::AppError` for validation errors (return 400 for invalid threshold values)". The diff does not use `AppError` for validation at all.

### What correct implementation would look like

The code should check if the threshold value is valid and return an error if not:

```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .ok_or_else(|| AppError::BadRequest(format!("Invalid threshold: {}", threshold)))?;
```

This would use the `?` operator to propagate a 400 Bad Request error when the threshold is not recognized.

## Evidence

- File: `modules/fundamental/src/advisory/endpoints/get.rs`
- `.unwrap_or(0)` on the position lookup silently accepts any string
- No `AppError::BadRequest` or any 400-related error handling in the diff
- Task Implementation Notes specify returning 400 for invalid threshold values

## Conclusion

The criterion is not met. Invalid threshold values are silently accepted and treated as "critical" instead of producing a 400 Bad Request response. This is a significant correctness and API contract issue -- callers with typos in the threshold value would receive filtered results without any indication that their parameter was invalid.
