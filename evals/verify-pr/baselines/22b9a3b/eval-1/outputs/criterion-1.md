## Criterion 1: `GET /api/v2/package?license=MIT` returns only packages with MIT license

### Result: PASS

### Reasoning

**Endpoint layer (`modules/fundamental/src/package/endpoints/list.rs`):**
The `PackageListParams` struct has been extended with an optional `license: Option<String>` field. When a request arrives with `?license=MIT`, Axum's `Query` extractor deserializes the query parameter into this field. In the `list_packages` handler, when `params.license` is `Some("MIT")`, the handler calls `validate_license_param("MIT")`. This function splits the string on commas, trims whitespace, and validates each identifier via `spdx::Expression::parse(id)`. Since `MIT` is a valid SPDX license identifier, validation succeeds and produces `vec!["MIT".to_string()]`. This is passed to `PackageService::list()` as `Some(&["MIT"])`.

**Service layer (`modules/fundamental/src/package/service/mod.rs`):**
The `list` method now accepts a `license_filter: Option<&[String]>` parameter. When `Some(licenses)` is provided, two query modifications are applied:
1. A `Condition::any()` filter with `package_license::Column::License.is_in(licenses.iter().cloned())` is added, which generates a SQL `WHERE license IN ('MIT')` clause.
2. An `InnerJoin` on `package::Relation::PackageLicense` is added, ensuring only packages that have a matching row in the `package_license` table are returned.

The combination of the inner join and the `IN` filter correctly restricts results to only packages whose associated `package_license` record has `license = 'MIT'`. Packages with other licenses or no license are excluded by the inner join semantics.

**Test coverage:**
The integration test `test_list_packages_single_license_filter` in `tests/api/package.rs` directly validates this criterion:
- Seeds 3 packages: `pkg-a` (MIT), `pkg-b` (Apache-2.0), `pkg-c` (MIT)
- Requests `GET /api/v2/package?license=MIT`
- Asserts HTTP 200 status
- Asserts exactly 2 items returned
- Asserts all returned items have `license == "MIT"`

This confirms the filtering returns only MIT-licensed packages and excludes non-matching packages.
