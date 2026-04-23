# Criterion 3: `GET /api/v2/package?license=INVALID-999` returns 400 Bad Request with an error message

## Result: PASS

## Analysis

### 1. Validation logic

The `validate_license_param` function validates each license identifier:

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

When `INVALID-999` is passed, `spdx::Expression::parse("INVALID-999")` will fail because it is not a valid SPDX expression. The error is mapped to `AppError::BadRequest` with a descriptive message that includes the invalid identifier.

### 2. Error propagation

In the `list_packages` handler, the `?` operator propagates the `AppError::BadRequest` returned by `validate_license_param`:

```rust
let license_filter = match &params.license {
    Some(license) => Some(validate_license_param(license)?),
    None => None,
};
```

Based on the repository conventions (see `common/src/error.rs` description: "AppError enum, implements IntoResponse"), `AppError::BadRequest` will be converted to an HTTP 400 response with the error message.

### 3. Test coverage

The test `test_list_packages_invalid_license_returns_400` sends a request with `?license=INVALID-999` and asserts:

```rust
assert_eq!(resp.status(), StatusCode::BAD_REQUEST);
```

### 4. Error message content

The error message format is `"Invalid SPDX license identifier: INVALID-999"`, which is descriptive and includes the offending value, satisfying the "with an error message" requirement.

## Conclusion

Invalid SPDX identifiers are caught during validation, before any database query is executed. The `AppError::BadRequest` response provides a clear error message. The test confirms the 400 status code.
