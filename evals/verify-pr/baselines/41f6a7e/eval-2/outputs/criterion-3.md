# Criterion 3: `GET /api/v2/sbom/{id}/advisory-summary?threshold=invalid` returns 400 Bad Request

## Verdict: FAIL

## Analysis

When an invalid threshold value is provided (e.g., `threshold=invalid`), the code executes:

```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .unwrap_or(0);
```

The `.position()` call returns `None` because `"invalid"` does not match any entry in `["critical", "high", "medium", "low"]`. The `.unwrap_or(0)` then silently converts this to index 0, which corresponds to "critical". The endpoint proceeds to return a 200 OK response with filtering applied as if `threshold=critical` had been specified.

The acceptance criterion requires that invalid threshold values return a 400 Bad Request error. The implementation has no validation of the threshold parameter and no error return path for invalid values. The task's Implementation Notes specify reusing `common/src/error.rs::AppError` for validation errors, but no such error handling was implemented.

## Evidence

- File: `modules/fundamental/src/advisory/endpoints/get.rs`
- Code: `.unwrap_or(0)` silently converts unrecognized threshold values to index 0
- No `AppError` or 400 status code return exists for invalid threshold values
- The task explicitly states: "Reuse `common/src/error.rs::AppError` for validation errors (return 400 for invalid threshold values)"
