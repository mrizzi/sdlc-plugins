# Criterion 3: GET /api/v2/package?license=INVALID-999 returns 400 Bad Request with an error message

## Result: PASS

## Analysis

The implementation satisfies this criterion through the following code path:

**1. SPDX validation (list.rs):**
The `validate_license_param` function validates each license identifier by parsing it as an SPDX expression:
```rust
Expression::parse(id).map_err(|_| {
    AppError::BadRequest(format!("Invalid SPDX license identifier: {}", id))
})?;
```

When an invalid identifier like `"INVALID-999"` is provided, `Expression::parse` will fail because it is not a recognized SPDX license identifier. The error is mapped to `AppError::BadRequest` with a descriptive error message that includes the invalid identifier.

**2. Error propagation (list.rs):**
The `?` operator in `validate_license_param` propagates the `AppError::BadRequest` to the handler. Since the handler returns `Result<Json<PaginatedResults<PackageSummary>>, AppError>`, the error is converted to an HTTP 400 Bad Request response via the `AppError` implementation (documented in the repository as `common/src/error.rs` which implements `IntoResponse`).

**3. Error message content:**
The error message format `"Invalid SPDX license identifier: INVALID-999"` provides a clear explanation of what went wrong, satisfying the "with an error message" part of the criterion.

**4. Test coverage:**
The test `test_list_packages_invalid_license_returns_400` explicitly verifies this behavior: it sends a request with `?license=INVALID-999` and asserts that the response status is `StatusCode::BAD_REQUEST` (400).

The implementation correctly validates license identifiers and returns a 400 Bad Request with a descriptive error message for invalid values.
