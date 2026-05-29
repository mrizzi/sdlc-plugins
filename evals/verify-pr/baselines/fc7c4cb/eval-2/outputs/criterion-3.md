## Criterion 3

**Text:** `GET /api/v2/sbom/{id}/advisory-summary?threshold=invalid` returns 400 Bad Request

**What I checked:** How the code handles an unrecognized threshold value in `modules/fundamental/src/advisory/endpoints/get.rs`.

**Code evidence:**

```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .unwrap_or(0);
```

When `threshold=invalid` is provided, `position()` returns `None` because "invalid" does not match any entry in `["critical", "high", "medium", "low"]`. The code then calls `.unwrap_or(0)`, which silently defaults the threshold index to 0 (equivalent to "critical").

There is no validation branch that returns a 400 Bad Request error. The task's implementation notes explicitly state: "Reuse `common/src/error.rs::AppError` for validation errors (return 400 for invalid threshold values)." This was not implemented.

The correct implementation should check if `position()` returns `None` and, in that case, return an `AppError` variant that maps to HTTP 400 (e.g., `AppError::BadRequest`). Instead, invalid input is silently accepted and treated as a "critical" threshold filter.

**Verdict: FAIL**

Invalid threshold values are silently accepted via `unwrap_or(0)` instead of returning 400 Bad Request. No validation logic exists.
