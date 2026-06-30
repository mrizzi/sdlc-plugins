## Criterion 3: `GET /api/v2/package?license=INVALID-999` returns 400 Bad Request with an error message

**Verdict: PASS**

### Reasoning

The `validate_license_param` function validates each license identifier against the SPDX specification using the `spdx` crate:

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

When `Expression::parse("INVALID-999")` fails (as it is not a recognized SPDX expression), the error is mapped to `AppError::BadRequest` with a descriptive error message: `"Invalid SPDX license identifier: INVALID-999"`. The `?` operator propagates this error, causing the handler to return the 400 response immediately.

Per the repository conventions, `AppError` implements `IntoResponse` (defined in `common/src/error.rs`), which maps `BadRequest` to HTTP 400 status code.

### Test Coverage

The integration test `test_list_packages_invalid_license_returns_400` validates this criterion:
- Queries `?license=INVALID-999`
- Asserts the response status is `StatusCode::BAD_REQUEST` (400)

This criterion is satisfied by the implementation.
