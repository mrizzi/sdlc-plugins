# Criterion 2: `GET /api/v2/package?license=MIT,Apache-2.0` returns packages with either license

## Verdict: PASS

## Analysis

The PR diff demonstrates that comma-separated license filtering is correctly implemented and tested.

### Implementation Evidence

**Endpoint layer** (`modules/fundamental/src/package/endpoints/list.rs`):
- The `validate_license_param()` function splits the `license` parameter on commas: `license.split(',').map(|s| s.trim().to_string()).collect()`.
- Each identifier is validated individually via `spdx::Expression::parse()`.
- The function returns a `Vec<String>` of all validated identifiers (e.g., `["MIT", "Apache-2.0"]`).

**Service layer** (`modules/fundamental/src/package/service/mod.rs`):
- The filter uses `Condition::any()` combined with `is_in(licenses.iter().cloned())`.
- `Condition::any()` produces an OR condition, meaning packages matching ANY of the provided license identifiers will be included.
- The `is_in` clause generates `WHERE license IN ('MIT', 'Apache-2.0')`, which is semantically a union/OR operation.
- The inner join to `PackageLicense` ensures only packages with a matching license record are returned.

### Test Evidence

The test `test_list_packages_multi_license_filter` in `tests/api/package.rs`:
- Seeds three packages: `pkg-a` (MIT), `pkg-b` (Apache-2.0), `pkg-c` (GPL-3.0-only)
- Requests `GET /api/v2/package?license=MIT,Apache-2.0`
- Asserts HTTP 200 status
- Asserts exactly 2 items returned (excluding the GPL-3.0-only package)
- Asserts all returned items have `license == "MIT" || license == "Apache-2.0"`

This directly validates the union behavior for comma-separated licenses.

### Conclusion

The comma-splitting in `validate_license_param`, the `Condition::any()` + `is_in` filter in the service layer, and the integration test all confirm that multiple comma-separated license values return the union of matching packages.
