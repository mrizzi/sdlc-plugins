# Criterion 2: `GET /api/v2/package?license=MIT,Apache-2.0` returns packages with either license

## Result: PASS

## Analysis

The diff implements comma-separated multi-license filtering:

### Endpoint layer (`modules/fundamental/src/package/endpoints/list.rs`)

- `validate_license_param` splits the license string on commas: `license.split(',').map(|s| s.trim().to_string()).collect()`. For input `MIT,Apache-2.0`, this produces `vec!["MIT", "Apache-2.0"]`.
- Each identifier is individually validated via `Expression::parse(id)`, ensuring all values in the list are valid SPDX identifiers.
- The full vector is passed to the service layer.

### Service layer (`modules/fundamental/src/package/service/mod.rs`)

- The filter uses `Condition::any()` with `is_in(licenses.iter().cloned())`, which produces a SQL `WHERE package_license.license IN ('MIT', 'Apache-2.0')` clause. The `any()` condition combined with `is_in` correctly returns packages matching any of the specified licenses (union semantics).

### Test coverage

- `test_list_packages_multi_license_filter` seeds three packages (MIT, Apache-2.0, GPL-3.0-only), requests `?license=MIT,Apache-2.0`, and asserts that exactly 2 packages are returned, each with either `MIT` or `Apache-2.0` license.

The implementation correctly handles comma-separated license values and returns the union of matching packages.
