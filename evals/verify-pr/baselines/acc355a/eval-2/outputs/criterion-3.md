## Criterion 3: `GET /api/v2/sbom/{id}/advisory-summary?threshold=invalid` returns 400 Bad Request

**Result: FAIL**

### Evidence

The task explicitly requires that invalid threshold values return a 400 Bad Request error. The implementation notes state: "Reuse `common/src/error.rs::AppError` for validation errors (return 400 for invalid threshold values)."

However, the diff uses `unwrap_or(0)` when looking up the threshold value in the severity order array:

```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .unwrap_or(0);
```

When an invalid threshold value like `"invalid"` is passed, `.position()` returns `None`, and `unwrap_or(0)` silently converts it to index 0 (which corresponds to "critical"). This means an invalid threshold is silently treated as `threshold=critical` instead of returning a 400 Bad Request error.

The correct implementation should:
1. Check if the threshold value matches one of the valid severity levels
2. If not, return `Err(AppError::BadRequest("Invalid threshold value"))` or equivalent

There is no validation logic anywhere in the diff, and no 400 error is ever returned for invalid input. This is a clear gap.
