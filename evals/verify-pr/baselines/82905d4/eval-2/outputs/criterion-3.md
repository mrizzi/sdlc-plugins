# Criterion 3: Invalid threshold returns 400 Bad Request

**Criterion:** `GET /api/v2/sbom/{id}/advisory-summary?threshold=invalid` returns 400 Bad Request

**Result: FAIL**

## Analysis

The PR diff shows the following code for handling the threshold parameter:

```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .unwrap_or(0);
```

When an invalid threshold value is provided (e.g., `threshold=invalid`), the `.position()` call returns `None` because "invalid" does not match any element in the `severity_order` array. The code then uses `.unwrap_or(0)` which silently defaults to index 0 ("critical").

This means that instead of returning a 400 Bad Request error for invalid threshold values, the endpoint silently treats any invalid value as `threshold=critical`. This is incorrect behavior that:

1. Violates the acceptance criterion requiring a 400 Bad Request response
2. Could confuse API consumers who misspell a threshold value and get unexpected results without any error indication
3. Does not use the `AppError` type mentioned in the implementation notes for validation errors

The correct implementation should:
- Check if the threshold value matches one of the valid severity levels
- If not, return an `AppError` with a 400 Bad Request status code
- Include a descriptive error message indicating the valid values

**Conclusion:** Invalid threshold values are silently accepted and defaulted to "critical" instead of returning a 400 Bad Request error. This criterion is **not satisfied**.
