## Criterion 1: `GET /api/v2/package?license=MIT` returns only packages with MIT license

### Verdict: PASS

### Reasoning

The PR implements single-license filtering through the following code path:

1. **Endpoint layer** (`modules/fundamental/src/package/endpoints/list.rs`): The `PackageListParams` struct now includes an optional `license: Option<String>` field. When present, the `list_packages` handler calls `validate_license_param(license)` which splits on commas and validates each identifier as a valid SPDX expression. For a single value like `MIT`, this produces `Some(vec!["MIT".to_string()])`.

2. **Service layer** (`modules/fundamental/src/package/service/mod.rs`): The `PackageService::list` method now accepts `license_filter: Option<&[String]>`. When `Some(licenses)` is provided, it applies:
   - A `Condition::any()` filter with `package_license::Column::License.is_in(licenses.iter().cloned())` -- for a single license `["MIT"]`, this generates a SQL `WHERE license IN ('MIT')` clause
   - An `InnerJoin` on `package::Relation::PackageLicense` to join the package table to the package_license table

   This correctly filters packages to only those whose license column matches `MIT`.

3. **Test coverage** (`tests/api/package.rs`): The `test_list_packages_single_license_filter` test seeds three packages (two with MIT, one with Apache-2.0), requests `?license=MIT`, and asserts:
   - Response status is 200 OK
   - Result contains exactly 2 items
   - All items have `license == "MIT"`

   This directly validates the criterion.

### Evidence

- `list.rs`: `pub license: Option<String>` added to `PackageListParams`
- `list.rs`: `validate_license_param` splits on comma and validates via `Expression::parse`
- `mod.rs`: `license_filter: Option<&[String]>` parameter added to `PackageService::list`
- `mod.rs`: `Condition::any().add(package_license::Column::License.is_in(...))` applies the filter
- `mod.rs`: `InnerJoin` on `PackageLicense` relation ensures only packages with matching licenses are returned
- `package.rs` test: `test_list_packages_single_license_filter` directly tests this criterion with MIT filter
