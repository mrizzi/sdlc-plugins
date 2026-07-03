# Criterion 3: `GET /api/v2/sbom/{id}/advisory-summary?threshold=invalid` returns 400 Bad Request

## Verdict: FAIL

## Analysis

The task requires that providing an invalid threshold value (e.g., `?threshold=invalid`) returns a 400 Bad Request error response. The implementation notes specify: "Reuse `common/src/error.rs::AppError` for validation errors (return 400 for invalid threshold values)."

The implementation does NOT validate the threshold value. Instead, it uses `.unwrap_or(0)` to silently default to index 0 when the threshold string does not match any known severity:

```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .unwrap_or(0);
```

When `threshold=invalid`:
1. `"invalid".to_lowercase()` produces `"invalid"`
2. `severity_order.iter().position(|&s| s == "invalid")` returns `None` (no match)
3. `.unwrap_or(0)` converts `None` to `0` (the index for "critical")
4. The endpoint silently treats `invalid` as equivalent to `threshold=critical`

This is a correctness defect: instead of returning a 400 Bad Request error, the endpoint silently accepts any string and defaults to filtering as if `threshold=critical` were specified. The caller receives a 200 OK response with no indication that the provided threshold was unrecognized.

The correct implementation should:
1. Check if the threshold string matches a known severity
2. If not, return an error using `AppError` (as specified in the Implementation Notes)
3. The error should be a 400 Bad Request with a message indicating the valid threshold values

## Evidence

- File: `modules/fundamental/src/advisory/endpoints/get.rs`
- Line: `let threshold_idx = severity_order.iter().position(|&s| s == threshold.to_lowercase()).unwrap_or(0);`
- `.unwrap_or(0)` silently accepts invalid input instead of returning 400
- No `AppError` usage for invalid threshold validation
- The `AppError` type is imported (`use common::error::AppError;`) but never used for threshold validation
