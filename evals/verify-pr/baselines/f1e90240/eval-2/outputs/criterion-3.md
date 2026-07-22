# Criterion 3: `GET /api/v2/sbom/{id}/advisory-summary?threshold=invalid` returns 400 Bad Request

## Verdict: FAIL

## Analysis

The PR handles invalid threshold values with the following logic:

```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .unwrap_or(0);
```

When an invalid threshold value (e.g., `?threshold=invalid`) is provided:

1. `threshold.to_lowercase()` produces `"invalid"`
2. `.position(|&s| s == "invalid")` returns `None` because `"invalid"` is not in `["critical", "high", "medium", "low"]`
3. `.unwrap_or(0)` silently converts the `None` to index `0`
4. Index `0` corresponds to `"critical"`, so the endpoint treats the invalid value as if `?threshold=critical` was provided

This means **any invalid threshold value is silently accepted** and treated as equivalent to `threshold=critical`. The endpoint returns a 200 OK response with (attempted) critical-only filtering instead of the required 400 Bad Request error.

### Expected behavior

The task description explicitly states:
- "Reuse `common/src/error.rs::AppError` for validation errors (return 400 for invalid threshold values)"

The correct implementation should validate the threshold value and return an `AppError` (which maps to 400 Bad Request) when the value does not match any valid severity level. For example:

```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .ok_or_else(|| AppError::BadRequest(
        format!("Invalid threshold '{}'. Valid values: critical, high, medium, low", threshold)
    ))?;
```

## Conclusion

This criterion is **not satisfied**. Invalid threshold values are silently accepted via `unwrap_or(0)` instead of producing a 400 Bad Request response. No input validation exists.
