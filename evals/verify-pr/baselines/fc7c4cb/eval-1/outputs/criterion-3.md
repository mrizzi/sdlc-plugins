## Criterion 3

**Text**: `GET /api/v2/package?license=INVALID-999` returns 400 Bad Request with an error message

### What was checked

Examined the validation logic for invalid SPDX identifiers and the error response path, plus the corresponding test.

### Code evidence

1. **Validation** (`modules/fundamental/src/package/endpoints/list.rs`): The `validate_license_param` function calls `Expression::parse(id)` for each identifier. For `INVALID-999`, the `spdx` crate's parser will return an error since this is not a recognized SPDX expression.

2. **Error mapping**: The parse error is mapped to `AppError::BadRequest` with a descriptive message:
   ```rust
   Expression::parse(id).map_err(|_| {
       AppError::BadRequest(format!("Invalid SPDX license identifier: {}", id))
   })?;
   ```
   The `?` operator short-circuits the handler, returning the `AppError::BadRequest` which (per the repository's `common/src/error.rs` `IntoResponse` implementation) produces a 400 status code with the error message in the response body.

3. **Handler propagation** (`modules/fundamental/src/package/endpoints/list.rs`): In `list_packages`, the validation is called as:
   ```rust
   Some(license) => Some(validate_license_param(license)?),
   ```
   The `?` propagates the `AppError::BadRequest` directly out of the handler's `Result` return type.

4. **Test coverage** (`tests/api/package.rs`): `test_list_packages_invalid_license_returns_400` queries `?license=INVALID-999` and asserts:
   ```rust
   assert_eq!(resp.status(), StatusCode::BAD_REQUEST);
   ```

### Verdict: PASS

Invalid SPDX identifiers are caught by the `spdx::Expression::parse` call, mapped to `AppError::BadRequest` with a human-readable error message, and short-circuited before any database query. The test confirms a 400 response code.
