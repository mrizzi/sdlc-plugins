# Criterion 3: `GET /api/v2/package?license=INVALID-999` returns 400 Bad Request with an error message

## Verdict: PASS

## Analysis

### What was checked

This criterion requires that invalid SPDX license identifiers are rejected with a 400 Bad Request response containing an error message.

### Evidence from the diff

1. **Validation logic** (`modules/fundamental/src/package/endpoints/list.rs`):
   - `validate_license_param` iterates over each identifier and calls `Expression::parse(id)`.
   - On parse failure, it maps the error to `AppError::BadRequest(format!("Invalid SPDX license identifier: {}", id))`.
   - The `?` operator causes the function to return early on the first invalid identifier, propagating the error to the handler.

2. **Error propagation in handler** (`modules/fundamental/src/package/endpoints/list.rs`):
   - In `list_packages`, the call `validate_license_param(license)?` propagates any `AppError::BadRequest` to the Axum response pipeline.
   - Per the repository's `common/src/error.rs`, `AppError` implements `IntoResponse`, so `AppError::BadRequest` maps to HTTP 400 status.

3. **Error message content**:
   - The error message includes the specific invalid identifier: `"Invalid SPDX license identifier: INVALID-999"`. This provides actionable feedback to the API consumer.

4. **Test coverage** (`tests/api/package.rs`):
   - `test_list_packages_invalid_license_returns_400` sends `?license=INVALID-999` and asserts `resp.status() == StatusCode::BAD_REQUEST`.

### Conclusion

The implementation validates each license identifier against the SPDX specification using the `spdx` crate's `Expression::parse`. Invalid identifiers produce a 400 Bad Request response with a descriptive error message. The test confirms the 400 status code.
