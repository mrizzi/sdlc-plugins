## Criterion 3: `GET /api/v2/package?license=INVALID-999` returns 400 Bad Request with an error message

**Verdict: PASS**

### Analysis

The implementation satisfies this criterion through the following code path:

1. **SPDX validation:** The `validate_license_param()` function validates each license identifier by calling `spdx::Expression::parse(id)`. The `INVALID-999` string is not a valid SPDX license expression, so `Expression::parse()` returns an error.

2. **Error mapping to 400 Bad Request:** The parse error is mapped to `AppError::BadRequest` with a descriptive message: `format!("Invalid SPDX license identifier: {}", id)`. The `?` operator propagates this error, causing the handler to return early with the 400 response.

3. **Error response:** The `AppError::BadRequest` variant is defined in `common/src/error.rs` and implements `IntoResponse`, which generates an HTTP 400 Bad Request response. The error message is included in the response body, providing the caller with actionable information about which identifier was invalid.

4. **Early validation:** The validation happens in the endpoint handler before the service layer is called, ensuring invalid requests are rejected without database queries.

5. **Test coverage:** The test `test_list_packages_invalid_license_returns_400` sends a request with `?license=INVALID-999` and asserts:
   - Response status is 400 Bad Request (`StatusCode::BAD_REQUEST`)

### Evidence

- `list.rs`: `Expression::parse(id).map_err(|_| AppError::BadRequest(format!("Invalid SPDX license identifier: {}", id)))?` validates and returns 400 on failure
- `list.rs`: Error message includes the invalid identifier: `"Invalid SPDX license identifier: INVALID-999"`
- `tests/api/package.rs`: `test_list_packages_invalid_license_returns_400` verifies 400 status for invalid input
