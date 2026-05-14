## Criterion 3: `GET /api/v2/package?license=INVALID-999` returns 400 Bad Request with an error message

### Verdict: PASS

### Evidence

**Endpoint layer (`list.rs`):**
- `validate_license_param` iterates over each identifier and calls `Expression::parse(id)`. If parsing fails, it returns `AppError::BadRequest(format!("Invalid SPDX license identifier: {}", id))`.
- The `?` operator in `validate_license_param(license)?` propagates this error up to the handler, which returns `Result<..., AppError>`. Per the repository conventions, `AppError` implements `IntoResponse`, so `AppError::BadRequest` maps to HTTP 400.
- The error message includes the specific invalid identifier, providing actionable feedback to the caller.

**Test evidence (`tests/api/package.rs`):**
- `test_list_packages_invalid_license_returns_400` sends a request with `?license=INVALID-999` and asserts:
  - Response status is `StatusCode::BAD_REQUEST` (400)

The validation logic correctly rejects unknown SPDX identifiers with a 400 response and descriptive error message, and the test confirms this behavior.
