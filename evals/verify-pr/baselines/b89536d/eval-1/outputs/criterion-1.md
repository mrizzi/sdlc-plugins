## Criterion 1: `GET /api/v2/package?license=MIT` returns only packages with MIT license

### Verdict: PASS

### Reasoning

The PR diff adds a `license` query parameter to the `PackageListParams` struct in `modules/fundamental/src/package/endpoints/list.rs`:

```rust
pub license: Option<String>,
```

When this parameter is present, the `validate_license_param` function parses the comma-separated value and validates each identifier as a valid SPDX expression using `Expression::parse(id)`. The validated identifiers are then passed to `PackageService::list()` as `license_filter: Option<&[String]>`.

In `modules/fundamental/src/package/service/mod.rs`, the `list` method applies a filter when `license_filter` is `Some`:

```rust
if let Some(licenses) = license_filter {
    query = query.filter(
        Condition::any()
            .add(package_license::Column::License.is_in(licenses.iter().cloned()))
    );
    query = query.join(JoinType::InnerJoin, package::Relation::PackageLicense.def());
}
```

This filters the query to only include packages whose license column matches one of the provided identifiers. For a single value like `?license=MIT`, the `is_in` clause effectively becomes an equality check, returning only packages with MIT license.

The integration test `test_list_packages_single_license_filter` in `tests/api/package.rs` verifies this behavior by seeding packages with MIT and Apache-2.0 licenses, requesting `?license=MIT`, and asserting that only 2 MIT-licensed packages are returned and all have `license == "MIT"`.

### Evidence

- `modules/fundamental/src/package/endpoints/list.rs`: `license` field added to `PackageListParams`, `validate_license_param` function validates SPDX identifiers
- `modules/fundamental/src/package/service/mod.rs`: `is_in` filter applied with `InnerJoin` to `PackageLicense` table
- `tests/api/package.rs`: `test_list_packages_single_license_filter` seeds MIT and Apache-2.0 packages, asserts only MIT packages returned
