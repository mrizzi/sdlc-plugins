# Criterion 3: `GET /api/v2/sbom/{id}/advisory-summary?threshold=invalid` returns 400 Bad Request

## Result: FAIL

## Reasoning

The code does not validate the threshold parameter value. When an invalid value such as `threshold=invalid` is provided, the lookup in the severity order array fails:

```rust
let severity_order = ["critical", "high", "medium", "low"];
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .unwrap_or(0);
```

The `.position()` call returns `None` for any value not in `["critical", "high", "medium", "low"]`. Instead of returning a 400 Bad Request error, the code uses `.unwrap_or(0)` which silently falls back to index 0 ("critical"). This means any invalid threshold value is silently treated as `threshold=critical`.

The task's implementation notes explicitly state: "Reuse `common/src/error.rs::AppError` for validation errors (return 400 for invalid threshold values)." The implementation ignores this guidance entirely.

The correct implementation should:
1. Check whether the threshold value matches one of the valid severity levels
2. If not, return `Err(AppError::BadRequest("Invalid threshold value: ..."))` or equivalent
3. Only proceed with filtering if the value is valid

As implemented, there is no way for a client to detect that they provided a typo in the threshold parameter -- the endpoint silently returns a result as if the threshold were "critical".
