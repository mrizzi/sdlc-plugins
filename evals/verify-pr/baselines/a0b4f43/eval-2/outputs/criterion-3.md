# Criterion 3: Invalid threshold returns 400 Bad Request

**Criterion:** `GET /api/v2/sbom/{id}/advisory-summary?threshold=invalid` returns 400 Bad Request

**Verdict: FAIL**

## Analysis

The PR diff in `modules/fundamental/src/advisory/endpoints/get.rs` handles the threshold parameter as follows:

```rust
let severity_order = ["critical", "high", "medium", "low"];
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .unwrap_or(0);
```

When an invalid threshold value (e.g., `threshold=invalid`) is provided:

1. `threshold.to_lowercase()` produces `"invalid"`
2. `.position(|&s| s == "invalid")` returns `None` because "invalid" is not in the severity_order array
3. `.unwrap_or(0)` silently converts the `None` to index `0`

This means an invalid threshold value is silently treated as `threshold=critical` (index 0) instead of returning a 400 Bad Request error response. The code does not perform any validation of the threshold value and does not use the `AppError` type for validation errors as specified in the Implementation Notes.

**What should happen:** The task's Implementation Notes explicitly state: "Reuse `common/src/error.rs::AppError` for validation errors (return 400 for invalid threshold values)." The correct implementation would check whether the threshold value matches a known severity level and, if not, return an error:

```rust
// Expected behavior (not implemented):
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .ok_or_else(|| AppError::BadRequest(format!("Invalid threshold: {}", threshold)))?;
```

**Evidence:**
- `.unwrap_or(0)` on line in the filtering logic silently accepts any string
- No validation of the threshold parameter against valid severity values
- No 400 response is returned for invalid values
- `AppError` is imported (`use common::error::AppError;`) but never used for threshold validation
- The Implementation Notes require: "return 400 for invalid threshold values"

This criterion is clearly NOT satisfied. Invalid threshold values are silently accepted rather than rejected with a 400 Bad Request.
