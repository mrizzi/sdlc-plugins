# Criterion 3: `GET /api/v2/package?license=INVALID-999` returns 400 Bad Request with an error message

## Verdict: PASS

## Reasoning

The `validate_license_param` function in `list.rs` validates each license identifier against the SPDX expression parser:

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

When `INVALID-999` is passed, `Expression::parse("INVALID-999")` will fail because it is not a valid SPDX identifier. The error is mapped to `AppError::BadRequest` with a descriptive error message: `"Invalid SPDX license identifier: INVALID-999"`. The `?` operator propagates this error, causing the handler to return a 400 Bad Request response.

This follows the task's implementation note to "Validate license identifiers against a known SPDX license list before querying; return `AppError::BadRequest` for invalid values" and uses the `spdx::Expression` crate imported at the top of the file.

The integration test `test_list_packages_invalid_license_returns_400` queries with `?license=INVALID-999` and asserts:
- Response status is 400 BAD_REQUEST

The implementation correctly validates SPDX identifiers and returns 400 for invalid values with an error message.
