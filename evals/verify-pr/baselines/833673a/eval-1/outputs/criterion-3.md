## Criterion 3: `GET /api/v2/package?license=INVALID-999` returns 400 Bad Request with an error message

### Verdict: PASS

### Reasoning

The PR implements SPDX license identifier validation with proper error handling:

**Validation function (`modules/fundamental/src/package/endpoints/list.rs`):**
- The `validate_license_param` function iterates over each comma-separated license identifier and attempts to parse it using `spdx::Expression::parse(id)`.
- If any identifier fails to parse, the function maps the error to `AppError::BadRequest(format!("Invalid SPDX license identifier: {}", id))` and returns early via the `?` operator.
- `INVALID-999` is not a valid SPDX license expression, so `Expression::parse("INVALID-999")` will return an error, which is converted to the `AppError::BadRequest` variant.

**Handler integration:**
- The handler calls `validate_license_param(license)?` with the `?` operator, so the `AppError::BadRequest` propagates up and becomes the HTTP response. Based on the repository's error handling convention (`common/src/error.rs` defines `AppError` which implements `IntoResponse`), `AppError::BadRequest` maps to HTTP 400 status code.

**Error message quality:**
- The error message includes the specific invalid identifier: `"Invalid SPDX license identifier: INVALID-999"`, which provides clear feedback to the API consumer about which identifier was invalid.

**Test coverage (`tests/api/package.rs`):**
- `test_list_packages_invalid_license_returns_400` sends a request with `?license=INVALID-999` and asserts `resp.status() == StatusCode::BAD_REQUEST`. This directly verifies the 400 response.

The implementation correctly validates license identifiers against the SPDX standard, returns 400 Bad Request for invalid values, and includes a descriptive error message identifying the invalid identifier.
