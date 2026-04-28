# Criterion 3: Invalid threshold returns 400 Bad Request

## Criterion

`GET /api/v2/sbom/{id}/advisory-summary?threshold=invalid` returns 400 Bad Request.

## Verdict: FAIL

## Reasoning

The task explicitly requires that invalid threshold values return a 400 Bad Request response. The implementation notes further specify: "Reuse `common/src/error.rs::AppError` for validation errors (return 400 for invalid threshold values)."

However, the PR diff does NOT implement any validation of the threshold parameter. Instead, the code uses `.unwrap_or(0)` when looking up the threshold in the severity ordering array:

```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .unwrap_or(0);
```

When an invalid value like `"invalid"` is provided:
1. `.position()` returns `None` because `"invalid"` is not in `["critical", "high", "medium", "low"]`
2. `.unwrap_or(0)` silently converts this to index `0` (the "critical" position)
3. The endpoint returns a 200 OK response with only the critical count, as if `?threshold=critical` was passed

This is a significant gap:
- **No 400 status code** is returned for invalid input
- **No use of `AppError`** for validation as specified in the implementation notes
- **Silent acceptance** of arbitrary values, which is a usability and correctness issue -- a user who mistypes a threshold value (e.g., `?threshold=hgih`) gets filtered results without any indication of an error
- There is no `Severity` enum with validation as recommended in the implementation notes

## Evidence

The `.unwrap_or(0)` on line 46 of the modified `get.rs` is the specific code that silently swallows invalid values. The task required a 400 response, and the `AppError` type from `common/src/error.rs` (already imported in the file) should have been used to return `AppError::BadRequest` or equivalent.

Missing code pattern that should have been implemented (pseudocode):
```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .ok_or_else(|| AppError::bad_request(format!("Invalid threshold value: {}", threshold)))?;
```
