## Criterion 1: Single License Filter

**Requirement**: `GET /api/v2/package?license=MIT` returns only packages with MIT license.

**Verdict**: PASS

### Analysis

**Parameter Parsing**: The `PackageListParams` struct in `list.rs` now includes `pub license: Option<String>`, which Axum's `Query` extractor will populate from the `?license=MIT` query parameter.

**Validation**: The `validate_license_param` function splits the license string by comma, trims whitespace, and validates each identifier using `spdx::Expression::parse()`. For a single value like `MIT`, this produces a `Vec<String>` containing one element `["MIT"]`. If parsing fails, it returns `AppError::BadRequest`.

**Filtering**: In the `list_packages` handler, the validated license identifiers are passed to `PackageService::list()` as `license_filter: Option<&[String]>`. The service method applies the filter using:

```rust
if let Some(licenses) = license_filter {
    query = query.filter(
        Condition::any()
            .add(package_license::Column::License.is_in(licenses.iter().cloned()))
    );
    query = query.join(JoinType::InnerJoin, package::Relation::PackageLicense.def());
}
```

This joins the `package_license` table and filters to rows where the license column matches any of the provided values. For a single value, this effectively becomes `WHERE package_license.license = 'MIT'`.

**Test Coverage**: `test_list_packages_single_license_filter` seeds 3 packages (2 MIT, 1 Apache-2.0), queries with `?license=MIT`, and asserts:
- Response status is 200 OK
- Exactly 2 items are returned
- All returned items have license == "MIT"
