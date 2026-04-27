# Criterion 1: `GET /api/v2/package?license=MIT` returns only packages with MIT license

## Result: PASS

## Analysis

The diff implements single-license filtering through the following changes:

### Endpoint layer (`modules/fundamental/src/package/endpoints/list.rs`)

- The `PackageListParams` struct now includes `pub license: Option<String>`, which Axum's `Query` extractor will populate from the `?license=MIT` query parameter.
- In `list_packages`, when `params.license` is `Some`, the value is passed to `validate_license_param`, which splits on commas and validates each identifier against the SPDX expression parser. For a single value like `MIT`, this produces `Some(vec!["MIT".to_string()])`.
- The validated identifiers are passed to `PackageService::list` as `license_filter: Option<&[String]>`.

### Service layer (`modules/fundamental/src/package/service/mod.rs`)

- When `license_filter` is `Some`, the service adds a `Condition::any()` filter using `package_license::Column::License.is_in(licenses.iter().cloned())`, which produces a SQL `WHERE package_license.license IN ('MIT')` clause.
- An `InnerJoin` to the `PackageLicense` relation ensures only packages that have a matching license record are returned.

### Test coverage

- `test_list_packages_single_license_filter` seeds three packages (two MIT, one Apache-2.0), requests `?license=MIT`, and asserts that exactly 2 packages are returned, all with `license == "MIT"`.

The implementation correctly filters packages by a single license identifier. The query parameter is parsed, validated, converted to a database filter, and tested end-to-end.
