# Criterion 3: `GET /api/v2/package?license=INVALID-999` returns 400 Bad Request with an error message

## Verdict: PASS

## Reasoning

The implementation validates license identifiers against the SPDX standard and returns a 400 Bad Request for invalid values:

### Validation Logic (`modules/fundamental/src/package/endpoints/list.rs`)

1. **SPDX parsing**: The `validate_license_param` function calls `Expression::parse(id)` for each license identifier. The `spdx` crate's `Expression::parse` validates against known SPDX license identifiers.

2. **Error mapping**: When `Expression::parse` fails (returns `Err`), the error is mapped to `AppError::BadRequest(format!("Invalid SPDX license identifier: {}", id))`. This produces:
   - HTTP 400 status code (via `AppError::BadRequest` which implements `IntoResponse` in the common error module)
   - A descriptive error message including the invalid identifier

3. **Early return**: The `?` operator after `map_err` propagates the error immediately, short-circuiting processing of remaining identifiers. For `"INVALID-999"`, the first (and only) identifier fails validation.

### Error Response Flow

4. **Handler integration**: In `list_packages`, the `validate_license_param(license)?` call uses the `?` operator, which returns the `AppError::BadRequest` as the `Err` variant of the handler's `Result`. Axum's error handling converts this into a 400 response.

5. **Error message content**: The error message `"Invalid SPDX license identifier: INVALID-999"` satisfies the "with an error message" requirement in the criterion.

### Test Coverage

The test `test_list_packages_invalid_license_returns_400` directly validates this criterion:
- Queries `?license=INVALID-999`
- Asserts `resp.status() == StatusCode::BAD_REQUEST` (HTTP 400)

## Evidence

- `Expression::parse("INVALID-999")` returns `Err` (not a valid SPDX identifier)
- `AppError::BadRequest(format!("Invalid SPDX license identifier: {}", id))` produces HTTP 400 with message
- Test asserts `resp.status() == StatusCode::BAD_REQUEST`
