## Criterion 1: `GET /api/v2/package?license=MIT` returns only packages with MIT license

### Result: PASS

### Reasoning

**Endpoint layer (`list.rs`):**
The `PackageListParams` struct now includes an optional `license: Option<String>` field, which Axum will automatically deserialize from the `?license=MIT` query parameter. In `list_packages`, when `params.license` is `Some(...)`, the handler calls `validate_license_param(license)` which splits on commas, trims whitespace, and validates each identifier as a valid SPDX expression via `Expression::parse(id)`. For a single value like `MIT`, this produces a `Vec<String>` containing `["MIT"]`, which is passed to `PackageService::list()` as `Some(&["MIT"])`.

**Service layer (`service/mod.rs`):**
The `list` method now accepts `license_filter: Option<&[String]>`. When `Some(licenses)` is provided, it applies:
1. A `Condition::any()` with `package_license::Column::License.is_in(licenses.iter().cloned())` -- this builds a SQL `WHERE license IN ('MIT')` clause.
2. An `InnerJoin` on `package::Relation::PackageLicense` -- this ensures only packages that have a matching license row are returned.

The `INNER JOIN` combined with the `IN` filter correctly ensures that only packages whose associated `package_license` record matches `MIT` are returned. Packages without a `MIT` license row are excluded by the inner join.

**Test coverage:**
The test `test_list_packages_single_license_filter` seeds three packages (two with MIT, one with Apache-2.0), requests `?license=MIT`, and asserts:
- Status is 200 OK
- Exactly 2 items returned
- All items have `license == "MIT"`

This directly validates the criterion.
