## Criterion 2: `GET /api/v2/package?license=MIT,Apache-2.0` returns packages with either license

### Result: PASS

### Reasoning

**Endpoint layer (`modules/fundamental/src/package/endpoints/list.rs`):**
The `validate_license_param` function handles comma-separated values by splitting the input string: `license.split(',').map(|s| s.trim().to_string()).collect()`. For the input `MIT,Apache-2.0`, this produces the vector `["MIT", "Apache-2.0"]`. Each identifier is validated individually through `Expression::parse(id)` -- both `MIT` and `Apache-2.0` are valid SPDX license identifiers, so validation passes successfully. The resulting two-element vector is forwarded to `PackageService::list()`.

**Service layer (`modules/fundamental/src/package/service/mod.rs`):**
The filter clause uses `Condition::any().add(package_license::Column::License.is_in(licenses.iter().cloned()))`. The `is_in` method generates SQL equivalent to `WHERE license IN ('MIT', 'Apache-2.0')`, which implements union (OR) semantics -- any package with a license matching either value is included. The `Condition::any()` wrapper is consistent with OR semantics, though `is_in` alone would suffice for this case.

The `InnerJoin` on `PackageLicense` ensures only packages with at least one matching license record are returned, correctly implementing the "packages with either license" behavior.

**Test validation:**
The integration test `test_list_packages_multi_license_filter` in `tests/api/package.rs` validates this criterion:
- Seeds 3 packages: `pkg-a` (MIT), `pkg-b` (Apache-2.0), `pkg-c` (GPL-3.0-only)
- Sends `GET /api/v2/package?license=MIT,Apache-2.0`
- Asserts response status is 200 OK
- Asserts exactly 2 items returned (MIT and Apache-2.0; GPL-3.0-only excluded)
- Asserts all returned items have `license == "MIT"` or `license == "Apache-2.0"`

This confirms the comma-separated filter correctly returns the union of packages matching either license identifier.
