# Criterion 1: `GET /api/v2/package?license=MIT` returns only packages with MIT license

## Result: PASS

## Evidence

The PR diff adds a `license` query parameter to `PackageListParams` in `modules/fundamental/src/package/endpoints/list.rs`:

```rust
pub struct PackageListParams {
    pub offset: Option<i64>,
    pub limit: Option<i64>,
    pub license: Option<String>,
}
```

When the `license` parameter is present, the `list_packages` handler calls `validate_license_param` to parse and validate the value, then passes the resulting filter to `PackageService::list`:

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

In `modules/fundamental/src/package/service/mod.rs`, the `list` method applies the filter using a `Condition::any()` with `is_in` on the `package_license::Column::License` column, joined via `InnerJoin` to the `PackageLicense` relation:

```rust
if let Some(licenses) = license_filter {
    query = query.filter(
        Condition::any()
            .add(package_license::Column::License.is_in(licenses.iter().cloned()))
    );
    query = query.join(JoinType::InnerJoin, package::Relation::PackageLicense.def());
}
```

For a single value like `MIT`, the `validate_license_param` function splits on commas, producing a single-element vector `["MIT"]`. The `is_in` clause then filters to only packages whose license matches `MIT`.

The integration test `test_list_packages_single_license_filter` in `tests/api/package.rs` seeds packages with MIT and Apache-2.0 licenses, queries with `?license=MIT`, and asserts that only 2 MIT-licensed packages are returned with all items having `license == "MIT"`.

## Reasoning

The endpoint correctly parses the `license` query parameter, validates it as a valid SPDX identifier, and applies it as a WHERE clause filter via an inner join to the package_license table. A single license value results in a single-element `is_in` filter that returns only matching packages. The test confirms the expected behavior.
