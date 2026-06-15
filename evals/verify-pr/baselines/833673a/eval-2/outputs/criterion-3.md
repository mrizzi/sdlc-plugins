# Criterion 3: `GET /api/v2/sbom/{id}/advisory-summary?threshold=invalid` returns 400 Bad Request

## Verdict: FAIL

## Analysis

The acceptance criterion requires that providing an invalid threshold value (e.g., `?threshold=invalid`) returns a 400 Bad Request HTTP response. The implementation does NOT satisfy this requirement.

When an invalid threshold value is provided, the code attempts to find it in the `severity_order` array:

```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .unwrap_or(0);
```

The `.position()` call returns `None` when the value is not found in the array. Instead of returning an error, the code uses `.unwrap_or(0)` to silently default to index 0 (which corresponds to "critical"). This means:

1. An invalid threshold like `?threshold=invalid` is silently treated as `?threshold=critical`
2. No 400 Bad Request response is ever generated
3. No validation error is raised via the `AppError` mechanism
4. The caller receives a 200 OK with filtered results, with no indication that their input was invalid

The task's Implementation Notes explicitly state: "Reuse `common/src/error.rs::AppError` for validation errors (return 400 for invalid threshold values)". This guidance was not followed.

The correct implementation should:
1. Check if the threshold value is valid before proceeding
2. Return an `AppError` (which maps to 400 Bad Request) when the value is not one of "critical", "high", "medium", or "low"

## Evidence

- File: `modules/fundamental/src/advisory/endpoints/get.rs`
- Line: `.unwrap_or(0)` silently converts invalid input to index 0 instead of returning an error
- No `AppError` or 400-related error handling exists in the threshold processing code
- The `common/src/error.rs::AppError` import exists but is not used for threshold validation
