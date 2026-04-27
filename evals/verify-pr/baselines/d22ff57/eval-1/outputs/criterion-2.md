## Criterion 2

**Text:** `GET /api/v2/package?license=MIT,Apache-2.0` returns packages with either license

### Evidence

1. **Comma splitting** (`modules/fundamental/src/package/endpoints/list.rs`): `validate_license_param` splits the input on commas: `license.split(',').map(|s| s.trim().to_string())`. For `MIT,Apache-2.0`, this produces `["MIT", "Apache-2.0"]`.

2. **Each identifier is validated** individually via `Expression::parse(id)`, so both `MIT` and `Apache-2.0` pass validation.

3. **OR semantics in the query** (`modules/fundamental/src/package/service/mod.rs`): The filter uses `Condition::any()` combined with `.is_in(licenses.iter().cloned())`. The `is_in` clause generates a SQL `WHERE license IN ('MIT', 'Apache-2.0')`, which returns the union of packages matching either license.

4. **Test coverage** (`tests/api/package.rs`): `test_list_packages_multi_license_filter` seeds packages with MIT, Apache-2.0, and GPL-3.0-only licenses, queries `?license=MIT,Apache-2.0`, and asserts:
   - Response status is 200 OK
   - Exactly 2 items returned (MIT and Apache-2.0, excluding GPL-3.0-only)
   - All items have license equal to `"MIT"` or `"Apache-2.0"`

### Verdict: PASS
