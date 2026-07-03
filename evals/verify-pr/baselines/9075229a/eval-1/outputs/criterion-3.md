## Criterion 3: `GET /api/v2/package?license=INVALID-999` returns 400 Bad Request with an error message

**Verdict: PASS**

### Analysis

The `validate_license_param` function in `modules/fundamental/src/package/endpoints/list.rs` validates each license identifier against the SPDX expression parser:

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

When `INVALID-999` is passed, `Expression::parse("INVALID-999")` will fail because `INVALID-999` is not a valid SPDX license expression. The `map_err` converts the parse error into an `AppError::BadRequest` with a descriptive message: `"Invalid SPDX license identifier: INVALID-999"`.

The `?` operator propagates this error, causing the handler to return early with the `AppError::BadRequest`. Per the repository's error handling convention (`common/src/error.rs` implements `IntoResponse` for `AppError`), this translates to an HTTP 400 Bad Request response with the error message in the body.

The validation happens in the handler before the service call, so no database query is executed for invalid license identifiers.

### Test Coverage

The test `test_list_packages_invalid_license_returns_400` in `tests/api/package.rs` directly verifies this criterion:
- Sends `GET /api/v2/package?license=INVALID-999`
- Asserts response status is `StatusCode::BAD_REQUEST` (400)

This confirms that invalid SPDX identifiers are rejected with a 400 response.

### Conclusion

The implementation validates license identifiers using the `spdx` crate's `Expression::parse` function and returns `AppError::BadRequest` with a descriptive error message for invalid identifiers. This follows the repository's established error handling pattern. The integration test validates the 400 response behavior. Criterion satisfied.
