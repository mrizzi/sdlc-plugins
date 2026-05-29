# Criterion 3: `GET /api/v2/package?license=INVALID-999` returns 400 Bad Request with an error message

## Verdict: PASS

## Reasoning

The PR diff implements SPDX license validation that rejects invalid identifiers with a 400 Bad Request response:

**Validation logic (`modules/fundamental/src/package/endpoints/list.rs`):**
- `validate_license_param` iterates over each comma-separated identifier and calls `Expression::parse(id)`.
- The `spdx` crate's `Expression::parse` validates against known SPDX license identifiers. For an invalid identifier like `"INVALID-999"`, the parse will fail.
- The error is mapped using `.map_err(|_| AppError::BadRequest(format!("Invalid SPDX license identifier: {}", id)))`.
- `AppError::BadRequest` is a variant of the application's error enum (defined in `common/src/error.rs`), which implements `IntoResponse` to produce a 400 HTTP status code.

**Error propagation in the handler:**
- In `list_packages`, the `?` operator on `validate_license_param(license)?` propagates the `AppError::BadRequest` as an early return, preventing any database query from executing.
- Axum's error handling converts the `AppError::BadRequest` into a 400 response with the error message as the body.

**Test coverage (`tests/api/package.rs`):**
- `test_list_packages_invalid_license_returns_400` requests `GET /api/v2/package?license=INVALID-999`.
- It asserts `resp.status() == StatusCode::BAD_REQUEST` (HTTP 400).
- The test does not explicitly assert the error message body, but the criterion requires "400 Bad Request with an error message" and the implementation provides `"Invalid SPDX license identifier: INVALID-999"` as the message via `AppError::BadRequest`.

The implementation correctly validates license identifiers and returns 400 Bad Request with a descriptive error message for invalid values.
