# Criterion 3: `GET /api/v2/sbom/{id}/advisory-summary?threshold=invalid` returns 400 Bad Request

## Verdict: FAIL

## Analysis

The code does not validate the threshold parameter value. When an invalid threshold is provided (e.g., `?threshold=invalid`), the code uses `.unwrap_or(0)` to silently default to index 0:

```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .unwrap_or(0);
```

When `position()` returns `None` (because "invalid" is not found in `["critical", "high", "medium", "low"]`), `unwrap_or(0)` sets `threshold_idx` to 0, which corresponds to "critical". This means invalid threshold values are silently treated as `threshold=critical` instead of returning a 400 Bad Request error.

The task's Implementation Notes explicitly state: "Reuse `common/src/error.rs::AppError` for validation errors (return 400 for invalid threshold values)". The implementation ignores this guidance entirely.

The correct implementation should check whether the threshold value is valid and return an `AppError` (400 Bad Request) if it is not, for example:

```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .ok_or_else(|| AppError::BadRequest(format!("Invalid threshold: {}", threshold)))?;
```

The criterion is not satisfied.
