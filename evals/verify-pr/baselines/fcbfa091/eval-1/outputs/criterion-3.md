## Criterion 3: `GET /api/v2/package?license=INVALID-999` returns 400 Bad Request with an error message

### Verdict: PASS

### Analysis

This criterion requires that invalid SPDX license identifiers are rejected with a 400 Bad Request response containing an error message.

#### Validation Logic (`modules/fundamental/src/package/endpoints/list.rs`)

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

Key observations:
- Uses `spdx::Expression::parse(id)` to validate each identifier against the SPDX license list
- On parse failure, maps the error to `AppError::BadRequest` with a descriptive message
- The `?` operator propagates the error, causing an early return before any database query
- The error message includes the specific invalid identifier: `"Invalid SPDX license identifier: {id}"`

#### Error Handling Flow

1. Request arrives with `?license=INVALID-999`
2. `validate_license_param("INVALID-999")` is called
3. `Expression::parse("INVALID-999")` fails (not a valid SPDX identifier)
4. `AppError::BadRequest("Invalid SPDX license identifier: INVALID-999")` is returned
5. Per the repository conventions, `AppError` implements `IntoResponse` (documented in `common/src/error.rs`), which renders as HTTP 400

#### Test Coverage

The test `test_list_packages_invalid_license_returns_400` validates this criterion:
- Sends a request with `?license=INVALID-999`
- Asserts the response status is `StatusCode::BAD_REQUEST` (400)

### Evidence

- `spdx::Expression::parse` provides authoritative SPDX validation (using the `spdx` crate)
- `AppError::BadRequest` maps to HTTP 400 per the project's error handling pattern in `common/src/error.rs`
- Error message is descriptive and includes the rejected identifier
- Validation occurs before database access, preventing unnecessary queries
- Integration test confirms the 400 status code response
