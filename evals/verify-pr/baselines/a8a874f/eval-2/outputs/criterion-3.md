# Criterion 3: Invalid threshold returns 400 Bad Request

**Criterion:** `GET /api/v2/sbom/{id}/advisory-summary?threshold=invalid` returns 400 Bad Request

**Verdict:** FAIL

## Reasoning

The diff in `modules/fundamental/src/advisory/endpoints/get.rs` does NOT validate the threshold parameter value. When an invalid value is provided (e.g., `threshold=invalid`), the code silently falls through to a default behavior via `unwrap_or(0)`:

```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .unwrap_or(0);
```

The `position()` method returns `None` when the provided threshold does not match any entry in the `severity_order` array. Instead of returning a 400 Bad Request error, `unwrap_or(0)` silently converts the invalid input to index 0, which corresponds to "critical". This means:

- `?threshold=invalid` behaves identically to `?threshold=critical`
- `?threshold=foo` behaves identically to `?threshold=critical`
- `?threshold=` (empty string) behaves identically to `?threshold=critical`

The task explicitly requires: "Reuse `common/src/error.rs::AppError` for validation errors (return 400 for invalid threshold values)." The implementation notes reference `AppError` which is already imported in the file (`use common::error::AppError`), but the code never uses it for threshold validation.

The correct implementation should check whether `position()` returns `None` and, if so, return an `AppError` that maps to HTTP 400 Bad Request. For example:

```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .ok_or_else(|| AppError::bad_request(format!("Invalid threshold value: {}", threshold)))?;
```

## Evidence

- File: `modules/fundamental/src/advisory/endpoints/get.rs`
- The `unwrap_or(0)` on line 46 of the diff silently converts invalid input to index 0.
- No 400 error response is generated for invalid threshold values.
- The `AppError` type is imported but unused for validation.
- The Implementation Notes explicitly call for using `AppError` for validation errors returning 400.
