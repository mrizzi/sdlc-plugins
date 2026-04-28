# Criterion 3: `GET /api/v2/sbom/{id}/advisory-summary?threshold=invalid` returns 400 Bad Request

## Verdict: FAIL

## Analysis

The PR diff does NOT validate the threshold parameter. When an invalid value is provided (e.g., `?threshold=invalid`), the code uses `unwrap_or(0)` to silently default to index 0 (which corresponds to "critical"):

```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .unwrap_or(0);
```

The `.position()` call returns `None` when the threshold string doesn't match any entry in the `severity_order` array. Instead of returning a 400 Bad Request error, `unwrap_or(0)` silently treats the invalid value as if `threshold=critical` was specified.

The task's Implementation Notes explicitly state: "Reuse `common/src/error.rs::AppError` for validation errors (return 400 for invalid threshold values)". The implementation ignores this requirement entirely.

## Evidence

The code should check if the threshold value is valid and return an `AppError` (which maps to 400 Bad Request) for invalid values. Instead, it silently falls back to index 0:

```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .unwrap_or(0);  // Silent fallback instead of 400 error
```

There is no error handling code, no use of `AppError` for validation, and no path that returns a 400 status code for invalid threshold values.
