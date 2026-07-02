## Criterion 3: Invalid License Returns 400

**Requirement**: `GET /api/v2/package?license=INVALID-999` returns 400 Bad Request with an error message.

**Verdict**: PASS

### Analysis

**Validation Logic**: The `validate_license_param` function validates each license identifier against the SPDX expression parser:

```rust
for id in &identifiers {
    Expression::parse(id).map_err(|_| {
        AppError::BadRequest(format!("Invalid SPDX license identifier: {}", id))
    })?;
}
```

When `Expression::parse("INVALID-999")` fails (since "INVALID-999" is not a valid SPDX identifier), the error is mapped to `AppError::BadRequest` with a descriptive error message that includes the invalid identifier. The `?` operator short-circuits the handler, returning the error response immediately.

**Error Message**: The error message format is `"Invalid SPDX license identifier: INVALID-999"`, which provides clear feedback to the API consumer about what went wrong.

**Error Handling Integration**: Per the repository conventions, `AppError` implements `IntoResponse` (defined in `common/src/error.rs`), so `AppError::BadRequest` will produce a proper HTTP 400 response.

**Handler Integration**: In `list_packages`, the validation is called before any database query:

```rust
let license_filter = match &params.license {
    Some(license) => Some(validate_license_param(license)?),
    None => None,
};
```

The `?` propagates the `AppError::BadRequest`, so the handler returns 400 without hitting the database.

**Test Coverage**: `test_list_packages_invalid_license_returns_400` sends `?license=INVALID-999` and asserts:
- Response status is 400 BAD_REQUEST
