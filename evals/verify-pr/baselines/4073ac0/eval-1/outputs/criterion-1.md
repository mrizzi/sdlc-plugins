# Criterion 1: `GET /api/v2/package?license=MIT` returns only packages with MIT license

## Verdict: PASS

## Reasoning

The PR implements single-license filtering in two layers:

**Endpoint layer (`modules/fundamental/src/package/endpoints/list.rs`):**
- The `PackageListParams` struct now includes `pub license: Option<String>`, which Axum's `Query` extractor will populate from the `?license=MIT` query parameter.
- When `params.license` is `Some(license)`, the handler calls `validate_license_param(license)` which splits on commas and validates each identifier via `spdx::Expression::parse()`. For a single value like `MIT`, this produces a `Vec<String>` containing `["MIT"]`.
- The validated identifiers are passed to `PackageService::list()` as `license_filter: Option<&[String]>`.

**Service layer (`modules/fundamental/src/package/service/mod.rs`):**
- When `license_filter` is `Some(licenses)`, the service applies a filter using `Condition::any().add(package_license::Column::License.is_in(licenses.iter().cloned()))` with an `InnerJoin` to the `PackageLicense` relation.
- This ensures only packages whose `package_license` record has `License = "MIT"` are included in the result set.
- The `is_in` clause with a single-element slice is functionally equivalent to an equality check.

**Test verification (`tests/api/package.rs`):**
- `test_list_packages_single_license_filter` seeds three packages (two MIT, one Apache-2.0), queries `?license=MIT`, and asserts that exactly 2 packages are returned, all with `license == "MIT"`.

The implementation correctly handles the single-license filter case. The query parameter is parsed, validated, and applied to the database query, returning only matching packages.
