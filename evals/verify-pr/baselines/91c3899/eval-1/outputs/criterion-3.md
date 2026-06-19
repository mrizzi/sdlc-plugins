## Criterion 3: `GET /api/v2/package?license=INVALID-999` returns 400 Bad Request with an error message

### Analysis

The `validate_license_param` function validates each license identifier using `spdx::Expression::parse`:

```rust
Expression::parse(id).map_err(|_| {
    AppError::BadRequest(format!("Invalid SPDX license identifier: {}", id))
})?;
```

If any identifier fails parsing, the function returns an `AppError::BadRequest` with a descriptive error message including the invalid identifier. The `?` operator propagates this error to the handler, which returns a 400 response because `AppError` implements `IntoResponse` (as documented in the repo structure: `common/src/error.rs`).

The test `test_list_packages_invalid_license_returns_400` sends a request with `license=INVALID-999` and asserts `resp.status() == StatusCode::BAD_REQUEST`.

### Code Evidence

- `list.rs`: `Expression::parse(id).map_err(|_| AppError::BadRequest(...))` validates each identifier
- `list.rs`: Error message format: `"Invalid SPDX license identifier: {id}"`
- `tests/api/package.rs`: `test_list_packages_invalid_license_returns_400` verifies the 400 response

## Verdict: PASS
