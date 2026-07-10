# Criterion 1: `GET /api/v2/package?license=MIT` returns only packages with MIT license

## Verdict: PASS

## Analysis

### Code Changes

The PR adds a `license` query parameter to the `PackageListParams` struct in `modules/fundamental/src/package/endpoints/list.rs`:

```rust
pub struct PackageListParams {
    pub offset: Option<i64>,
    pub limit: Option<i64>,
    pub license: Option<String>,
}
```

When the `license` parameter is present, the handler calls `validate_license_param(license)` which parses the value and validates each identifier against the `spdx::Expression` parser. For a single value like `MIT`, this produces a `Vec<String>` containing one element: `["MIT"]`.

The validated identifiers are passed to `PackageService::list()` as `license_filter: Option<&[String]>`. In the service layer (`modules/fundamental/src/package/service/mod.rs`), when `license_filter` is `Some`, the query is filtered:

```rust
if let Some(licenses) = license_filter {
    query = query.filter(
        Condition::any()
            .add(package_license::Column::License.is_in(licenses.iter().cloned()))
    );
    query = query.join(JoinType::InnerJoin, package::Relation::PackageLicense.def());
}
```

This applies an `INNER JOIN` with the `package_license` table and a `WHERE license IN ('MIT')` condition, ensuring only packages whose license matches MIT are returned.

### Test Coverage

The test `test_list_packages_single_license_filter` seeds three packages (pkg-a with MIT, pkg-b with Apache-2.0, pkg-c with MIT), queries with `?license=MIT`, and asserts:
- Response status is 200 OK
- Exactly 2 items returned
- All items have `license == "MIT"`

This directly validates the criterion.

### Conclusion

The implementation correctly adds the `license` query parameter, validates it as a valid SPDX identifier, and filters the database query to return only matching packages. The test confirms the expected behavior end-to-end. Criterion is satisfied.
