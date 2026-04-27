## Criterion 1: `GET /api/v2/package?license=MIT` returns only packages with MIT license

### Result: PASS

### Reasoning

**Endpoint layer (`modules/fundamental/src/package/endpoints/list.rs`):**
The `PackageListParams` struct has been extended with an optional `license: Option<String>` field. When a request arrives at `GET /api/v2/package?license=MIT`, Axum's `Query` extractor deserializes this into `params.license = Some("MIT")`. The handler then calls `validate_license_param("MIT")`, which splits on commas, trims whitespace, and validates each identifier using `Expression::parse(id)` from the `spdx` crate. For the single value `MIT`, this produces `Ok(vec!["MIT".to_string()])`. The validated identifiers are passed to `PackageService::list()` as `Some(&["MIT"])`.

**Service layer (`modules/fundamental/src/package/service/mod.rs`):**
The `list` method signature now includes `license_filter: Option<&[String]>`. When `Some(licenses)` is provided, two operations are applied to the query:
1. A filter using `Condition::any().add(package_license::Column::License.is_in(licenses.iter().cloned()))` -- this generates a SQL `WHERE license IN ('MIT')` clause.
2. An `InnerJoin` on `package::Relation::PackageLicense` -- this joins the package table with the package_license table, ensuring only packages that have a matching license record are included in results.

The combination of the inner join and the `IN` filter correctly restricts results to only those packages whose associated `package_license` record has `license = 'MIT'`. Packages with other licenses (e.g., Apache-2.0) are excluded because the inner join produces no matching rows for them.

**Test validation:**
The integration test `test_list_packages_single_license_filter` in `tests/api/package.rs` directly validates this criterion:
- Seeds 3 packages: `pkg-a` (MIT), `pkg-b` (Apache-2.0), `pkg-c` (MIT)
- Sends `GET /api/v2/package?license=MIT`
- Asserts response status is 200 OK
- Asserts exactly 2 items are returned
- Asserts all returned items have `license == "MIT"`

This confirms the filter correctly returns only MIT-licensed packages and excludes others.
