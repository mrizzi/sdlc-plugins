# Criterion 2: `GET /api/v2/package?license=MIT,Apache-2.0` returns packages with either license

## Verdict: PASS

## Reasoning

The PR diff demonstrates that multi-license (comma-separated) filtering is correctly implemented and tested.

### Implementation Evidence

1. **Comma parsing** (`modules/fundamental/src/package/endpoints/list.rs`):
   - The `validate_license_param` function splits the license string on commas: `license.split(',').map(|s| s.trim().to_string()).collect()`.
   - For input `"MIT,Apache-2.0"`, this produces `vec!["MIT", "Apache-2.0"]`.
   - Each identifier is individually validated against `spdx::Expression::parse()`. Both "MIT" and "Apache-2.0" are valid SPDX identifiers.

2. **OR-based filtering** (`modules/fundamental/src/package/service/mod.rs`):
   - The service uses `Condition::any()` combined with `package_license::Column::License.is_in(licenses.iter().cloned())`.
   - `Condition::any()` produces an OR condition, meaning a package matches if its license is in the provided set.
   - `is_in` generates a SQL `IN ('MIT', 'Apache-2.0')` clause, which returns packages matching either license.

3. **Union semantics**: The combination of `Condition::any()` and `is_in` correctly implements union semantics -- packages with MIT OR Apache-2.0 license are returned, which matches the criterion's "returns packages with either license" requirement.

### Test Evidence

The test `test_list_packages_multi_license_filter` in `tests/api/package.rs`:
- Seeds packages with MIT, Apache-2.0, and GPL-3.0-only licenses.
- Requests `GET /api/v2/package?license=MIT,Apache-2.0`.
- Asserts the response status is 200 OK.
- Asserts exactly 2 items are returned (the MIT and Apache-2.0 packages, excluding GPL-3.0-only).
- Asserts all returned packages have either `license == "MIT"` or `license == "Apache-2.0"`.

This test directly validates the union/either-license behavior specified by the criterion.
