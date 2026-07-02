## Criterion 1: `GET /api/v2/package?license=MIT` returns only packages with MIT license

### Verdict: PASS

### Analysis

This criterion requires that the endpoint accepts a `license` query parameter and returns only packages matching the specified license.

#### Endpoint Layer (`modules/fundamental/src/package/endpoints/list.rs`)

The `PackageListParams` struct now includes a `license` field:

```rust
pub struct PackageListParams {
    pub offset: Option<i64>,
    pub limit: Option<i64>,
    pub license: Option<String>,
}
```

When the `license` parameter is present, the handler calls `validate_license_param(license)` to parse and validate it, then passes the resulting `Vec<String>` to the service layer:

```rust
let license_filter = match &params.license {
    Some(license) => Some(validate_license_param(license)?),
    None => None,
};

let results = PackageService::new(&db)
    .list(params.offset, params.limit, license_filter.as_deref())
    .await
    .context("Failed to list packages")?;
```

#### Service Layer (`modules/fundamental/src/package/service/mod.rs`)

The `list` method now accepts an optional `license_filter: Option<&[String]>` parameter. When provided, it applies an `is_in` filter joined to the `package_license` table:

```rust
if let Some(licenses) = license_filter {
    query = query.filter(
        Condition::any()
            .add(package_license::Column::License.is_in(licenses.iter().cloned()))
    );
    query = query.join(JoinType::InnerJoin, package::Relation::PackageLicense.def());
}
```

The `is_in` filter ensures only packages whose license column matches one of the provided identifiers are returned. For a single value like `MIT`, this effectively filters to MIT-only packages.

#### Test Coverage

The test `test_list_packages_single_license_filter` directly validates this criterion:
- Seeds packages with MIT and Apache-2.0 licenses
- Queries `?license=MIT`
- Asserts exactly 2 results returned (the two MIT packages)
- Asserts all returned packages have `license == "MIT"`

### Evidence

- `PackageListParams.license` field added as `Option<String>` -- correctly optional
- `validate_license_param` splits by comma and validates each identifier via `spdx::Expression::parse`
- Service layer applies `is_in` filter with `InnerJoin` to `PackageLicense` entity
- Integration test confirms filtering behavior with concrete seed data
