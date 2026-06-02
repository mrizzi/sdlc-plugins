# Criterion 3: Invalid threshold returns 400 Bad Request

**Criterion:** `GET /api/v2/sbom/{id}/advisory-summary?threshold=invalid` returns 400 Bad Request

**Verdict:** FAIL

## Analysis

The PR diff shows the threshold parsing logic:

```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .unwrap_or(0);
```

When an invalid threshold value is provided (e.g., `?threshold=invalid`), the `.position()` call returns `None` because "invalid" does not match any entry in `["critical", "high", "medium", "low"]`. The code then uses `.unwrap_or(0)`, which silently defaults to index 0 (the "critical" position).

This means:
- An invalid threshold like `?threshold=invalid` silently behaves as if `?threshold=critical` was specified
- No validation error is returned
- No 400 Bad Request status code is generated
- The `AppError` type from `common/src/error.rs` is available but not used for this validation

The task explicitly requires that invalid threshold values return a 400 Bad Request response. The implementation should validate the threshold value and return an error like:

```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .ok_or_else(|| AppError::bad_request(format!("Invalid threshold: {}", threshold)))?;
```

**Result:** FAIL -- Invalid threshold values are silently accepted instead of returning 400 Bad Request.
