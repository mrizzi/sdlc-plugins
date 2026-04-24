## Criterion 3: `GET /api/v2/package?license=INVALID-999` returns 400 Bad Request with an error message

**Result: PASS**

**Evidence from diff:**

1. **Validation logic** (`modules/fundamental/src/package/endpoints/list.rs`): The `validate_license_param` function calls `Expression::parse(id)` for each license identifier. If parsing fails (i.e., the identifier is not a valid SPDX expression), the error is mapped to `AppError::BadRequest(format!("Invalid SPDX license identifier: {}", id))`. The `?` operator propagates this error, short-circuiting the handler and returning the error response.

2. **Error propagation**: The handler calls `validate_license_param(license)?`, so the `AppError::BadRequest` is returned as the handler's error type. Per the repository conventions noted in `repo-backend.md`, `AppError` implements `IntoResponse`, which means a `BadRequest` variant will produce an HTTP 400 status code with the error message in the response body.

3. **Test coverage** (`tests/api/package.rs`): The test `test_list_packages_invalid_license_returns_400` sends a request with `?license=INVALID-999` and asserts `resp.status() == StatusCode::BAD_REQUEST`.

The invalid license handling is correctly implemented with proper SPDX validation and 400 error responses.
