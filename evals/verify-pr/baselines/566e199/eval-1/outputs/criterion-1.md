# Criterion 1: `GET /api/v2/package?license=MIT` returns only packages with MIT license

## Verdict: PASS

## Reasoning

The PR diff implements this criterion through coordinated changes across the endpoint and service layers:

**Endpoint layer (`modules/fundamental/src/package/endpoints/list.rs`):**
- The `PackageListParams` struct now includes `pub license: Option<String>`, which allows Axum's `Query` extractor to parse the `?license=MIT` query parameter from the URL.
- The `list_packages` handler calls `validate_license_param(license)` when the parameter is present, which splits on commas, trims whitespace, and validates each identifier against the `spdx::Expression::parse` function. For a single value like `MIT`, this produces a `Vec<String>` containing `["MIT"]`.
- The validated license list is passed to `PackageService::list` as `license_filter: Option<&[String]>`.

**Service layer (`modules/fundamental/src/package/service/mod.rs`):**
- When `license_filter` is `Some(licenses)`, the service adds a `Condition::any()` filter with `package_license::Column::License.is_in(licenses.iter().cloned())` and joins on `package::Relation::PackageLicense`.
- This generates SQL that filters packages whose associated license record matches any of the provided license identifiers. For a single `MIT` value, this effectively becomes `WHERE package_license.license IN ('MIT')`.
- The `InnerJoin` ensures only packages that have a matching license association are returned.

**Test coverage (`tests/api/package.rs`):**
- `test_list_packages_single_license_filter` seeds three packages: `pkg-a` (MIT), `pkg-b` (Apache-2.0), `pkg-c` (MIT).
- It requests `GET /api/v2/package?license=MIT` and asserts:
  - Response status is 200 OK
  - Result contains exactly 2 items
  - All returned items have `license == "MIT"`
- This directly validates the acceptance criterion.

The implementation correctly handles the single-license filter case end-to-end.
