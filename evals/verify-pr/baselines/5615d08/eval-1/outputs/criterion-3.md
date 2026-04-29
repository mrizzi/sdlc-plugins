# Criterion 3: `GET /api/v2/package?license=INVALID-999` returns 400 Bad Request with an error message

## Verdict: PASS

## Reasoning

The PR diff demonstrates that invalid SPDX license identifiers are properly validated and rejected with a 400 Bad Request response.

### Implementation Evidence

1. **SPDX validation** (`modules/fundamental/src/package/endpoints/list.rs`):
   - The `validate_license_param` function validates each license identifier by calling `Expression::parse(id)`.
   - The `spdx` crate's `Expression::parse()` checks whether the string is a recognized SPDX license expression. "INVALID-999" is not a valid SPDX identifier and will cause `parse()` to return an error.
   - The error is mapped to `AppError::BadRequest(format!("Invalid SPDX license identifier: {}", id))`.

2. **Error propagation**:
   - The `?` operator in `validate_license_param` propagates the `AppError::BadRequest` immediately upon the first invalid identifier.
   - In the `list_packages` handler, the call `validate_license_param(license)?` propagates the error, which Axum converts to a 400 Bad Request HTTP response (via `AppError`'s `IntoResponse` implementation documented in `common/src/error.rs`).

3. **Error message**: The format string `"Invalid SPDX license identifier: {}"` ensures the response includes a descriptive error message identifying which identifier was invalid, satisfying the "with an error message" part of the criterion.

### Test Evidence

The test `test_list_packages_invalid_license_returns_400` in `tests/api/package.rs`:
- Requests `GET /api/v2/package?license=INVALID-999`.
- Asserts the response status is `StatusCode::BAD_REQUEST` (400).

This test directly validates that invalid license identifiers trigger a 400 response. While the test does not assert on the error message body, the implementation code clearly includes the error message in the response.
