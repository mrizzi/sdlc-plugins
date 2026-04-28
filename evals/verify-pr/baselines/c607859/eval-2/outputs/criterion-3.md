# Criterion 3: `GET /api/v2/sbom/{id}/advisory-summary?threshold=invalid` returns 400 Bad Request

## Verdict: FAIL

## Reasoning

The PR diff handles the threshold parameter with this code:

```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .unwrap_or(0);
```

When an invalid threshold value is provided (e.g., `?threshold=invalid`), the `.position()` call returns `None` because "invalid" does not match any entry in `["critical", "high", "medium", "low"]`. The `.unwrap_or(0)` then silently defaults to index 0, which corresponds to "critical".

This means that `?threshold=invalid` is treated identically to `?threshold=critical` -- it silently returns only critical counts instead of returning a 400 Bad Request error.

The task explicitly requires:
- "Reuse `common/src/error.rs::AppError` for validation errors (return 400 for invalid threshold values)"

The implementation should validate the threshold value against the known severity levels and return an `AppError` (which maps to 400 Bad Request) if the value is not one of `critical`, `high`, `medium`, or `low`. Instead, the code silently accepts any input.

There is no validation logic anywhere in the diff. No `Err(AppError::...)` return for invalid values. No pattern matching with an error case. The `unwrap_or(0)` completely swallows invalid input.

**Conclusion:** This criterion is NOT satisfied. Invalid threshold values are silently accepted and defaulted to "critical" behavior instead of returning 400 Bad Request.
