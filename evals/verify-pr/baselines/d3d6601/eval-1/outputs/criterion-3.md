# Criterion 3: `GET /api/v2/package?license=INVALID-999` returns 400 Bad Request with an error message

## Verdict: PASS

## Reasoning

### What was checked

This criterion requires that invalid SPDX license identifiers are rejected with a 400 Bad Request response containing an error message.

### Evidence from the diff

**1. Validation logic (`list.rs`):**
The `validate_license_param` function iterates over each identifier and calls `Expression::parse(id)`. If parsing fails, it returns an `AppError::BadRequest` with a descriptive message: `format!("Invalid SPDX license identifier: {}", id)`. The `?` operator propagates this error, causing the handler to return the 400 response before any database query is executed.

**2. Error propagation (`list.rs`):**
In `list_packages`, the license filter is validated via `validate_license_param(license)?`. The `?` operator converts the `AppError::BadRequest` into the handler's error return type, which Axum's error handling (via the `AppError` enum's `IntoResponse` implementation in `common/src/error.rs`) translates to an HTTP 400 response.

**3. Error message content:**
The error message includes the specific invalid identifier (e.g., "Invalid SPDX license identifier: INVALID-999"), satisfying the "with an error message" requirement.

**4. Test coverage (`tests/api/package.rs`):**
The test `test_list_packages_invalid_license_returns_400` sends a request with `?license=INVALID-999` and asserts that the response status is `StatusCode::BAD_REQUEST` (400).

### Conclusion

The implementation validates license identifiers against the SPDX standard using the `spdx` crate. Invalid identifiers produce a clear `AppError::BadRequest` with a descriptive message, which is correctly translated to an HTTP 400 response. The test confirms the expected status code.
