# Criterion 3: `?threshold=invalid` returns 400 Bad Request

## Verdict: FAIL

## Analysis

The code does not validate the threshold parameter value. Invalid values are silently accepted and treated as if `threshold=critical` was specified.

### Code Under Review

```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .unwrap_or(0);
```

### Trace for threshold="invalid"

1. `threshold.to_lowercase()` produces `"invalid"`.
2. `severity_order.iter().position(|&s| s == "invalid")` returns `None` because "invalid" is not in `["critical", "high", "medium", "low"]`.
3. `.unwrap_or(0)` converts the `None` to `0`, which is the index for "critical".
4. The handler proceeds normally, returning a 200 response with filtered data.

### Expected Behavior

Per the task specification and implementation notes, the endpoint should:
- Return HTTP 400 Bad Request for invalid threshold values
- Use `common::error::AppError` for the validation error (as noted in the Implementation Notes: "Reuse `common/src/error.rs::AppError` for validation errors (return 400 for invalid threshold values)")

### What Should Have Been Implemented

The code should check whether `position()` returns `None` and, if so, return an `AppError` that maps to a 400 status code. For example:

```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .ok_or_else(|| AppError::BadRequest(format!("Invalid threshold value: {}", threshold)))?;
```

### Conclusion

Any arbitrary string (e.g., "invalid", "foo", "xyz") is silently accepted with no error, violating the requirement for 400 Bad Request on invalid input. This is a validation gap that could confuse API consumers who send typos or unsupported values.
