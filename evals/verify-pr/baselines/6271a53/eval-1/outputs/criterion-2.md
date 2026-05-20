# Criterion 2: `GET /api/v2/package?license=MIT,Apache-2.0` returns packages with either license

## Verdict: PASS

## Analysis

**What was checked:**
This criterion requires that comma-separated license values return the union of packages matching any of the specified licenses.

**Evidence from the diff:**

1. **Comma splitting (list.rs):** The `validate_license_param` function splits the input on commas and trims whitespace:
   ```rust
   let identifiers: Vec<String> = license.split(',').map(|s| s.trim().to_string()).collect();
   ```
   For input `MIT,Apache-2.0`, this produces `["MIT", "Apache-2.0"]`.

2. **Individual validation (list.rs):** Each identifier in the resulting vector is validated independently against `Expression::parse(id)`. Both `MIT` and `Apache-2.0` are valid SPDX identifiers, so validation passes.

3. **OR-based filtering (service/mod.rs):** The filter uses `Condition::any()` with `is_in`:
   ```rust
   Condition::any()
       .add(package_license::Column::License.is_in(licenses.iter().cloned()))
   ```
   `Condition::any()` combined with `is_in` produces a SQL `WHERE license IN ('MIT', 'Apache-2.0')` clause, which correctly returns the union of packages matching either license.

4. **Test coverage (tests/api/package.rs):** The test `test_list_packages_multi_license_filter` seeds three packages (MIT, Apache-2.0, GPL-3.0-only), requests `?license=MIT,Apache-2.0`, and asserts:
   - Response status is 200 OK
   - Exactly 2 items are returned
   - All returned items have license equal to either `MIT` or `Apache-2.0`

**Conclusion:** The implementation correctly handles comma-separated license values by splitting, validating each independently, and applying an `IN` clause via SeaORM's `Condition::any()`. The integration test verifies union semantics. This criterion is satisfied.
