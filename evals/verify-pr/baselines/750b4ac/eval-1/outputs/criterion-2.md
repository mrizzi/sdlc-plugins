# Criterion 2: `GET /api/v2/package?license=MIT,Apache-2.0` returns packages with either license

## Verdict: PASS

## Analysis

### What was checked

This criterion requires that comma-separated license values produce a union (OR) filter, returning packages matching any of the specified licenses.

### Evidence from the diff

1. **Comma splitting** (`modules/fundamental/src/package/endpoints/list.rs`):
   - `validate_license_param` splits on commas: `license.split(',').map(|s| s.trim().to_string()).collect()`. For input `MIT,Apache-2.0`, this produces `["MIT", "Apache-2.0"]`.
   - Each identifier is validated individually via `Expression::parse(id)`.

2. **OR filter in service layer** (`modules/fundamental/src/package/service/mod.rs`):
   - The filter uses `Condition::any()` (SeaORM's OR condition) with `.add(package_license::Column::License.is_in(licenses.iter().cloned()))`.
   - `is_in` generates a SQL `IN ('MIT', 'Apache-2.0')` clause, which inherently returns rows matching any of the listed values.

3. **Test coverage** (`tests/api/package.rs`):
   - `test_list_packages_multi_license_filter` seeds three packages (MIT, Apache-2.0, GPL-3.0-only), queries `?license=MIT,Apache-2.0`, and asserts:
     - Response status is 200 OK
     - Exactly 2 items returned (MIT and Apache-2.0, not GPL-3.0-only)
     - All items have license equal to either "MIT" or "Apache-2.0"

### Conclusion

The implementation correctly handles comma-separated license identifiers by splitting, validating each one, and applying an IN clause via SeaORM's `Condition::any()`. The test confirms the union behavior and that non-matching licenses are excluded.
