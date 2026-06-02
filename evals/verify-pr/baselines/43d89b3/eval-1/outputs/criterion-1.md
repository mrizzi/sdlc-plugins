## Criterion 1: `GET /api/v2/package?license=MIT` returns only packages with MIT license

**Verdict: PASS**

### Analysis

The implementation satisfies this criterion through the following code path:

1. **Query parameter parsing:** In `modules/fundamental/src/package/endpoints/list.rs`, the `PackageListParams` struct now includes `pub license: Option<String>`. When a request like `?license=MIT` is made, Axum's `Query` extractor deserializes the `license` field to `Some("MIT")`.

2. **Validation:** The `validate_license_param()` function splits the license string by commas and validates each identifier using `spdx::Expression::parse()`. For a single value like `"MIT"`, this produces a `Vec` containing one element `["MIT"]`. MIT is a valid SPDX identifier, so validation passes.

3. **Filtering in service layer:** In `modules/fundamental/src/package/service/mod.rs`, the `list()` method receives `license_filter: Option<&[String]>`. When `Some(["MIT"])` is provided:
   - A `Condition::any()` filter is built with `package_license::Column::License.is_in(["MIT"])`, which generates a SQL `WHERE license IN ('MIT')` clause.
   - An `InnerJoin` on `package::Relation::PackageLicense` ensures only packages with a matching license record are returned.

4. **Test coverage:** The test `test_list_packages_single_license_filter` in `tests/api/package.rs` seeds packages with MIT and Apache-2.0 licenses, filters by `?license=MIT`, and asserts:
   - Response status is 200 OK
   - Only 2 packages are returned (the two MIT-licensed ones)
   - All returned packages have `license == "MIT"`

### Evidence

- `list.rs` line: `pub license: Option<String>` added to `PackageListParams`
- `list.rs` function: `validate_license_param` parses and validates the license parameter
- `service/mod.rs`: `Condition::any().add(package_license::Column::License.is_in(licenses.iter().cloned()))` applies the filter
- `tests/api/package.rs`: `test_list_packages_single_license_filter` covers this exact scenario
