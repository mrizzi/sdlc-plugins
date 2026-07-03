# Criterion 3: `GET /api/v2/sbom/{id}/advisory-summary?threshold=invalid` returns 400 Bad Request

## Verdict: FAIL

## Analysis

The task requires that passing an invalid threshold value (e.g., `?threshold=invalid`) returns an HTTP 400 Bad Request error. The Implementation Notes explicitly state: "Reuse `common/src/error.rs::AppError` for validation errors (return 400 for invalid threshold values)."

### Code Inspection

In `modules/fundamental/src/advisory/endpoints/get.rs`, the threshold value is resolved using:

```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .unwrap_or(0);
```

The `.position()` method returns `None` when the threshold string does not match any entry in the `severity_order` array (i.e., it is not one of "critical", "high", "medium", "low"). The `.unwrap_or(0)` then silently defaults to index 0, which corresponds to "critical".

### Why This Fails

Instead of returning a 400 Bad Request error for invalid input, the code silently treats any unrecognized threshold value as "critical". For example:

- `?threshold=invalid` is silently treated as `?threshold=critical`
- `?threshold=xyz` is silently treated as `?threshold=critical`
- `?threshold=` (empty string) is silently treated as `?threshold=critical`

This violates the acceptance criterion and the Implementation Notes. The correct behavior would be to detect the `None` return from `.position()` and return an `AppError` with a 400 status code. For example:

```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .ok_or_else(|| AppError::BadRequest(format!("Invalid threshold value: {}", threshold)))?;
```

### Evidence

- **File:** `modules/fundamental/src/advisory/endpoints/get.rs`, line 45 of the diff
- **Bug:** `.unwrap_or(0)` silently accepts any string as a valid threshold
- **Expected behavior:** Return `AppError` (400 Bad Request) for values not in ["critical", "high", "medium", "low"]
- **Implementation Notes reference:** "Reuse `common/src/error.rs::AppError` for validation errors (return 400 for invalid threshold values)"
- **Repository context:** `common/src/error.rs` contains the `AppError` enum which implements `IntoResponse` -- the infrastructure for proper error responses already exists
