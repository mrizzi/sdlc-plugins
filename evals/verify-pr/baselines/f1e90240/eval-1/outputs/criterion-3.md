# Criterion 3: `GET /api/v2/package?license=INVALID-999` returns 400 Bad Request with an error message

## Verdict: PASS

## Analysis

### Code Changes

The `validate_license_param` function in `modules/fundamental/src/package/endpoints/list.rs` validates each license identifier against the `spdx` crate's `Expression::parse`:

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

When `INVALID-999` is passed, `Expression::parse("INVALID-999")` will return an error because it is not a recognized SPDX license expression. The `map_err` converts this into `AppError::BadRequest` with a descriptive error message including the invalid identifier. The `?` operator propagates this error, causing the handler to return a 400 Bad Request response.

The error message format `"Invalid SPDX license identifier: INVALID-999"` provides clear feedback to the API consumer about what went wrong.

### Test Coverage

The test `test_list_packages_invalid_license_returns_400` in `tests/api/package.rs` validates this criterion:
- Sends `GET /api/v2/package?license=INVALID-999`
- Asserts response status is `StatusCode::BAD_REQUEST` (400)

The test confirms the validation rejects invalid SPDX identifiers with a 400 response.

### Conclusion

The implementation follows the task's instruction to "validate license identifiers against a known SPDX license list before querying" and "return `AppError::BadRequest` for invalid values." The validation occurs early in the handler (before any database query), the error message is descriptive, and the test confirms the expected 400 status code.
