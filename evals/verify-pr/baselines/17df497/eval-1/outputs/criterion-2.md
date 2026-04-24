## Criterion 2: `GET /api/v2/package?license=MIT,Apache-2.0` returns packages with either license

### Result: PASS

### Reasoning

**Endpoint layer (`list.rs`):**
The `validate_license_param` function splits the license string on commas: `license.split(',').map(|s| s.trim().to_string()).collect()`. For `MIT,Apache-2.0`, this produces `["MIT", "Apache-2.0"]`. Each identifier is validated individually via `Expression::parse(id)`, and both `MIT` and `Apache-2.0` are valid SPDX identifiers, so validation passes. The resulting vector is forwarded to the service layer.

**Service layer (`service/mod.rs`):**
The filter uses `Condition::any()` with `package_license::Column::License.is_in(licenses.iter().cloned())`. The `is_in` clause generates SQL equivalent to `WHERE license IN ('MIT', 'Apache-2.0')`, which is a union/OR semantic -- any package matching either license is included. The `Condition::any()` wrapper is also consistent with OR semantics.

The `InnerJoin` on `PackageLicense` ensures only packages with at least one matching license record are returned. This correctly implements the "union of matching packages" behavior described in the criterion.

**Test coverage:**
The test `test_list_packages_multi_license_filter` seeds three packages (MIT, Apache-2.0, GPL-3.0-only), requests `?license=MIT,Apache-2.0`, and asserts:
- Status is 200 OK
- Exactly 2 items returned (MIT and Apache-2.0; GPL-3.0-only is excluded)
- All returned items have a license that is either `MIT` or `Apache-2.0`

This directly validates the criterion.
