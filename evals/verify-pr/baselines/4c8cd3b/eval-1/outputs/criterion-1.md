## Criterion 1: `GET /api/v2/package?license=MIT` returns only packages with MIT license

### Result: PASS

### Reasoning

**Endpoint layer (`modules/fundamental/src/package/endpoints/list.rs`):**
The `PackageListParams` struct now includes an optional `license: Option<String>` field. When a request arrives with `?license=MIT`, Axum's `Query` extractor deserializes this into `Some("MIT")`. The handler then calls `validate_license_param(license)`, which splits the string on commas, trims whitespace, and validates each identifier using `Expression::parse(id)` from the `spdx` crate. For a single value like `MIT`, this produces `Vec<String>` containing `["MIT"]`, which is passed to `PackageService::list()` as `Some(&["MIT"])`.

**Service layer (`modules/fundamental/src/package/service/mod.rs`):**
The `list` method now accepts `license_filter: Option<&[String]>`. When `Some(licenses)` is provided, two operations are applied to the query:
1. A `Condition::any()` with `package_license::Column::License.is_in(licenses.iter().cloned())` -- this generates a SQL `WHERE license IN ('MIT')` clause.
2. An `InnerJoin` on `package::Relation::PackageLicense` -- this ensures only packages that have a matching entry in the `package_license` table are included.

The combination of the `INNER JOIN` and `IN` filter correctly restricts results to only packages whose associated `package_license` record matches `MIT`. Packages without a MIT license entry are excluded by the inner join.

**Test coverage:**
The test `test_list_packages_single_license_filter` in `tests/api/package.rs` seeds three packages (two with MIT, one with Apache-2.0), requests `?license=MIT`, and asserts:
- Response status is 200 OK
- Exactly 2 items are returned
- All returned items have `license == "MIT"`

This directly validates the criterion.
