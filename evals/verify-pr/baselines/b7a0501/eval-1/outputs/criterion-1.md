## Criterion 1: `GET /api/v2/package?license=MIT` returns only packages with MIT license

**Result: PASS**

**Evidence from diff:**

1. **Query parameter parsing** (`modules/fundamental/src/package/endpoints/list.rs`): The `PackageListParams` struct now includes `pub license: Option<String>`, which means `?license=MIT` is deserialized from the query string by Axum's `Query` extractor.

2. **Validation** (`list.rs`): The `validate_license_param` function parses the license string, splitting by comma and validating each identifier against the SPDX expression parser. A single value like `MIT` will pass validation and be returned as a `Vec<String>` containing one element.

3. **Filtering** (`modules/fundamental/src/package/service/mod.rs`): The `list` method now accepts `license_filter: Option<&[String]>`. When `Some`, it applies a `Condition::any()` filter with `package_license::Column::License.is_in(licenses)` and joins the `PackageLicense` table. This ensures only packages whose license matches one of the provided values are returned.

4. **Test coverage** (`tests/api/package.rs`): The test `test_list_packages_single_license_filter` seeds packages with MIT and Apache-2.0 licenses, queries `?license=MIT`, and asserts that only 2 packages are returned, all with `license == "MIT"`.

The full chain from query parameter parsing through validation, filtering, and response is implemented correctly for single-license filtering.
