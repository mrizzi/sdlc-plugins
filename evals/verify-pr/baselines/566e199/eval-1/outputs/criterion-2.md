# Criterion 2: `GET /api/v2/package?license=MIT,Apache-2.0` returns packages with either license

## Verdict: PASS

## Reasoning

The PR diff implements comma-separated multi-license filtering through the validation function and the query builder:

**Validation (`modules/fundamental/src/package/endpoints/list.rs`):**
- `validate_license_param` splits the license string on commas: `license.split(',').map(|s| s.trim().to_string()).collect()`.
- For input `"MIT,Apache-2.0"`, this produces `["MIT", "Apache-2.0"]`.
- Each identifier is individually validated via `Expression::parse(id)`, ensuring both are valid SPDX identifiers before proceeding.

**Query construction (`modules/fundamental/src/package/service/mod.rs`):**
- The `license_filter` receives `Some(&["MIT", "Apache-2.0"])`.
- The filter uses `Condition::any().add(package_license::Column::License.is_in(licenses.iter().cloned()))`.
- `Condition::any()` with `is_in` produces SQL equivalent to `WHERE package_license.license IN ('MIT', 'Apache-2.0')`, which returns the union of packages matching either license.
- The `InnerJoin` on `PackageLicense` ensures only packages with a matching license association are included.

**Test coverage (`tests/api/package.rs`):**
- `test_list_packages_multi_license_filter` seeds three packages: `pkg-a` (MIT), `pkg-b` (Apache-2.0), `pkg-c` (GPL-3.0-only).
- It requests `GET /api/v2/package?license=MIT,Apache-2.0` and asserts:
  - Response status is 200 OK
  - Result contains exactly 2 items (MIT and Apache-2.0, excluding GPL-3.0-only)
  - All returned items have license matching either `"MIT"` or `"Apache-2.0"`
- This directly validates the union behavior required by the acceptance criterion.

The implementation correctly handles the comma-separated multi-license filter producing the union of matching packages.
