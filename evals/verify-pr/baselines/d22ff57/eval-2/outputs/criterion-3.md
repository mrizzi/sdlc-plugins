# Criterion 3

**Text**: `GET /api/v2/sbom/{id}/advisory-summary?threshold=invalid` returns 400 Bad Request

**Evidence from diff**:

The diff shows the following handling when a threshold value is provided:

```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .unwrap_or(0);
```

When an invalid threshold value is passed (e.g., `threshold=invalid`), `.position()` returns `None`, and `.unwrap_or(0)` silently defaults to index 0 (which corresponds to "critical"). The code does not return a 400 Bad Request error. Instead, it silently treats the invalid value as if the user had passed `threshold=critical`.

The task's implementation notes explicitly state: "Reuse `common/src/error.rs::AppError` for validation errors (return 400 for invalid threshold values)." This was not implemented.

There is no validation, no `AppError` usage for invalid input, and no 400 response anywhere in the diff.

**Verdict**: FAIL
