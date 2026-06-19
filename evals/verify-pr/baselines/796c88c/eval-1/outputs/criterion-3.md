## Criterion 3: `GET /api/v2/package?license=INVALID-999` returns 400 Bad Request with an error message

### Verdict: PASS

### Analysis

This criterion requires that invalid SPDX license identifiers are rejected with a 400 Bad Request response containing an error message.

### Evidence

**1. SPDX validation (list.rs):**
The `validate_license_param` function validates each license identifier using the `spdx` crate's `Expression::parse`:
```rust
for id in &identifiers {
    Expression::parse(id).map_err(|_| {
        AppError::BadRequest(format!("Invalid SPDX license identifier: {}", id))
    })?;
}
```
`INVALID-999` is not a valid SPDX expression, so `Expression::parse("INVALID-999")` will return an error. This error is mapped to `AppError::BadRequest` with a descriptive message: `"Invalid SPDX license identifier: INVALID-999"`.

**2. Error propagation (list.rs):**
The handler uses the `?` operator on the validation result:
```rust
let license_filter = match &params.license {
    Some(license) => Some(validate_license_param(license)?),
    None => None,
};
```
If validation fails, the `AppError::BadRequest` is returned immediately, short-circuiting the handler before any database query is executed.

**3. Error response rendering:**
Per the repository conventions (documented in `common/src/error.rs`), `AppError` implements `IntoResponse`. `AppError::BadRequest` renders as HTTP 400 with the error message in the response body.

**4. Test coverage (tests/api/package.rs):**
`test_list_packages_invalid_license_returns_400` queries with `?license=INVALID-999` and asserts:
```rust
assert_eq!(resp.status(), StatusCode::BAD_REQUEST);
```

### Conclusion

The SPDX validation using the `spdx` crate correctly rejects invalid identifiers, maps them to `AppError::BadRequest` with a descriptive error message, and the handler propagates this error before reaching the database. The test confirms the 400 status code. Criterion is satisfied.
