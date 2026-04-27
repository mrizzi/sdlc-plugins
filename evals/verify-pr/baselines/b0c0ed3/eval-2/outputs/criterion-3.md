## Criterion 3: `GET /api/v2/sbom/{id}/advisory-summary?threshold=invalid` returns 400 Bad Request

### Result: FAIL

### Analysis

The implementation does not validate the `threshold` parameter. When an invalid value such as `threshold=invalid` is provided, the following code executes:

```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .unwrap_or(0);
```

The `.position()` call searches for the threshold value in the `["critical", "high", "medium", "low"]` array. For the input `"invalid"`, no match is found and `.position()` returns `None`. The `.unwrap_or(0)` then silently converts this to index 0, which corresponds to `"critical"`.

This means any invalid threshold value is silently treated as `threshold=critical` instead of returning a 400 Bad Request error. The API consumer receives a successful response with no indication that their input was invalid.

The task acceptance criteria explicitly require a 400 Bad Request response for invalid threshold values. The implementation notes reference using `common/src/error.rs::AppError` for validation errors. The correct implementation should:

1. Check whether the threshold value matches one of the recognized severity levels (critical, high, medium, low)
2. If it does not match, return an error such as `Err(AppError::BadRequest("Invalid threshold value".into()))`
3. Only proceed with filtering if the threshold value is valid

No input validation logic exists in the PR diff. This criterion is clearly not met.
