## Criterion 1: `GET /api/v2/package?license=MIT` returns only packages with MIT license

### Verdict: PASS

### Analysis

This criterion requires that the endpoint accepts a `license` query parameter and filters results to return only packages matching the specified license.

### Evidence

**1. Query parameter parsing (list.rs):**
The `PackageListParams` struct now includes an optional `license` field:
```rust
pub struct PackageListParams {
    pub offset: Option<i64>,
    pub limit: Option<i64>,
    pub license: Option<String>,
}
```
This means `?license=MIT` in the query string will be deserialized into `params.license = Some("MIT")`.

**2. License validation (list.rs):**
The `validate_license_param` function parses the license string, splitting on commas, and validates each identifier against the SPDX expression parser:
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
For `?license=MIT`, this produces `vec!["MIT"]` after validation.

**3. Filter application (service/mod.rs):**
The `PackageService::list` method now accepts a `license_filter` parameter and applies it to the query:
```rust
if let Some(licenses) = license_filter {
    query = query.filter(
        Condition::any()
            .add(package_license::Column::License.is_in(licenses.iter().cloned()))
    );
    query = query.join(JoinType::InnerJoin, package::Relation::PackageLicense.def());
}
```
When `license_filter = Some(&["MIT"])`, the query adds a WHERE clause filtering `package_license.license IN ('MIT')` via an inner join to the `package_license` table. This ensures only packages with MIT license are returned.

**4. Handler wiring (list.rs):**
The `list_packages` handler connects the parameter to the service:
```rust
let license_filter = match &params.license {
    Some(license) => Some(validate_license_param(license)?),
    None => None,
};
let results = PackageService::new(&db)
    .list(params.offset, params.limit, license_filter.as_deref())
    .await
```

**5. Test coverage (tests/api/package.rs):**
`test_list_packages_single_license_filter` seeds packages with MIT and Apache-2.0 licenses, queries with `?license=MIT`, and asserts:
- Response status is 200 OK
- Result contains exactly 2 items (the two MIT packages)
- All returned items have `license == "MIT"`

### Conclusion

The full chain -- query parameter parsing, SPDX validation, filter application via SeaORM condition with inner join, and handler wiring -- correctly implements single-license filtering. The test confirms the expected behavior. Criterion is satisfied.
