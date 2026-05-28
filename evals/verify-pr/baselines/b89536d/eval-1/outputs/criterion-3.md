## Criterion 3: `GET /api/v2/package?license=INVALID-999` returns 400 Bad Request with an error message

### Verdict: PASS

### Reasoning

The `validate_license_param` function in `modules/fundamental/src/package/endpoints/list.rs` validates each license identifier by parsing it as an SPDX expression:

```rust
Expression::parse(id).map_err(|_| {
    AppError::BadRequest(format!("Invalid SPDX license identifier: {}", id))
})?;
```

If `Expression::parse` fails (which it will for an invalid identifier like `INVALID-999`), the function returns an `AppError::BadRequest` with a descriptive error message that includes the invalid identifier. The `?` operator propagates this error up through the handler, which returns `Result<Json<PaginatedResults<PackageSummary>>, AppError>`. The `AppError::BadRequest` variant is converted to an HTTP 400 response by the `IntoResponse` implementation documented in `common/src/error.rs`.

The integration test `test_list_packages_invalid_license_returns_400` in `tests/api/package.rs` verifies this by requesting `?license=INVALID-999` and asserting:

```rust
assert_eq!(resp.status(), StatusCode::BAD_REQUEST);
```

### Evidence

- `modules/fundamental/src/package/endpoints/list.rs`: `Expression::parse(id)` validates SPDX identifiers, returns `AppError::BadRequest` with error message on failure
- `common/src/error.rs`: `AppError` enum implements `IntoResponse` (documented in repo structure)
- `tests/api/package.rs`: `test_list_packages_invalid_license_returns_400` asserts 400 status for `INVALID-999`
