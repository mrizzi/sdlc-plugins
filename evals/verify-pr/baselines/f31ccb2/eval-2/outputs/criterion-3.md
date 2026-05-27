## Criterion 3: `GET /api/v2/sbom/{id}/advisory-summary?threshold=invalid` returns 400 Bad Request

**Verdict: FAIL**

### Analysis

The diff does NOT validate the threshold parameter value. When an invalid threshold string (e.g., `?threshold=invalid`) is provided, the code silently accepts it via `unwrap_or(0)`:

```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .unwrap_or(0);
```

When `.position()` returns `None` (because the value is not found in `["critical", "high", "medium", "low"]`), the code defaults to index `0` (the position for "critical"). This means an invalid threshold value is silently treated as `threshold=critical` instead of returning a 400 Bad Request error.

### What should happen

The task explicitly requires:
- "Reuse `common/src/error.rs::AppError` for validation errors (return 400 for invalid threshold values)"

The correct implementation would check whether `.position()` returned `None` and, if so, return an `Err(AppError::BadRequest(...))` or equivalent 400-status error response. For example:

```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .ok_or_else(|| AppError::BadRequest(format!("Invalid threshold value: {}", threshold)))?;
```

### Impact

Users providing typos or incorrect values (e.g., `?threshold=hig`, `?threshold=critical!`, `?threshold=5`) will receive a 200 OK response with results filtered as if `threshold=critical` was specified, with no indication that their input was invalid. This is a usability and correctness defect.
