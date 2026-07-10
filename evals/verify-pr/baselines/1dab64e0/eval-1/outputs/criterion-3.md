# Criterion 3: `GET /api/v2/package?license=INVALID-999` returns 400 Bad Request with an error message

## Verdict: PASS

## Analysis

### Code Changes

The `validate_license_param` function validates each license identifier using the `spdx` crate's `Expression::parse`:

```rust
fn validate_license_param(license: &str) -> Result<Vec<String>, AppError> {
    let identifiers: Vec<String> = license.split(',').map(|s| s.trim().to_string()).collect();
    for id in &identifiers {
        Expression::parse(id).map_err(|_| {
            AppError::BadRequest(format!("Invalid SPDX license identifier: {}", id))
        })?;
    }
    Ok(identifiers)
}
```

When `INVALID-999` is passed:
1. The function splits by comma, producing `["INVALID-999"]`
2. `Expression::parse("INVALID-999")` fails because `INVALID-999` is not a recognized SPDX license identifier
3. The error is mapped to `AppError::BadRequest` with the message `"Invalid SPDX license identifier: INVALID-999"`
4. The `?` operator propagates the error, which Axum converts to an HTTP 400 response

The handler uses the early-return pattern via `?`:

```rust
let license_filter = match &params.license {
    Some(license) => Some(validate_license_param(license)?),
    None => None,
};
```

This ensures validation happens before any database query, returning 400 immediately for invalid input.

### Error Handling Pattern

The implementation follows the existing `AppError` pattern documented in the repository structure (`common/src/error.rs` -- `AppError` enum implements `IntoResponse`). The `AppError::BadRequest` variant maps to HTTP 400 with the provided message, consistent with the task's Implementation Notes which specify `AppError::BadRequest`.

### Test Coverage

The test `test_list_packages_invalid_license_returns_400` sends a request with `?license=INVALID-999` and asserts:
- Response status is `StatusCode::BAD_REQUEST` (400)

This directly validates the error handling behavior.

### Conclusion

Invalid SPDX identifiers are caught by the `spdx::Expression::parse` validation, converted to `AppError::BadRequest` with a descriptive error message, and returned as HTTP 400. The test confirms the expected behavior. Criterion is satisfied.
