## Criterion 3: `GET /api/v2/sbom/{id}/advisory-summary?threshold=invalid` returns 400 Bad Request

**Verdict: FAIL**

### Analysis

The task requires that an invalid threshold value (e.g., `?threshold=invalid`) results in a 400 Bad Request response. The implementation notes explicitly state: "Reuse `common/src/error.rs::AppError` for validation errors (return 400 for invalid threshold values)."

The diff in `modules/fundamental/src/advisory/endpoints/get.rs` does NOT validate the threshold value. Instead, it uses `.unwrap_or(0)` when looking up the threshold in the severity ordering:

```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .unwrap_or(0);
```

When an invalid threshold value like `"invalid"` is provided:
1. `.position(...)` returns `None` because "invalid" is not in the `["critical", "high", "medium", "low"]` array
2. `.unwrap_or(0)` silently falls back to index 0 (which corresponds to "critical")
3. The endpoint returns a 200 OK response with filtering applied as if `threshold=critical` was specified

This means invalid input is silently accepted and treated as a valid request, rather than returning a 400 error. No `AppError::BadRequest` or equivalent validation error is raised.

### Expected Behavior

The implementation should check whether the provided threshold value is a valid severity level. If not, it should return an error:

```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .ok_or_else(|| AppError::BadRequest(format!("Invalid threshold value: {}", threshold)))?;
```

### Evidence

- The `.unwrap_or(0)` on line ~46 of the diff silently converts invalid input to index 0
- No `AppError` or error return path exists for invalid threshold values
- The task's Implementation Notes explicitly require using `AppError` for validation errors

### Conclusion

This criterion is NOT satisfied. Invalid threshold values are silently accepted instead of producing a 400 Bad Request response.
