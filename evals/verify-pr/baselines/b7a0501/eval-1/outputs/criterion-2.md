## Criterion 2: `GET /api/v2/package?license=MIT,Apache-2.0` returns packages with either license

**Result: PASS**

**Evidence from diff:**

1. **Comma splitting** (`modules/fundamental/src/package/endpoints/list.rs`): The `validate_license_param` function splits the license string by comma: `license.split(',').map(|s| s.trim().to_string()).collect()`. For input `MIT,Apache-2.0`, this produces `["MIT", "Apache-2.0"]`.

2. **Validation**: Each identifier is individually validated via `Expression::parse(id)`, so both `MIT` and `Apache-2.0` are checked as valid SPDX identifiers.

3. **OR-style filtering** (`modules/fundamental/src/package/service/mod.rs`): The filter uses `Condition::any()` with `is_in(licenses.iter().cloned())`, which generates a SQL `WHERE license IN ('MIT', 'Apache-2.0')` clause. This correctly implements union semantics -- packages matching either license are returned.

4. **Test coverage** (`tests/api/package.rs`): The test `test_list_packages_multi_license_filter` seeds packages with MIT, Apache-2.0, and GPL-3.0-only licenses, queries `?license=MIT,Apache-2.0`, and asserts that exactly 2 packages are returned, each having either MIT or Apache-2.0 as the license.

The comma-separated multi-license filter is fully implemented with correct union/OR semantics.
