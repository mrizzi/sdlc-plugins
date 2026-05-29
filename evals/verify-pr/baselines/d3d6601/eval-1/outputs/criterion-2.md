# Criterion 2: `GET /api/v2/package?license=MIT,Apache-2.0` returns packages with either license

## Verdict: PASS

## Reasoning

### What was checked

This criterion requires that comma-separated license values are supported and return the union of matching packages (i.e., packages with either MIT or Apache-2.0 licenses).

### Evidence from the diff

**1. Comma splitting (`list.rs`):**
The `validate_license_param` function splits the input on commas: `license.split(',').map(|s| s.trim().to_string()).collect()`. For `MIT,Apache-2.0`, this produces `["MIT", "Apache-2.0"]`. Each identifier is validated individually via `Expression::parse(id)`.

**2. OR-based filtering (`service/mod.rs`):**
The filter uses `Condition::any()` with `.add(package_license::Column::License.is_in(licenses.iter().cloned()))`. The `is_in` clause combined with `Condition::any()` produces a SQL `WHERE license IN ('MIT', 'Apache-2.0')`, which correctly returns the union of packages matching either license.

**3. Test coverage (`tests/api/package.rs`):**
The test `test_list_packages_multi_license_filter` seeds three packages (MIT, Apache-2.0, GPL-3.0-only), requests `?license=MIT,Apache-2.0`, and asserts:
- Response status is 200 OK
- Result contains exactly 2 items (MIT and Apache-2.0, excluding GPL-3.0-only)
- All items have license equal to either "MIT" or "Apache-2.0"

### Conclusion

The implementation correctly parses comma-separated values, validates each one, and applies an inclusive (OR-based) filter. The test confirms that the union semantics work as expected, returning packages matching any of the specified licenses while excluding others.
