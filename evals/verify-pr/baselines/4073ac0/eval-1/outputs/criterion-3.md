# Criterion 3: `GET /api/v2/package?license=INVALID-999` returns 400 Bad Request with an error message

## Verdict: PASS

## Reasoning

The PR implements SPDX validation that rejects invalid license identifiers with a 400 Bad Request response:

**Validation logic (`modules/fundamental/src/package/endpoints/list.rs`):**
- `validate_license_param` iterates over each comma-separated identifier and calls `Expression::parse(id)` from the `spdx` crate.
- If parsing fails (i.e., the identifier is not a valid SPDX expression), the error is mapped to `AppError::BadRequest(format!("Invalid SPDX license identifier: {}", id))` using `.map_err()`.
- The `?` operator propagates this error, causing the handler to return the `AppError::BadRequest` response immediately.

**Error response mechanism:**
- Per the repository conventions documented in `repo-backend.md`, `AppError` is defined in `common/src/error.rs` and implements `IntoResponse`. The `BadRequest` variant returns HTTP 400 with the provided error message.
- The handler's return type is `Result<Json<PaginatedResults<PackageSummary>>, AppError>`, so the `AppError::BadRequest` is correctly returned as the Err variant.

**Test verification (`tests/api/package.rs`):**
- `test_list_packages_invalid_license_returns_400` sends a request with `?license=INVALID-999` and asserts that the response status is `StatusCode::BAD_REQUEST` (400).

The implementation correctly validates license identifiers against the SPDX standard and returns 400 Bad Request with a descriptive error message for invalid values.
