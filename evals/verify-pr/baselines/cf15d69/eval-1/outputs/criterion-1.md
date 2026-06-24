# Criterion 1: `GET /api/v2/package?license=MIT` returns only packages with MIT license

## Verdict: PASS

## Reasoning

The PR diff implements this criterion through two coordinated changes:

1. **Endpoint parameter parsing** (`modules/fundamental/src/package/endpoints/list.rs`):
   - The `PackageListParams` struct now includes `pub license: Option<String>`, which Axum's `Query` extractor will automatically parse from the `?license=MIT` query parameter.
   - The `validate_license_param` function parses the license string and validates it against SPDX expressions using `Expression::parse(id)`.
   - In `list_packages`, the license parameter is extracted and passed to the service layer: `let license_filter = match &params.license { Some(license) => Some(validate_license_param(license)?), None => None };`

2. **Service-layer filtering** (`modules/fundamental/src/package/service/mod.rs`):
   - The `list` method signature now accepts `license_filter: Option<&[String]>`.
   - When a license filter is provided, the query adds a `Condition::any()` with `package_license::Column::License.is_in(licenses.iter().cloned())` and joins the `PackageLicense` relation via `InnerJoin`.
   - This ensures only packages matching the specified license(s) are returned from the database.

3. **Test coverage** (`tests/api/package.rs`):
   - `test_list_packages_single_license_filter` seeds packages with MIT and Apache-2.0 licenses, queries with `?license=MIT`, and asserts that exactly 2 packages are returned and all have `license == "MIT"`.

The implementation correctly filters at the database level using an inner join on the package-license relationship, ensuring only matching packages are returned.
