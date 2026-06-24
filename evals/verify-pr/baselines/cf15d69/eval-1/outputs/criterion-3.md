# Criterion 3: `GET /api/v2/package?license=INVALID-999` returns 400 Bad Request with an error message

## Verdict: PASS

## Reasoning

The PR diff implements invalid license rejection through SPDX validation:

1. **Validation logic** (`modules/fundamental/src/package/endpoints/list.rs`):
   - The `validate_license_param` function iterates over each identifier and calls `Expression::parse(id)`.
   - If parsing fails (the identifier is not a valid SPDX expression), it maps the error to `AppError::BadRequest(format!("Invalid SPDX license identifier: {}", id))`.
   - The `?` operator propagates this error, causing the handler to return early with a 400 response.
   - The error message includes the specific invalid identifier, providing actionable feedback to the API consumer.

2. **Error propagation** (`modules/fundamental/src/package/endpoints/list.rs`):
   - In `list_packages`, the validation is called before the service query: `Some(validate_license_param(license)?)`.
   - The `?` operator on the `Result` ensures the `AppError::BadRequest` is returned as the handler's error response.
   - Per the repo conventions, `AppError` implements `IntoResponse`, so `AppError::BadRequest` maps to HTTP 400.

3. **Test coverage** (`tests/api/package.rs`):
   - `test_list_packages_invalid_license_returns_400` sends a request with `?license=INVALID-999`.
   - Asserts `resp.status() == StatusCode::BAD_REQUEST` (HTTP 400).

The implementation correctly validates against the SPDX standard and returns a descriptive 400 error for invalid identifiers.
