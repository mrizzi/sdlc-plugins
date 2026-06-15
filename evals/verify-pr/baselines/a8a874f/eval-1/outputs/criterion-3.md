# Criterion 3: `GET /api/v2/package?license=INVALID-999` returns 400 Bad Request with an error message

## Verdict: PASS

## Reasoning

The `validate_license_param` function validates each license identifier by parsing it as an SPDX expression:

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

When `Expression::parse(id)` fails for an invalid identifier like `INVALID-999`, the function returns `AppError::BadRequest` with a descriptive error message including the invalid identifier. The `?` operator propagates this error to the handler, which returns a 400 response. This follows the error handling pattern documented in the repository's `common/src/error.rs` (`AppError` enum implements `IntoResponse`).

The integration test `test_list_packages_invalid_license_returns_400` sends a request with `?license=INVALID-999` and asserts that the response status is `StatusCode::BAD_REQUEST`.

This criterion is satisfied by both the implementation and the test coverage.
