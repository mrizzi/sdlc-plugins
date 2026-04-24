# Criterion 2: `GET /api/v2/package?license=MIT,Apache-2.0` returns packages with either license

## Result: PASS

## Evidence

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

For the input `MIT,Apache-2.0`, this produces `["MIT", "Apache-2.0"]`. Each identifier is validated individually against the SPDX expression parser.

In the service layer (`modules/fundamental/src/package/service/mod.rs`), the filter uses `Condition::any()` with `is_in`, which generates an SQL `IN ('MIT', 'Apache-2.0')` clause. The `Condition::any()` wrapper ensures this operates as an OR condition, returning packages matching either license:

```rust
query = query.filter(
    Condition::any()
        .add(package_license::Column::License.is_in(licenses.iter().cloned()))
);
```

The integration test `test_list_packages_multi_license_filter` seeds packages with MIT, Apache-2.0, and GPL-3.0-only licenses, queries with `?license=MIT,Apache-2.0`, and asserts that exactly 2 packages are returned, each having either MIT or Apache-2.0 as their license.

## Reasoning

The implementation correctly handles comma-separated license values by splitting them into a vector, validating each one, and using an `is_in` SQL condition that returns packages matching any of the provided licenses (union semantics). The test confirms the expected behavior for multi-license filtering.
