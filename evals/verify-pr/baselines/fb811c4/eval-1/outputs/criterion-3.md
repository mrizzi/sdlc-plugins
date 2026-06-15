# Criterion 3: `GET /api/v2/package?license=INVALID-999` returns 400 Bad Request with an error message

## Verdict: PASS

## Analysis

The `validate_license_param` function validates each license identifier by calling `Expression::parse(id)`. When parsing fails (i.e., the identifier is not a valid SPDX expression), the error is mapped to an `AppError::BadRequest` with a descriptive message:

```rust
Expression::parse(id).map_err(|_| {
    AppError::BadRequest(format!("Invalid SPDX license identifier: {}", id))
})?;
```

The `?` operator propagates this error to the handler, which returns a 400 Bad Request response. The error message includes the specific invalid identifier, providing clear feedback to the API consumer.

## Evidence

- `list.rs`: `Expression::parse(id).map_err(|_| AppError::BadRequest(format!("Invalid SPDX license identifier: {}", id)))?;`
- `list.rs`: The `?` propagates the error from `validate_license_param` to the handler's `Result<Json<...>, AppError>` return type
- `tests/api/package.rs`: `test_list_packages_invalid_license_returns_400` sends `?license=INVALID-999` and asserts `resp.status() == StatusCode::BAD_REQUEST`
