# Criterion 3: GET /api/v2/package?license=INVALID-999 returns 400 Bad Request with an error message

## Verdict: PASS

## Analysis

The `validate_license_param` function validates each license identifier against the SPDX expression parser:

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

When an invalid SPDX identifier like `INVALID-999` is provided, `Expression::parse(id)` returns an error. The `map_err` converts this to `AppError::BadRequest` with a descriptive error message: `"Invalid SPDX license identifier: INVALID-999"`. The `?` operator propagates this error, causing the handler to return a 400 Bad Request response.

The import `use spdx::Expression;` confirms the SPDX validation library is used, which provides authoritative SPDX license identifier validation.

The integration test `test_list_packages_invalid_license_returns_400` validates this: it sends a request with `?license=INVALID-999` and asserts that the response status is `StatusCode::BAD_REQUEST`.

## Evidence

- `modules/fundamental/src/package/endpoints/list.rs`: `Expression::parse(id)` validates against SPDX, returns `AppError::BadRequest` with descriptive message on failure
- `tests/api/package.rs`: `test_list_packages_invalid_license_returns_400` confirms 400 status code for invalid identifiers
