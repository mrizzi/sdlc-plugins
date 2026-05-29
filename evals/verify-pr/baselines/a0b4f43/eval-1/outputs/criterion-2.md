## Criterion 2: `GET /api/v2/package?license=MIT,Apache-2.0` returns packages with either license

**Verdict: PASS**

### Reasoning

The comma-separated license filtering is handled through the following code path:

**Parsing (`modules/fundamental/src/package/endpoints/list.rs`):**
- The `validate_license_param` function splits the input on commas: `license.split(',').map(|s| s.trim().to_string()).collect()`. For `license=MIT,Apache-2.0`, this produces `["MIT", "Apache-2.0"]`.
- Each identifier is individually validated via `spdx::Expression::parse()`, so both `MIT` and `Apache-2.0` are checked as valid SPDX identifiers.

**Filtering (`modules/fundamental/src/package/service/mod.rs`):**
- The service layer uses `Condition::any()` with `.is_in(licenses.iter().cloned())`. The `is_in` operator generates a SQL `WHERE license IN ('MIT', 'Apache-2.0')` clause, which returns packages matching **either** license -- this is the correct union semantics.

**Test verification (`tests/api/package.rs`):**
- The `test_list_packages_multi_license_filter` test seeds three packages with `MIT`, `Apache-2.0`, and `GPL-3.0-only` licenses, queries `?license=MIT,Apache-2.0`, and asserts:
  - The response status is 200 OK
  - Exactly 2 items are returned (MIT and Apache-2.0, but not GPL-3.0-only)
  - All returned items have license equal to either `MIT` or `Apache-2.0`

The implementation correctly returns the union of packages matching any of the comma-separated license values.
