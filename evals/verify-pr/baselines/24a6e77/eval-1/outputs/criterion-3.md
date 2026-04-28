# Criterion 3: GET /api/v2/package?license=INVALID-999 returns 400 Bad Request with an error message

## Verdict: PASS

## Reasoning

### Code Analysis

The `validate_license_param` function validates each license identifier against the SPDX specification using `spdx::Expression::parse()`:

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

When `?license=INVALID-999` is provided:
1. The string is split to `["INVALID-999"]`.
2. `Expression::parse("INVALID-999")` fails because "INVALID-999" is not a valid SPDX expression.
3. The error is mapped to `AppError::BadRequest(...)` with a descriptive message: `"Invalid SPDX license identifier: INVALID-999"`.
4. The `?` operator propagates the error, causing the handler to return early with the 400 response.

The `AppError::BadRequest` variant (defined in `common/src/error.rs` per the repo structure) implements `IntoResponse` for Axum, returning an HTTP 400 status code with the error message.

### Test Verification

The test `test_list_packages_invalid_license_returns_400` in `tests/api/package.rs`:
- Requests `?license=INVALID-999`.
- Asserts the response status is `StatusCode::BAD_REQUEST` (400).

This directly validates the criterion. The error message content is not explicitly asserted in the test, but the `AppError::BadRequest` format string includes the invalid identifier, satisfying the "with an error message" requirement.

### Conclusion

The implementation correctly rejects invalid SPDX identifiers by returning a 400 Bad Request response with a descriptive error message. The validation happens before any database query, which is the correct approach. Criterion is satisfied.
