## Criterion 3: `GET /api/v2/package?license=INVALID-999` returns 400 Bad Request with an error message

### Result: PASS

### Reasoning

**Endpoint layer (`modules/fundamental/src/package/endpoints/list.rs`):**
When the license parameter is present, the handler calls `validate_license_param(license)`. This function iterates over each comma-separated identifier and attempts to parse it via `spdx::Expression::parse(id)`. For the input `INVALID-999`, which is not a valid SPDX license expression, `Expression::parse` returns an error. This error is mapped using `.map_err(|_| AppError::BadRequest(format!("Invalid SPDX license identifier: {}", id)))`.

The `?` operator propagates this `AppError::BadRequest` error, causing the handler to return early with a 400 Bad Request response. The error message includes the specific invalid identifier (`"Invalid SPDX license identifier: INVALID-999"`), satisfying the "with an error message" part of the criterion.

**Error handling pattern:**
The `AppError::BadRequest` variant is part of the repository's shared error enum in `common/src/error.rs`, which implements `IntoResponse` for Axum. This follows the established error handling convention used throughout the codebase.

**Test coverage:**
The integration test `test_list_packages_invalid_license_returns_400` in `tests/api/package.rs` validates this criterion:
- Requests `GET /api/v2/package?license=INVALID-999`
- Asserts the response status is `StatusCode::BAD_REQUEST` (HTTP 400)

This confirms that invalid SPDX license identifiers are rejected with a 400 status code. The validation happens before any database query is executed, which is the correct fail-fast behavior.
