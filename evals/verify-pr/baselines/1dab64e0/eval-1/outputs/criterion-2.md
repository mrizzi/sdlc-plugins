# Criterion 2: `GET /api/v2/package?license=MIT,Apache-2.0` returns packages with either license

## Verdict: PASS

## Analysis

### Code Changes

The `validate_license_param` function in `modules/fundamental/src/package/endpoints/list.rs` handles comma-separated values:

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

For `license=MIT,Apache-2.0`, the function:
1. Splits by comma producing `["MIT", "Apache-2.0"]`
2. Trims whitespace from each identifier
3. Validates each identifier individually against `spdx::Expression::parse`
4. Returns the full vector `["MIT", "Apache-2.0"]`

In the service layer, the filter uses `Condition::any()` with `is_in`:

```rust
Condition::any()
    .add(package_license::Column::License.is_in(licenses.iter().cloned()))
```

This generates a SQL `WHERE license IN ('MIT', 'Apache-2.0')` clause, which returns the union of packages matching either license. The `Condition::any()` wrapper ensures OR semantics.

### Test Coverage

The test `test_list_packages_multi_license_filter` seeds three packages (pkg-a with MIT, pkg-b with Apache-2.0, pkg-c with GPL-3.0-only), queries with `?license=MIT,Apache-2.0`, and asserts:
- Response status is 200 OK
- Exactly 2 items returned (MIT and Apache-2.0 packages; GPL-3.0-only excluded)
- All items have license equal to either MIT or Apache-2.0

This directly validates the union behavior.

### Conclusion

The comma-separated parsing, per-identifier validation, and `IN` clause filtering together ensure that multiple license values produce the union of matching packages. The test confirms the expected behavior. Criterion is satisfied.
