## Criterion 1: `GET /api/v2/package?license=MIT` returns only packages with MIT license

### Analysis

The PR diff adds a `license` query parameter to `PackageListParams` in `list.rs`:

```rust
pub license: Option<String>,
```

When the `license` parameter is present, it calls `validate_license_param(license)` which splits by comma, validates each identifier via `spdx::Expression::parse`, and returns the list of identifiers.

The validated identifiers are passed to `PackageService::list()` as `license_filter: Option<&[String]>`.

In `service/mod.rs`, the filter is applied:

```rust
if let Some(licenses) = license_filter {
    query = query.filter(
        Condition::any()
            .add(package_license::Column::License.is_in(licenses.iter().cloned()))
    );
    query = query.join(JoinType::InnerJoin, package::Relation::PackageLicense.def());
}
```

With a single license value like `MIT`, `Condition::any()` with `is_in(["MIT"])` will filter to only packages whose `package_license.license` column matches "MIT". The `InnerJoin` to `PackageLicense` ensures only packages with a matching license record are returned.

The test `test_list_packages_single_license_filter` seeds MIT and Apache-2.0 packages, filters by MIT, and asserts `body.items.len() == 2` and all items have `license == "MIT"`.

### Code Evidence

- `list.rs`: `license: Option<String>` field added to `PackageListParams`
- `list.rs`: `validate_license_param` function parses and validates
- `service/mod.rs`: `is_in(licenses.iter().cloned())` applies the filter
- `tests/api/package.rs`: `test_list_packages_single_license_filter` verifies this behavior

## Verdict: PASS
