## Criterion 3: `GET /api/v2/package?license=INVALID-999` returns 400 Bad Request with an error message

### Verdict: PASS

### Reasoning

**Endpoint layer** (`modules/fundamental/src/package/endpoints/list.rs`):
- The `license` parameter `"INVALID-999"` is passed to `validate_license_param`.
- `validate_license_param` splits on comma, yielding `["INVALID-999"]`.
- For the identifier `"INVALID-999"`, `Expression::parse("INVALID-999")` is called. Since "INVALID-999" is not a valid SPDX license expression, this returns an `Err`.
- The error is mapped via `.map_err(|_| AppError::BadRequest(format!("Invalid SPDX license identifier: {}", id)))`, producing an `AppError::BadRequest` with a descriptive error message that includes the invalid identifier.
- The `?` operator propagates this error, causing the handler to return the `AppError::BadRequest` response immediately.

**Error handling** (`common/src/error.rs` per repo structure):
- `AppError` implements `IntoResponse` (noted in repo conventions), so `AppError::BadRequest` is rendered as an HTTP 400 response with the error message in the response body.

**Test coverage** (`tests/api/package.rs`):
- `test_list_packages_invalid_license_returns_400` requests `?license=INVALID-999` and asserts that `resp.status() == StatusCode::BAD_REQUEST`.

The implementation correctly validates license identifiers against SPDX and returns 400 Bad Request with an informative error message for invalid values.
