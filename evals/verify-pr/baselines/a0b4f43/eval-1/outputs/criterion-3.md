## Criterion 3: `GET /api/v2/package?license=INVALID-999` returns 400 Bad Request with an error message

**Verdict: PASS**

### Reasoning

The invalid license handling is implemented through SPDX validation:

**Validation (`modules/fundamental/src/package/endpoints/list.rs`):**
- The `validate_license_param` function validates each license identifier by calling `Expression::parse(id)`. The `spdx` crate's parser will reject identifiers that are not valid SPDX expressions.
- When parsing fails, the error is mapped to `AppError::BadRequest(format!("Invalid SPDX license identifier: {}", id))`. This produces a 400 Bad Request HTTP response with a descriptive error message containing the invalid identifier.
- The `?` operator propagates the error immediately from the handler, short-circuiting the request before any database query is executed.

**Error propagation:**
- The `validate_license_param` function returns `Result<Vec<String>, AppError>`, and the handler calls it with `validate_license_param(license)?`. If validation fails, the `?` operator returns the `AppError::BadRequest` early, which Axum's `IntoResponse` implementation (from `common/src/error.rs`) converts to a 400 status code response.

**Test verification (`tests/api/package.rs`):**
- The `test_list_packages_invalid_license_returns_400` test sends a request with `?license=INVALID-999` and asserts `resp.status() == StatusCode::BAD_REQUEST`.

The implementation correctly validates license identifiers before querying and returns a 400 Bad Request with an informative error message for invalid values.
