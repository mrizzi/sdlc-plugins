# Criterion 3: GET /api/v2/package?license=INVALID-999 returns 400 Bad Request with an error message

## Verdict: PASS

## Analysis

### Validation Logic (list.rs)

The `validate_license_param` function validates each license identifier against the SPDX standard:

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

When the input is `"INVALID-999"`:
1. It is split into `["INVALID-999"]`
2. `Expression::parse("INVALID-999")` is called -- "INVALID-999" is not a recognized SPDX license identifier, so this returns `Err`
3. The error is mapped to `AppError::BadRequest("Invalid SPDX license identifier: INVALID-999")`
4. The `?` operator propagates this error, causing the handler to return early with the error

### Error Response

The `AppError::BadRequest` variant (defined in `common/src/error.rs` per the repo structure) implements `IntoResponse` for Axum, which converts it to an HTTP 400 Bad Request response. The error message "Invalid SPDX license identifier: INVALID-999" is included in the response body, satisfying the "with an error message" part of the criterion.

### Early Return Behavior

Because validation happens before the database query (the `?` operator on `validate_license_param` causes early return), invalid license identifiers never reach the service layer. This is efficient and follows the "fail fast" principle documented in the implementation notes.

### Test Coverage

`test_list_packages_invalid_license_returns_400` validates this criterion:
- Queries `GET /api/v2/package?license=INVALID-999`
- Asserts response status is `StatusCode::BAD_REQUEST` (400)

The test confirms the 400 status code. Note that the test does not explicitly assert on the error message content, but the implementation clearly includes a descriptive message via the `format!` macro.

## Conclusion

The implementation correctly validates license identifiers against the SPDX standard using the `spdx` crate's `Expression::parse` function. Invalid identifiers cause an `AppError::BadRequest` response with a descriptive error message. The validation happens early in the handler before any database interaction. The test confirms the 400 status code response.
