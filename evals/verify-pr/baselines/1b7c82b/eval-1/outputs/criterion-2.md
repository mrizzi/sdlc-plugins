## Criterion 2: `GET /api/v2/package?license=MIT,Apache-2.0` returns packages with either license

### Verdict: PASS

### Analysis

**What the criterion requires:**
The endpoint must support comma-separated license values and return the union of packages matching any of the specified licenses.

**Evidence from the PR diff:**

1. **Comma splitting (`list.rs`):**
   The `validate_license_param` function performs `license.split(',').map(|s| s.trim().to_string()).collect()`. For the input `MIT,Apache-2.0`, this produces `vec!["MIT", "Apache-2.0"]`. Each identifier is individually validated via `spdx::Expression::parse`. Both `MIT` and `Apache-2.0` are valid SPDX identifiers, so validation succeeds.

2. **OR-based filtering (`service/mod.rs`):**
   The filter uses `Condition::any()` with `is_in(licenses.iter().cloned())`. The `Condition::any()` creates an OR condition, and `is_in` generates a SQL `IN ('MIT', 'Apache-2.0')` clause. This returns packages whose license is either MIT or Apache-2.0 -- a union of matching packages.

3. **Test coverage (`tests/api/package.rs`):**
   The `test_list_packages_multi_license_filter` test seeds three packages with MIT, Apache-2.0, and GPL-3.0-only licenses. It queries `?license=MIT,Apache-2.0` and asserts:
   - Status is `OK`
   - Exactly 2 items are returned
   - All returned items have license equal to either `MIT` or `Apache-2.0`

   This directly validates the union behavior.

**Conclusion:**
The comma-separated parsing, SPDX validation of each identifier, and OR-based SQL filtering correctly implement the union semantics. The test confirms the expected behavior. The criterion is satisfied.
