## Criterion 1: `GET /api/v2/package?license=MIT` returns only packages with MIT license

**Verdict: PASS**

### Reasoning

The PR diff implements license filtering at two layers, both of which support single-license filtering:

**Endpoint layer (`modules/fundamental/src/package/endpoints/list.rs`):**
- The `PackageListParams` struct adds a `pub license: Option<String>` field, which Axum's `Query` extractor will populate from the `?license=MIT` query parameter.
- The `validate_license_param` function splits the license string on commas and validates each identifier via `spdx::Expression::parse()`. For a single license value like `MIT`, this produces a `Vec<String>` with one element `["MIT"]`.
- The `list_packages` handler passes the validated identifiers to `PackageService::list()` as `license_filter`.

**Service layer (`modules/fundamental/src/package/service/mod.rs`):**
- The `list` method now accepts `license_filter: Option<&[String]>`.
- When `Some(licenses)` is provided, it applies a `Condition::any()` filter with `package_license::Column::License.is_in(licenses.iter().cloned())` -- this generates a SQL `WHERE license IN ('MIT')` clause.
- An `InnerJoin` to `PackageLicense` ensures only packages with a matching license row are returned.

**Test verification (`tests/api/package.rs`):**
- The `test_list_packages_single_license_filter` test seeds packages with `MIT` and `Apache-2.0` licenses, queries `?license=MIT`, and asserts that:
  - The response status is 200 OK
  - Exactly 2 items are returned (the two MIT packages)
  - All returned items have `license == "MIT"`

This comprehensively demonstrates that the single-license filter works correctly.
