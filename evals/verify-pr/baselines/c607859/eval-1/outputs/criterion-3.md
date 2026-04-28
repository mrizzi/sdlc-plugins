# Criterion 3: `GET /api/v2/package?license=INVALID-999` returns 400 Bad Request with an error message

## Verdict: PASS

## Analysis

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

When `Expression::parse(id)` fails (i.e., the identifier is not a valid SPDX expression), the function returns an `AppError::BadRequest` with a descriptive error message including the invalid identifier. The `?` operator propagates this error, causing the handler to return a 400 Bad Request response.

The integration test `test_list_packages_invalid_license_returns_400` requests `?license=INVALID-999` and asserts:

```rust
assert_eq!(resp.status(), StatusCode::BAD_REQUEST);
```

The implementation follows the task's instruction to "Validate license identifiers against a known SPDX license list before querying; return `AppError::BadRequest` for invalid values."

## Conclusion

Invalid SPDX license identifiers correctly return 400 Bad Request with an error message, and the test validates this behavior.
