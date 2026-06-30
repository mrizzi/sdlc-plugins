## Criterion 3: `GET /api/v2/sbom/{id}/advisory-summary?threshold=invalid` returns 400 Bad Request

**Verdict: FAIL**

### Reasoning

The code does NOT validate the threshold parameter against valid severity values. When an invalid threshold value is provided (e.g., `?threshold=invalid`), the following code executes:

```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .unwrap_or(0);
```

The `.position()` call returns `None` for an invalid value (since "invalid" is not in the `severity_order` array), and `.unwrap_or(0)` silently defaults to index 0 (which corresponds to "critical"). This means an invalid threshold value is treated as `threshold=critical` instead of returning a 400 Bad Request error.

The task's Implementation Notes explicitly state: "Reuse `common/src/error.rs::AppError` for validation errors (return 400 for invalid threshold values)". This guidance was not followed.

The correct implementation should:
1. Check if the threshold value is in the valid set `["critical", "high", "medium", "low"]`
2. If not, return `Err(AppError::BadRequest("Invalid threshold value"))` or equivalent
3. Only proceed with filtering if the value is valid

### Evidence

- File: `modules/fundamental/src/advisory/endpoints/get.rs`
- Line: `.unwrap_or(0)` silently accepts any string value without validation
- No `AppError::BadRequest` or similar 400 response is returned for invalid input
- The task explicitly required 400 Bad Request for invalid threshold values
- The task's Implementation Notes referenced `common/src/error.rs::AppError` for validation errors
