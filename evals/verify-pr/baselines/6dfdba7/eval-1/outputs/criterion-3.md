# Criterion 3: `GET /api/v2/package?license=INVALID-999` returns 400 Bad Request with an error message

## Result: PASS

## Evidence

The `validate_license_param` function in `modules/fundamental/src/package/endpoints/list.rs` validates each license identifier against the SPDX expression parser:

```rust
fn validate_license_param(license: &str) -> Result<Vec<String>, AppError> {
    let identifiers: Vec<String> = license.split(',').map(|s| s.trim().to_string()).collect();
    for id in &identifiers {
        Expression::parse(id).map_err(|_| {
            AppError::BadRequest(format!("Invalid SPDX license identifier: {}", id))
        })?;
    }
    Ok(identifiers)
}
```

When `INVALID-999` is provided, `Expression::parse("INVALID-999")` will fail because it is not a recognized SPDX license identifier. The error is mapped to `AppError::BadRequest` with the message `"Invalid SPDX license identifier: INVALID-999"`. Since `validate_license_param` is called with the `?` operator in the handler, this error propagates as the HTTP response.

The `AppError` enum (described in `common/src/error.rs` per the repository structure) implements `IntoResponse`, meaning `AppError::BadRequest` will produce a 400 status code HTTP response.

The integration test `test_list_packages_invalid_license_returns_400` confirms this behavior:

```rust
async fn test_list_packages_invalid_license_returns_400(ctx: &TestContext) {
    let resp = ctx.get("/api/v2/package?license=INVALID-999").await;
    assert_eq!(resp.status(), StatusCode::BAD_REQUEST);
}
```

## Reasoning

The implementation validates license identifiers before querying the database, using the `spdx::Expression::parse` function. Invalid identifiers cause an early return with `AppError::BadRequest`, which produces a 400 HTTP response with an error message. The validation happens per-identifier, so even in a comma-separated list, a single invalid identifier will reject the entire request. The test confirms the 400 response for an invalid identifier.
