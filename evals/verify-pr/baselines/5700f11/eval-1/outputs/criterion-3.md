## Criterion 3: `GET /api/v2/package?license=INVALID-999` returns 400 Bad Request with an error message

### Result: PASS

### Reasoning

The PR implements SPDX validation that rejects invalid license identifiers:

**Validation logic** (`modules/fundamental/src/package/endpoints/list.rs`):
- `validate_license_param` iterates over each comma-separated identifier and calls `Expression::parse(id)`.
- When `Expression::parse` fails (i.e., the identifier is not a recognized SPDX expression), `map_err` converts the error to `AppError::BadRequest(format!("Invalid SPDX license identifier: {}", id))`.
- The `?` operator propagates this error, causing the handler to return immediately with the 400 response.

**Error handling chain**:
- `AppError::BadRequest` is defined in `common/src/error.rs` and implements `IntoResponse`, which Axum uses to produce an HTTP 400 status code with the error message in the response body.
- The validation runs before any database query, ensuring invalid inputs are rejected early.

**Test coverage** (`tests/api/package.rs`):
- `test_list_packages_invalid_license_returns_400` sends a request with `?license=INVALID-999` and asserts `resp.status() == StatusCode::BAD_REQUEST`.

The implementation correctly validates license identifiers and returns 400 for invalid values with a descriptive error message.
