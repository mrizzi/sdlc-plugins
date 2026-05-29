# Criterion 3: `GET /api/v2/package?license=INVALID-999` returns 400 Bad Request with an error message

## Verdict: PASS

## Analysis

The PR diff demonstrates that invalid SPDX license identifiers are correctly rejected with a 400 Bad Request response.

### Implementation Evidence

**Endpoint layer** (`modules/fundamental/src/package/endpoints/list.rs`):
- The `validate_license_param()` function iterates over each comma-separated identifier and attempts to parse it with `spdx::Expression::parse(id)`.
- If parsing fails, the function returns an `AppError::BadRequest` with a descriptive error message: `format!("Invalid SPDX license identifier: {}", id)`.
- The `?` operator in `validate_license_param` propagates the error immediately upon encountering the first invalid identifier.
- In `list_packages()`, the `validate_license_param(license)?` call uses `?` to short-circuit and return the error to the HTTP layer before any database query executes.

**Error handling**: The `AppError::BadRequest` variant (defined in `common/src/error.rs` per the repository structure) implements `IntoResponse` for Axum, which converts it to a 400 HTTP status code with the error message in the response body.

### Test Evidence

The test `test_list_packages_invalid_license_returns_400` in `tests/api/package.rs`:
- Requests `GET /api/v2/package?license=INVALID-999`
- Asserts the response status is `StatusCode::BAD_REQUEST` (HTTP 400)

This directly validates the criterion. The test confirms that an invalid SPDX identifier like `INVALID-999` (which is not a recognized SPDX expression) triggers the validation error path.

### Conclusion

The `spdx::Expression::parse()` validation, the `AppError::BadRequest` error mapping with a descriptive message, and the integration test all confirm that invalid license identifiers produce a 400 Bad Request response with an error message.
