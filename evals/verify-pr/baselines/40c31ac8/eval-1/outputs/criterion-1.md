## Criterion 1: `GET /api/v2/package?license=MIT` returns only packages with MIT license

**Result: PASS**

### Evidence

**Endpoint layer (`modules/fundamental/src/package/endpoints/list.rs`):**

The `PackageListParams` struct now includes an optional `license` field:

```rust
pub struct PackageListParams {
    pub offset: Option<i64>,
    pub limit: Option<i64>,
    pub license: Option<String>,
}
```

When a request is made with `?license=MIT`, Axum's `Query` extractor deserializes the query string into this struct, populating `license` with `Some("MIT")`.

The handler `list_packages` passes the license value through `validate_license_param`, which splits on commas and validates each identifier against the SPDX expression parser. For a single value like `MIT`, this produces `vec!["MIT"]`.

```rust
let license_filter = match &params.license {
    Some(license) => Some(validate_license_param(license)?),
    None => None,
};
```

The validated list is then passed to the service layer.

**Service layer (`modules/fundamental/src/package/service/mod.rs`):**

The `list` method now accepts `license_filter: Option<&[String]>`. When present, it applies an `is_in` filter on the `package_license::Column::License` column and performs an `InnerJoin` to the `PackageLicense` relation:

```rust
if let Some(licenses) = license_filter {
    query = query.filter(
        Condition::any()
            .add(package_license::Column::License.is_in(licenses.iter().cloned()))
    );
    query = query.join(JoinType::InnerJoin, package::Relation::PackageLicense.def());
}
```

This ensures that only packages whose associated license record matches `MIT` are returned. The `InnerJoin` excludes packages that have no license record at all.

**Test coverage (`tests/api/package.rs`):**

The test `test_list_packages_single_license_filter` seeds three packages (two with MIT, one with Apache-2.0), requests `?license=MIT`, and asserts:
- Response status is 200 OK
- Exactly 2 items are returned
- All returned items have `license == "MIT"`

This directly exercises the single-license filter path end-to-end.

### Conclusion

The implementation correctly parses a single license query parameter, validates it against SPDX, filters packages via the database query, and returns only matching results. The integration test confirms the expected behavior.
