## Criterion 3

**Text:** `GET /api/v2/package?license=INVALID-999` returns 400 Bad Request with an error message

### Evidence

1. **SPDX validation** (`modules/fundamental/src/package/endpoints/list.rs`): `validate_license_param` calls `Expression::parse(id)` for each license identifier. `INVALID-999` is not a valid SPDX expression, so `Expression::parse` returns an error.

2. **Error mapping**: The parse error is mapped to `AppError::BadRequest(format!("Invalid SPDX license identifier: {}", id))`. Per the repository conventions, `AppError` implements `IntoResponse` (as documented in `common/src/error.rs`), so `AppError::BadRequest` produces a 400 HTTP response with the error message in the body.

3. **Propagation via `?`**: The `?` operator in the handler (`validate_license_param(license)?`) propagates the `AppError::BadRequest` as the handler's error response.

4. **Test coverage** (`tests/api/package.rs`): `test_list_packages_invalid_license_returns_400` queries `?license=INVALID-999` and asserts `resp.status() == StatusCode::BAD_REQUEST`.

### Verdict: PASS
