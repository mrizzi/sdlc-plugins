# Criterion 1: `GET /api/v2/package?license=MIT` returns only packages with MIT license

## Verdict: PASS

## Analysis

### What was checked

This criterion requires that when a single license value is provided as a query parameter, only packages matching that license are returned.

### Evidence from the diff

1. **Query parameter parsing** (`modules/fundamental/src/package/endpoints/list.rs`):
   - The `PackageListParams` struct now includes `pub license: Option<String>`, which Axum's `Query` extractor will populate from the `?license=MIT` query string.

2. **Validation** (`modules/fundamental/src/package/endpoints/list.rs`):
   - The `validate_license_param` function splits the license string on commas and validates each identifier using `spdx::Expression::parse(id)`. For a single value like `MIT`, this produces a `Vec<String>` containing `["MIT"]`.

3. **Filter application** (`modules/fundamental/src/package/service/mod.rs`):
   - The `list` method now accepts `license_filter: Option<&[String]>`.
   - When `Some(licenses)` is provided, it applies `Condition::any().add(package_license::Column::License.is_in(licenses.iter().cloned()))` and joins via `package::Relation::PackageLicense`.
   - This produces a SQL WHERE clause filtering to only packages whose associated license matches one of the provided identifiers. For a single value, this effectively filters to `WHERE license = 'MIT'`.

4. **Test coverage** (`tests/api/package.rs`):
   - `test_list_packages_single_license_filter` seeds three packages (two MIT, one Apache-2.0), queries `?license=MIT`, and asserts:
     - Response status is 200 OK
     - Exactly 2 items returned
     - All items have `license == "MIT"`

### Conclusion

The implementation correctly parses the single license query parameter, validates it against the SPDX specification, applies the filter at the database query level via an inner join to the package_license table, and returns only matching packages. The test confirms the expected behavior.
