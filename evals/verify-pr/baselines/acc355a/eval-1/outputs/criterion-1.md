## Criterion 1: `GET /api/v2/package?license=MIT` returns only packages with MIT license

### Verdict: PASS

### Evidence

**Endpoint layer (`list.rs`):**
- The `PackageListParams` struct now includes `pub license: Option<String>` (line 5 of the diff addition), which binds the `license` query parameter from the request URL.
- The `validate_license_param` function parses the comma-separated license string and validates each identifier against SPDX expressions using `Expression::parse(id)`.
- In `list_packages`, when `params.license` is `Some`, the validated identifiers are passed to `PackageService::list` as `license_filter`.

**Service layer (`service/mod.rs`):**
- The `list` method now accepts `license_filter: Option<&[String]>`.
- When `license_filter` is `Some(licenses)`, the query adds a filter: `package_license::Column::License.is_in(licenses.iter().cloned())` with an `InnerJoin` on `package::Relation::PackageLicense`.
- This ensures only packages whose associated license record matches the provided identifiers are returned.

**Test evidence (`tests/api/package.rs`):**
- `test_list_packages_single_license_filter` seeds packages with MIT and Apache-2.0 licenses, requests `?license=MIT`, and asserts:
  - Response status is 200 OK
  - Exactly 2 items are returned (the two MIT packages)
  - All returned items have `license == "MIT"`

The implementation correctly filters by a single license identifier via the query parameter, the service applies the WHERE clause, and a dedicated test verifies the behavior.
