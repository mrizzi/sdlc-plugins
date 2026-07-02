## Criterion 3: `GET /api/v2/package?license=INVALID-999` returns 400 Bad Request with an error message

**Result: PASS**

### Evidence

**Validation logic (`modules/fundamental/src/package/endpoints/list.rs`):**

The `validate_license_param` function validates each license identifier using the `spdx` crate's `Expression::parse`:

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

When `INVALID-999` is passed, `Expression::parse("INVALID-999")` returns an `Err` because it is not a recognized SPDX identifier. The `map_err` converts this into `AppError::BadRequest` with a descriptive message: `"Invalid SPDX license identifier: INVALID-999"`.

The `?` operator in the handler causes early return with this error, which Axum's `IntoResponse` implementation for `AppError` translates into an HTTP 400 Bad Request response.

**Handler integration:**

```rust
let license_filter = match &params.license {
    Some(license) => Some(validate_license_param(license)?),
    None => None,
};
```

The `?` propagates the `AppError::BadRequest` before any database query is executed, ensuring invalid input is rejected at the API boundary.

**Test coverage (`tests/api/package.rs`):**

The test `test_list_packages_invalid_license_returns_400` sends `?license=INVALID-999` and asserts:

```rust
assert_eq!(resp.status(), StatusCode::BAD_REQUEST);
```

This confirms the 400 status code is returned for invalid license identifiers.

### Conclusion

Invalid SPDX license identifiers are detected during validation using the `spdx` crate, and the handler returns a 400 Bad Request response with a descriptive error message before reaching the database layer. The test confirms this behavior.
