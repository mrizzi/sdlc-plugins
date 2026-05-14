## Criterion 3: `GET /api/v2/package?license=INVALID-999` returns 400 Bad Request with an error message

### Verdict: PASS

### Evidence

The PR implements SPDX license validation with appropriate error handling for invalid identifiers:

1. **Validation logic** (`modules/fundamental/src/package/endpoints/list.rs` -- `validate_license_param`):
   Each identifier extracted from the comma-separated list is validated using `spdx::Expression::parse(id)`. When parsing fails (as it would for `INVALID-999`, which is not a valid SPDX identifier), the error is mapped to `AppError::BadRequest`:
   ```rust
   Expression::parse(id).map_err(|_| {
       AppError::BadRequest(format!("Invalid SPDX license identifier: {}", id))
   })?;
   ```
   The `?` operator causes early return with the error, preventing the query from executing.

2. **Error propagation** (`list.rs` -- `list_packages` handler):
   The handler calls `validate_license_param(license)?`, so the `AppError::BadRequest` propagates to the Axum response layer. Per the repository structure (`common/src/error.rs` -- `AppError enum, implements IntoResponse`), `AppError::BadRequest` returns HTTP 400 status with the error message.

3. **Error message content**: The error message includes the invalid identifier: `"Invalid SPDX license identifier: INVALID-999"`, providing useful context to API consumers.

4. **Test coverage** (`tests/api/package.rs` -- `test_list_packages_invalid_license_returns_400`):
   The test requests `?license=INVALID-999` and asserts:
   - Response status is `StatusCode::BAD_REQUEST` (400)

### Conclusion

Invalid SPDX license identifiers are detected by the `spdx::Expression::parse` validation, mapped to `AppError::BadRequest` with a descriptive error message, and returned as HTTP 400. The integration test confirms the 400 status code. This criterion is satisfied.
