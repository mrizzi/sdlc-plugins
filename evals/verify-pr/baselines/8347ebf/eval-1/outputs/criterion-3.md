# Criterion 3: `GET /api/v2/package?license=INVALID-999` returns 400 Bad Request with an error message

## Verdict: PASS

## Reasoning

The PR diff demonstrates that invalid SPDX license identifiers are rejected with a 400 Bad Request response.

### Implementation Evidence

1. **Validation logic** (`validate_license_param` in `list.rs`):
   - Each identifier in the comma-separated list is parsed using `spdx::Expression::parse(id)`.
   - If parsing fails (the identifier is not a valid SPDX expression), the error is mapped to `AppError::BadRequest(format!("Invalid SPDX license identifier: {}", id))`.
   - The `?` operator propagates this error, causing the handler to return immediately with the 400 response.

2. **Error handling pattern**:
   - `AppError::BadRequest` is the established error variant in the codebase (defined in `common/src/error.rs`), which implements `IntoResponse` to return a 400 status code with the error message as the response body.
   - The error message includes the specific invalid identifier (e.g., `"Invalid SPDX license identifier: INVALID-999"`), satisfying the "with an error message" part of the criterion.

3. **Early validation**: The validation occurs before the database query is executed. The `validate_license_param` function is called in the handler and its result checked via `?` before `PackageService::list()` is called. This ensures invalid identifiers never reach the database layer.

### Test Evidence

The test `test_list_packages_invalid_license_returns_400` in `tests/api/package.rs`:
- Requests `GET /api/v2/package?license=INVALID-999`
- Asserts response status is `StatusCode::BAD_REQUEST` (400)

This test directly validates the criterion. The implementation uses the `spdx` crate's parser, which will correctly reject `INVALID-999` as it is not a recognized SPDX license identifier.
