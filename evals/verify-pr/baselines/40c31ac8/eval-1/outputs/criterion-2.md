## Criterion 2: `GET /api/v2/package?license=MIT,Apache-2.0` returns packages with either license

**Result: PASS**

### Evidence

**Parsing logic (`modules/fundamental/src/package/endpoints/list.rs`):**

The `validate_license_param` function handles comma-separated values:

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

For the input `"MIT,Apache-2.0"`, this produces `vec!["MIT", "Apache-2.0"]`. Each identifier is individually validated against the SPDX expression parser. The `.trim()` call handles optional whitespace around commas.

**Service layer (`modules/fundamental/src/package/service/mod.rs`):**

The filter uses `Condition::any()` combined with `is_in`:

```rust
query = query.filter(
    Condition::any()
        .add(package_license::Column::License.is_in(licenses.iter().cloned()))
);
```

`is_in` generates a SQL `WHERE license IN ('MIT', 'Apache-2.0')` clause, which inherently returns packages matching ANY of the provided values (union semantics). The `Condition::any()` wrapper is consistent with OR-based filtering.

**Test coverage (`tests/api/package.rs`):**

The test `test_list_packages_multi_license_filter` seeds three packages with distinct licenses (MIT, Apache-2.0, GPL-3.0-only), requests `?license=MIT,Apache-2.0`, and asserts:
- Response status is 200 OK
- Exactly 2 items are returned (MIT + Apache-2.0; GPL-3.0-only is excluded)
- All returned items have a license that is either `MIT` or `Apache-2.0`

### Conclusion

The comma-separated license parameter is correctly split, validated per-identifier, and translated into an `IN` clause that returns the union of matching packages. The test confirms the expected union behavior.
