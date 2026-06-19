# Criterion 3: `GET /api/v2/sbom/{id}/advisory-summary?threshold=invalid` returns 400 Bad Request

## What was checked

Inspected the PR diff for validation of the `threshold` parameter value. Specifically looked for any code that returns a 400 error when an invalid threshold value is provided.

## Evidence

The filtering logic in `get.rs` when a threshold is provided:

```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .unwrap_or(0);
```

When an invalid value like `"invalid"` is passed:
- `severity_order.iter().position(...)` returns `None` because "invalid" is not in the array
- `.unwrap_or(0)` silently defaults to index 0, which corresponds to "critical"

This means an invalid threshold value is silently treated as `threshold=critical` instead of returning a 400 Bad Request error. There is no validation, no error return, and no use of `AppError` for this case.

The task's Implementation Notes explicitly state: "Reuse `common/src/error.rs::AppError` for validation errors (return 400 for invalid threshold values)". This guidance was not followed.

## Verdict: FAIL

The implementation silently accepts invalid threshold values by defaulting to index 0 (critical) via `unwrap_or(0)`. No validation is performed and no 400 Bad Request is returned for invalid input. The acceptance criterion is not satisfied.
