# Criterion 3: Invalid threshold returns 400 Bad Request

**Criterion:** `GET /api/v2/sbom/{id}/advisory-summary?threshold=invalid` returns 400 Bad Request

**Verdict: FAIL**

## Detailed Reasoning

The PR does not validate the threshold parameter value. When an invalid threshold is provided, the code silently accepts it instead of returning a 400 Bad Request error.

The relevant code:

```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .unwrap_or(0);
```

The `position()` method returns `None` when the threshold value is not found in the `severity_order` array. Instead of treating this as a validation error and returning a 400 Bad Request response, the code uses `.unwrap_or(0)` which silently defaults to index 0 (corresponding to "critical").

This means:
- `?threshold=invalid` silently behaves as `?threshold=critical`
- `?threshold=xyz` silently behaves as `?threshold=critical`
- `?threshold=` (empty string) silently behaves as `?threshold=critical`
- Any misspelling like `?threshold=hihg` silently behaves as `?threshold=critical`

**What should happen:** The code should check whether `position()` returns `None` and, if so, return an `AppError` that maps to a 400 Bad Request response. The task's Implementation Notes explicitly state: "Reuse `common/src/error.rs::AppError` for validation errors (return 400 for invalid threshold values)."

A correct implementation would look something like:

```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .ok_or_else(|| AppError::bad_request(format!(
        "Invalid threshold '{}'. Valid values: critical, high, medium, low",
        threshold
    )))?;
```

## Evidence

- File: `modules/fundamental/src/advisory/endpoints/get.rs`, diff line with `.unwrap_or(0)`
- No error path exists for invalid threshold values
- No use of `AppError` for threshold validation despite the task's Implementation Notes requiring it
- The task explicitly lists `common/src/error.rs::AppError` as the mechanism for validation errors
