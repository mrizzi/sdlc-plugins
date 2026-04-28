## Criterion 2: `GET /api/v2/package?license=MIT,Apache-2.0` returns packages with either license

### Result: PASS

### Reasoning

**Endpoint layer (`modules/fundamental/src/package/endpoints/list.rs`):**
The `validate_license_param` function handles comma-separated values by splitting on commas: `license.split(',').map(|s| s.trim().to_string()).collect()`. For the input `MIT,Apache-2.0`, this produces the vector `["MIT", "Apache-2.0"]`. Each identifier is individually validated via `Expression::parse(id)`. Both `MIT` and `Apache-2.0` are valid SPDX identifiers, so the validation passes and the full vector is forwarded to the service layer as `Some(&["MIT", "Apache-2.0"])`.

**Service layer (`modules/fundamental/src/package/service/mod.rs`):**
The filter applies `Condition::any()` with `package_license::Column::License.is_in(licenses.iter().cloned())`. The `is_in` method generates SQL equivalent to `WHERE license IN ('MIT', 'Apache-2.0')`, which implements union/OR semantics -- a package is included if its license matches any of the provided values. The `Condition::any()` wrapper is consistent with OR semantics, and the `InnerJoin` on `PackageLicense` ensures only packages with at least one matching license record are returned.

This correctly implements the "returns packages with either license" requirement from the criterion.

**Test coverage:**
The integration test `test_list_packages_multi_license_filter` in `tests/api/package.rs` validates this criterion:
- Seeds 3 packages: `pkg-a` (MIT), `pkg-b` (Apache-2.0), `pkg-c` (GPL-3.0-only)
- Requests `GET /api/v2/package?license=MIT,Apache-2.0`
- Asserts HTTP 200 status
- Asserts exactly 2 items returned (MIT and Apache-2.0; GPL-3.0-only is excluded)
- Asserts all returned items have a license that is either `MIT` or `Apache-2.0`

This directly confirms the union semantics work correctly with multiple comma-separated license values.
