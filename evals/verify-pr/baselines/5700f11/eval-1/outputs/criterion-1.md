## Criterion 1: `GET /api/v2/package?license=MIT` returns only packages with MIT license

### Result: PASS

### Reasoning

The PR implements this criterion through two coordinated changes:

**Endpoint layer** (`modules/fundamental/src/package/endpoints/list.rs`):
- The `PackageListParams` struct now includes `pub license: Option<String>`, which Axum's `Query` extractor will automatically parse from the `?license=MIT` query parameter.
- When `params.license` is `Some`, the handler calls `validate_license_param(license)` which parses each identifier via `spdx::Expression::parse(id)` to confirm it is a valid SPDX identifier, then returns a `Vec<String>` of validated identifiers.
- The validated identifiers are passed as `license_filter: Option<&[String]>` to `PackageService::list()`.

**Service layer** (`modules/fundamental/src/package/service/mod.rs`):
- When `license_filter` is `Some`, the query builder adds a `Condition::any()` with `package_license::Column::License.is_in(licenses.iter().cloned())`, restricting results to packages whose associated `package_license` record matches the given identifier(s).
- An `InnerJoin` to `package::Relation::PackageLicense` ensures the filter applies through the correct entity relationship.

**Test coverage** (`tests/api/package.rs`):
- `test_list_packages_single_license_filter` seeds packages with MIT and Apache-2.0 licenses, requests `?license=MIT`, and asserts that only 2 packages are returned and all have `license == "MIT"`.

The implementation correctly filters packages by a single SPDX license identifier, and the test validates the expected behavior.
