# Criterion 3: `GET /api/v2/package?license=INVALID-999` returns 400 Bad Request with an error message

## Verdict: PASS

## Reasoning

The PR diff implements SPDX license validation with proper error handling:

1. **Validation logic** (`list.rs`): The `validate_license_param()` function iterates over each comma-separated identifier and calls `spdx::Expression::parse(id)`. If parsing fails (indicating an invalid SPDX identifier), it maps the error to `AppError::BadRequest` with a descriptive message:
   ```rust
   Expression::parse(id).map_err(|_| {
       AppError::BadRequest(format!("Invalid SPDX license identifier: {}", id))
   })?;
   ```
   The `?` operator causes early return with the error, preventing the query from executing.

2. **Error propagation** (`list.rs`): In `list_packages()`, the validation result is checked before calling the service:
   ```rust
   let license_filter = match &params.license {
       Some(license) => Some(validate_license_param(license)?),
       None => None,
   };
   ```
   The `?` propagates the `AppError::BadRequest` directly to the Axum response handler, which converts it to a 400 status code response (as documented in `common/src/error.rs` -- `AppError` implements `IntoResponse`).

3. **Test coverage** (`tests/api/package.rs`): The `test_list_packages_invalid_license_returns_400` test requests `?license=INVALID-999` and asserts:
   - Response status is `StatusCode::BAD_REQUEST` (400)

   The identifier `INVALID-999` is not a valid SPDX expression, so `spdx::Expression::parse` will fail, triggering the error path. The error message includes the invalid identifier for debuggability.

The validation correctly uses the `spdx` crate for standards-compliant license identifier checking, and invalid identifiers produce a 400 response with a meaningful error message.
