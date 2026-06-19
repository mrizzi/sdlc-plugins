# Criterion 3: `GET /api/v2/sbom/{id}/advisory-summary?threshold=invalid` returns 400 Bad Request

## Verdict: FAIL

## Reasoning

The code does not validate the threshold parameter against the set of allowed values. The relevant code is:

```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .unwrap_or(0);
```

When an invalid threshold value is provided (e.g., `?threshold=invalid`):
1. `severity_order.iter().position(...)` returns `None` because "invalid" does not match any of ["critical", "high", "medium", "low"]
2. `.unwrap_or(0)` silently converts `None` to `0`, treating the invalid value as equivalent to "critical"

No error is returned. The endpoint produces a 200 OK response with filtered data as if `threshold=critical` were specified.

### What should happen

The task requires returning a 400 Bad Request for unrecognized threshold values. The implementation should validate the threshold string and return an `AppError` (which maps to HTTP 400) when the value is not one of the recognized severities. For example:

```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .ok_or_else(|| AppError::BadRequest(format!("Invalid threshold: {}", threshold)))?;
```

### Conclusion

Invalid threshold values are silently accepted and treated as "critical" instead of returning 400 Bad Request. This criterion is not satisfied.
