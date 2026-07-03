## Criterion 2: `GET /api/v2/package?license=MIT,Apache-2.0` returns packages with either license

**Verdict: PASS**

### Analysis

The `validate_license_param` function in `modules/fundamental/src/package/endpoints/list.rs` splits the comma-separated license string into individual identifiers:

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

For the input `MIT,Apache-2.0`, this produces `["MIT", "Apache-2.0"]`. Each identifier is validated against the SPDX expression parser. The resulting vector is passed to `PackageService::list()`.

In the service layer (`modules/fundamental/src/package/service/mod.rs`), the filter uses `Condition::any()` with `is_in()`:

```rust
query = query.filter(
    Condition::any()
        .add(package_license::Column::License.is_in(licenses.iter().cloned()))
);
```

`Condition::any()` produces a SQL `OR` condition, and `is_in` with multiple values generates a `WHERE license IN ('MIT', 'Apache-2.0')` clause. This returns packages matching either license, which is the union behavior required by the criterion.

### Test Coverage

The test `test_list_packages_multi_license_filter` in `tests/api/package.rs` directly verifies this criterion:
- Seeds three packages: `pkg-a` (MIT), `pkg-b` (Apache-2.0), `pkg-c` (GPL-3.0-only)
- Sends `GET /api/v2/package?license=MIT,Apache-2.0`
- Asserts response status is 200 OK
- Asserts exactly 2 items are returned
- Asserts all returned items have license equal to either `MIT` or `Apache-2.0`

This confirms the union behavior: packages with either license are included, while packages with other licenses (GPL-3.0-only) are excluded.

### Conclusion

The implementation correctly parses comma-separated license values, validates each one, and applies an `IN` filter that returns the union of matching packages. The integration test validates the multi-license filter end-to-end. Criterion satisfied.
