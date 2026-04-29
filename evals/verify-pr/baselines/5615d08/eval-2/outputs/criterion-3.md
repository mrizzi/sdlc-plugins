# Criterion 3: Invalid threshold returns 400 Bad Request

**Criterion:** `GET /api/v2/sbom/{id}/advisory-summary?threshold=invalid` returns 400 Bad Request

**Verdict: FAIL**

## Reasoning

The PR diff does **not** implement validation of the threshold parameter value. When an invalid threshold value is provided (e.g., `?threshold=invalid`), the code uses `unwrap_or(0)`:

```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .unwrap_or(0);
```

When `position()` returns `None` (because "invalid" does not match any entry in `severity_order`), `unwrap_or(0)` silently defaults to index `0`, which corresponds to "critical". This means an invalid threshold value like `?threshold=invalid` will behave identically to `?threshold=critical`, returning only the critical count -- rather than returning a 400 Bad Request error.

The task description explicitly requires returning 400 Bad Request for invalid threshold values. The Implementation Notes also specify: "Reuse `common/src/error.rs::AppError` for validation errors (return 400 for invalid threshold values)". Neither `AppError` nor any other error mechanism is used for threshold validation in the diff.

The correct implementation should check whether the threshold value matches one of the valid severity levels and, if not, return an `AppError` that maps to HTTP 400.

## Evidence

- `unwrap_or(0)` on line where threshold index is computed -- silently accepts any string
- No reference to `AppError` for threshold validation anywhere in the handler's filtering logic
- No `return Err(...)` or `?` operator for invalid threshold values
- The task's Implementation Notes explicitly say: "Reuse `common/src/error.rs::AppError` for validation errors (return 400 for invalid threshold values)"
