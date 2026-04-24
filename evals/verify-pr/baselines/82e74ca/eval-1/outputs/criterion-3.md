# Criterion 3: `GET /api/v2/package?license=INVALID-999` returns 400 Bad Request with an error message

## Result: PASS

## Analysis

### Code Evidence

**Validation logic** (`modules/fundamental/src/package/endpoints/list.rs`):

The `validate_license_param` function validates each license identifier by attempting to parse it as an SPDX expression using the `spdx` crate:

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

For an invalid identifier like `INVALID-999`, `Expression::parse("INVALID-999")` will fail (as it is not a recognized SPDX license expression). The error is mapped to `AppError::BadRequest` with a descriptive message: `"Invalid SPDX license identifier: INVALID-999"`.

**Error propagation**: The `?` operator in `validate_license_param(license)?` within the handler causes the `AppError::BadRequest` to be returned immediately, which (per the repository conventions noted in `common/src/error.rs`) renders as an HTTP 400 Bad Request response.

### Test Evidence

The test `test_list_packages_invalid_license_returns_400` in `tests/api/package.rs` sends a request with `?license=INVALID-999` and asserts:
- Status is 400 BAD_REQUEST

### Conclusion

The implementation validates license identifiers against the SPDX standard using `spdx::Expression::parse`. Invalid identifiers cause an immediate 400 Bad Request response with a descriptive error message. This criterion is satisfied.
