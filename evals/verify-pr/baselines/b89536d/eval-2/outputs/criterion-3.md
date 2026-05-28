## Criterion 3: `GET /api/v2/sbom/{id}/advisory-summary?threshold=invalid` returns 400 Bad Request

**Verdict: FAIL**

### Evidence

The PR diff in `modules/fundamental/src/advisory/endpoints/get.rs` handles an unrecognized threshold value using `unwrap_or(0)`:

```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .unwrap_or(0);
```

When an invalid threshold value is provided (e.g., `?threshold=invalid`), `position()` returns `None` because "invalid" does not match any entry in `["critical", "high", "medium", "low"]`. The `.unwrap_or(0)` then silently defaults to index 0 ("critical"), meaning the endpoint treats an invalid threshold the same as `?threshold=critical`.

### Analysis

This violates the acceptance criterion. The task specification explicitly requires:
- "Return 400 for invalid threshold values" (in both Acceptance Criteria and Implementation Notes)
- The Implementation Notes reference `common/src/error.rs::AppError` for validation errors: "Reuse `common/src/error.rs::AppError` for validation errors (return 400 for invalid threshold values)"

The correct implementation should:
1. Check whether the threshold value matches a valid severity
2. If not, return `Err(AppError::BadRequest("Invalid threshold value: ..."))` or equivalent 400 response
3. Use the existing `AppError` enum from `common/src/error.rs` as specified in the Implementation Notes

Instead, invalid values are silently accepted and treated as `threshold=critical`, which is both incorrect and could confuse API consumers who provide a typo in the threshold parameter. No validation, no `Err(...)` return, and no reference to `AppError::BadRequest` or any 400-producing mechanism exists in the diff.

This criterion is definitively not met.
