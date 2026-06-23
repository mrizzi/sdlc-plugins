# Criterion 3 Analysis

**Acceptance Criterion:** `GET /api/v2/sbom/{id}/advisory-summary?threshold=invalid` returns 400 Bad Request

**Verdict: FAIL**

## Evidence from the Diff

The threshold parameter handling in `modules/fundamental/src/advisory/endpoints/get.rs` uses `unwrap_or(0)` for unrecognized values:

```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .unwrap_or(0);
```

### Behavior for Invalid Input

When `threshold=invalid` is provided:
1. `threshold.to_lowercase()` produces `"invalid"`
2. `severity_order.iter().position(|&s| s == "invalid")` returns `None` because "invalid" is not in `["critical", "high", "medium", "low"]`
3. `.unwrap_or(0)` converts `None` to `0`
4. `threshold_idx = 0` means the code treats the invalid input as equivalent to `threshold=critical`

The handler then returns a 200 OK response with filtered counts (only critical) instead of returning a 400 Bad Request error.

### What the Implementation Should Do

Per the task's Implementation Notes: "Reuse `common/src/error.rs::AppError` for validation errors (return 400 for invalid threshold values)". The correct implementation would:

1. Check whether the threshold value matches a known severity
2. If not, return an `AppError` with a 400 status code, e.g.:
   ```rust
   let threshold_idx = severity_order.iter()
       .position(|&s| s == threshold.to_lowercase())
       .ok_or_else(|| AppError::BadRequest(format!("Invalid threshold value: {}", threshold)))?;
   ```

### Conclusion

Invalid threshold values are silently accepted and treated as `threshold=critical` due to the `unwrap_or(0)` fallback. The endpoint never returns 400 Bad Request for invalid input. This criterion is not satisfied.
