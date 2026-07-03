# Criterion 1: GET /api/v2/package?license=MIT returns only packages with MIT license

## Verdict: PASS

## Analysis

### Endpoint Layer (list.rs)

The `PackageListParams` struct adds a `pub license: Option<String>` field, which means Axum's `Query` extractor will automatically parse the `license` query parameter from the URL. When a request arrives at `GET /api/v2/package?license=MIT`, the `params.license` field will be `Some("MIT")`.

In the `list_packages` handler, the code checks `params.license` via a `match` expression:

```rust
let license_filter = match &params.license {
    Some(license) => Some(validate_license_param(license)?),
    None => None,
};
```

When `license` is `Some("MIT")`, it calls `validate_license_param("MIT")` which:
1. Splits the string on commas: produces `["MIT"]`
2. Trims whitespace from each part
3. Validates each identifier using `spdx::Expression::parse("MIT")` -- MIT is a valid SPDX identifier, so this succeeds
4. Returns `Ok(vec!["MIT".to_string()])`

The resulting filter is passed to the service via `license_filter.as_deref()`, which converts `Option<Vec<String>>` to `Option<&[String]>`.

### Service Layer (mod.rs)

The `list` method receives `license_filter: Option<&[String]>`. When `Some(["MIT"])` is provided:

```rust
if let Some(licenses) = license_filter {
    query = query.filter(
        Condition::any()
            .add(package_license::Column::License.is_in(licenses.iter().cloned()))
    );
    query = query.join(JoinType::InnerJoin, package::Relation::PackageLicense.def());
}
```

This adds an `INNER JOIN` to the `package_license` table and a `WHERE package_license.license IN ('MIT')` clause. The combination of INNER JOIN and IN filter ensures only packages with a matching license record are returned.

The filtered query is used for both `count()` (total) and the paginated item fetch, so both the total count and the returned items reflect only MIT-licensed packages.

### Test Coverage

`test_list_packages_single_license_filter` validates this criterion:
- Seeds 3 packages: pkg-a (MIT), pkg-b (Apache-2.0), pkg-c (MIT)
- Queries `GET /api/v2/package?license=MIT`
- Asserts response status is 200 OK
- Asserts exactly 2 items returned
- Asserts all returned items have `license == "MIT"`

This directly verifies the criterion's requirement.

## Conclusion

The implementation correctly accepts the `license` query parameter, validates it as a valid SPDX identifier, filters packages via an INNER JOIN with the package_license table, and returns only matching packages. The test confirms the expected behavior with concrete assertions on both count and content.
