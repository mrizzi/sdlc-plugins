## Criterion 3: `GET /api/v2/package?license=INVALID-999` returns 400 Bad Request with an error message

### Verdict: PASS

### Analysis

**Endpoint layer (`modules/fundamental/src/package/endpoints/list.rs`):**

The `validate_license_param` function validates each license identifier by attempting to parse it as an SPDX expression:
```rust
for id in &identifiers {
    Expression::parse(id).map_err(|_| {
        AppError::BadRequest(format!("Invalid SPDX license identifier: {}", id))
    })?;
}
```

`INVALID-999` is not a valid SPDX license identifier. `Expression::parse("INVALID-999")` will return an `Err`, which is mapped to `AppError::BadRequest` with a descriptive error message: `"Invalid SPDX license identifier: INVALID-999"`.

The `?` operator propagates this error out of `validate_license_param`, and since it is called within the handler function which returns `Result<..., AppError>`, the `AppError::BadRequest` is returned as the response. Per the repository conventions (`common/src/error.rs` implements `IntoResponse` for `AppError`), a `BadRequest` variant maps to HTTP 400 status.

**Error message content:**

The error message format `"Invalid SPDX license identifier: {id}"` provides clear context about which identifier failed validation, satisfying the "with an error message" part of the criterion.

**Test coverage (`tests/api/package.rs`):**

The test `test_list_packages_invalid_license_returns_400` sends a request with `?license=INVALID-999` and asserts:
```rust
assert_eq!(resp.status(), StatusCode::BAD_REQUEST);
```

This directly validates the 400 response for invalid identifiers.

### Conclusion

The SPDX expression parser correctly rejects invalid identifiers, the error is mapped to `AppError::BadRequest` with a descriptive message, and the integration test confirms the 400 status code. This criterion is satisfied.
