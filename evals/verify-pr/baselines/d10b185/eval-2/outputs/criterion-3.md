# Criterion 3: `GET /api/v2/sbom/{id}/advisory-summary?threshold=invalid` returns 400 Bad Request

## Verdict: FAIL

## Analysis

The PR does not implement any validation for invalid threshold values. The task explicitly requires returning a 400 Bad Request response for invalid threshold values, and the implementation notes reference `common/src/error.rs::AppError` for this purpose.

Instead, the code uses `unwrap_or(0)` to silently handle unrecognized threshold values:

```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .unwrap_or(0);
```

When an invalid threshold like `"invalid"` is provided, `.position()` returns `None`, and `.unwrap_or(0)` silently falls back to index 0 (which corresponds to `"critical"`). This means:

1. No 400 error is returned -- the request succeeds with a 200 status
2. The invalid value is silently treated as `threshold=critical`
3. The caller has no way to know their input was rejected or misinterpreted

The correct implementation should check whether the threshold value is one of the valid options (`critical`, `high`, `medium`, `low`) and return `AppError::BadRequest` (or equivalent 400 response) if it is not, as described in the Implementation Notes section of the task.

Additionally, the test file `tests/api/advisory_summary.rs` is entirely missing from the diff, so there is no test for the invalid threshold case (Test Requirements specify "Test invalid threshold value returns 400").

## Evidence

- `get.rs` line 44-46: `.unwrap_or(0)` silently accepts any string, including invalid ones
- No `AppError::BadRequest` or equivalent 400 response anywhere in the diff
- No test file `tests/api/advisory_summary.rs` in the diff
- Task Implementation Notes: "Reuse `common/src/error.rs::AppError` for validation errors (return 400 for invalid threshold values)"
