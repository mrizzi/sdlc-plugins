# Criterion 3: `GET /api/v2/package?license=INVALID-999` returns 400 Bad Request with an error message

## Result: PASS

## Analysis

The diff implements SPDX validation with proper error responses:

### Endpoint layer (`modules/fundamental/src/package/endpoints/list.rs`)

- `validate_license_param` iterates over each identifier and calls `Expression::parse(id)`. If parsing fails, it maps the error to `AppError::BadRequest(format!("Invalid SPDX license identifier: {}", id))`.
- The `?` operator propagates this error up from the `list_packages` handler, which returns `Result<Json<PaginatedResults<PackageSummary>>, AppError>`. Since `AppError` implements `IntoResponse` (per the repo structure notes in `common/src/error.rs`), the `BadRequest` variant will produce an HTTP 400 response.
- The error message includes the specific invalid identifier, satisfying the "with an error message" requirement.

### Test coverage

- `test_list_packages_invalid_license_returns_400` sends a request with `?license=INVALID-999` and asserts `resp.status() == StatusCode::BAD_REQUEST`.

The implementation correctly validates SPDX identifiers and returns a 400 Bad Request with a descriptive error message for invalid values.
