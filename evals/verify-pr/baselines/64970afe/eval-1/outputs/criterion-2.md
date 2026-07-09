## Criterion 2: `GET /api/v2/package?license=MIT,Apache-2.0` returns packages with either license

### Verdict: PASS

### Evidence

**Endpoint layer (`modules/fundamental/src/package/endpoints/list.rs`):**

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

For input `"MIT,Apache-2.0"`, this splits on `,`, trims whitespace, and produces `["MIT", "Apache-2.0"]`. Each identifier is individually validated against the SPDX expression parser.

**Service layer (`modules/fundamental/src/package/service/mod.rs`):**

The `is_in` clause accepts the full vector of identifiers:

```rust
Condition::any()
    .add(package_license::Column::License.is_in(licenses.iter().cloned()))
```

This generates `WHERE package_license.license IN ('MIT', 'Apache-2.0')`, which returns the union of packages matching either license. The use of `Condition::any()` ensures OR semantics.

**Test coverage (`tests/api/package.rs`):**

`test_list_packages_multi_license_filter` seeds three packages (MIT, Apache-2.0, GPL-3.0-only), queries `?license=MIT,Apache-2.0`, and asserts:
- Response status is 200 OK
- Exactly 2 items returned (MIT and Apache-2.0, excluding GPL-3.0-only)
- All returned items have a license that is either "MIT" or "Apache-2.0"

This directly verifies the union behavior specified in the criterion.
