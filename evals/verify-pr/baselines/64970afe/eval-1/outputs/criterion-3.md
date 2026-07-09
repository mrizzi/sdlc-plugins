## Criterion 3: `GET /api/v2/package?license=INVALID-999` returns 400 Bad Request with an error message

### Verdict: PASS

### Evidence

**Endpoint layer (`modules/fundamental/src/package/endpoints/list.rs`):**

The `validate_license_param` function validates each identifier by parsing it as an SPDX expression:

```rust
Expression::parse(id).map_err(|_| {
    AppError::BadRequest(format!("Invalid SPDX license identifier: {}", id))
})?;
```

`"INVALID-999"` is not a recognized SPDX license identifier, so `Expression::parse` will return an error. This is mapped to `AppError::BadRequest` with a descriptive message: `"Invalid SPDX license identifier: INVALID-999"`.

The `?` operator propagates this error, causing the handler to return early with a 400 status before any database query is executed. Per the repository conventions in `common/src/error.rs`, `AppError` implements `IntoResponse`, so `AppError::BadRequest` is rendered as an HTTP 400 response with the error message in the body.

**Request flow:**

1. Axum deserializes query params into `PackageListParams` with `license = Some("INVALID-999")`
2. `validate_license_param("INVALID-999")` is called
3. `Expression::parse("INVALID-999")` fails
4. `AppError::BadRequest("Invalid SPDX license identifier: INVALID-999")` is returned
5. Axum converts this to a 400 response via the `IntoResponse` implementation

**Test coverage (`tests/api/package.rs`):**

`test_list_packages_invalid_license_returns_400` sends `GET /api/v2/package?license=INVALID-999` and asserts:
- Response status is `StatusCode::BAD_REQUEST` (400)

This directly verifies the criterion. The error message content is produced by the `format!` macro in the `map_err` closure.
