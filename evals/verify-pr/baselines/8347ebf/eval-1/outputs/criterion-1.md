# Criterion 1: `GET /api/v2/package?license=MIT` returns only packages with MIT license

## Verdict: PASS

## Reasoning

The PR diff demonstrates that this criterion is satisfied through both implementation code and test coverage.

### Implementation Evidence

1. **Query parameter parsing** (`modules/fundamental/src/package/endpoints/list.rs`):
   - The `PackageListParams` struct now includes a `pub license: Option<String>` field, which Axum's `Query` extractor will populate from the `?license=MIT` query string.

2. **Validation** (`validate_license_param` function in `list.rs`):
   - The `validate_license_param` function splits the license string by comma, trims whitespace, and parses each identifier using `spdx::Expression::parse()`. For a single value like `MIT`, this produces a `Vec<String>` containing one element: `["MIT"]`.

3. **Filtering** (`modules/fundamental/src/package/service/mod.rs`):
   - The `list` method now accepts an `Option<&[String]>` parameter for `license_filter`.
   - When `Some(licenses)` is provided, it applies a `Condition::any()` filter using `package_license::Column::License.is_in(licenses.iter().cloned())`, which generates a SQL `WHERE license IN ('MIT')` clause.
   - An `InnerJoin` on `package::Relation::PackageLicense` ensures only packages with a matching license entry are returned.

4. **Wiring** (`list_packages` handler in `list.rs`):
   - The handler extracts the license parameter, validates it via `validate_license_param`, and passes the result as `license_filter.as_deref()` to `PackageService::list()`. The `?` operator ensures validation errors short-circuit as 400 responses.

### Test Evidence

The test `test_list_packages_single_license_filter` in `tests/api/package.rs`:
- Seeds three packages: `pkg-a` (MIT), `pkg-b` (Apache-2.0), `pkg-c` (MIT)
- Requests `GET /api/v2/package?license=MIT`
- Asserts response status is 200 OK
- Asserts exactly 2 items are returned
- Asserts all returned items have `license == "MIT"`

This test directly validates the criterion's requirement that only MIT-licensed packages are returned when filtering by `?license=MIT`.
