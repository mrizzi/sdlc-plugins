# Criterion 3: `GET /api/v2/package?license=INVALID-999` returns 400 Bad Request with an error message

## Verdict: PASS

## Analysis

The PR implements SPDX validation that rejects invalid license identifiers with a 400 Bad Request response.

### Validation logic (`modules/fundamental/src/package/endpoints/list.rs`)

1. **SPDX parsing:** The `validate_license_param` function attempts to parse each license identifier using `spdx::Expression::parse(id)`. The `spdx` crate validates identifiers against the SPDX license list.

2. **Error mapping:** If parsing fails, the error is mapped to `AppError::BadRequest`:
   ```rust
   Expression::parse(id).map_err(|_| {
       AppError::BadRequest(format!("Invalid SPDX license identifier: {}", id))
   })?;
   ```
   The `?` operator causes early return with the error, so the first invalid identifier in a comma-separated list triggers the 400 response.

3. **Error message:** The error message includes the specific invalid identifier: `"Invalid SPDX license identifier: INVALID-999"`. This satisfies the "with an error message" requirement.

4. **Handler propagation:** The handler function returns `Result<Json<PaginatedResults<PackageSummary>>, AppError>`. The `AppError::BadRequest` variant is returned from `validate_license_param` via the `?` operator in the `match` block:
   ```rust
   let license_filter = match &params.license {
       Some(license) => Some(validate_license_param(license)?),
       None => None,
   };
   ```
   Since `AppError` implements `IntoResponse` (as noted in the repo structure: `common/src/error.rs -- AppError enum, implements IntoResponse`), the 400 status code is returned to the client.

### Test coverage

The `test_list_packages_invalid_license_returns_400` test verifies:
- Queries `?license=INVALID-999`
- Asserts the response status is `StatusCode::BAD_REQUEST` (400)

## Conclusion

The implementation correctly validates license identifiers against the SPDX standard using the `spdx` crate, returns `AppError::BadRequest` with a descriptive error message for invalid identifiers, and the test confirms the 400 status code response.
