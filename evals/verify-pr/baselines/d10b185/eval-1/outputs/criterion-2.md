## Criterion 2: `GET /api/v2/package?license=MIT,Apache-2.0` returns packages with either license

### Verdict: PASS

### Evidence

The PR implements multi-license (comma-separated) filtering through the same code path as single-license, with the comma-split logic handling multiple values:

1. **Comma splitting** (`modules/fundamental/src/package/endpoints/list.rs` -- `validate_license_param`):
   The function splits the input on commas: `license.split(',').map(|s| s.trim().to_string()).collect()`. For input `MIT,Apache-2.0`, this produces `["MIT", "Apache-2.0"]`. Each identifier is individually validated via `spdx::Expression::parse`.

2. **OR-based filter** (`modules/fundamental/src/package/service/mod.rs`):
   The service uses `Condition::any()` with `is_in(licenses.iter().cloned())`, which generates a SQL `WHERE package_license.license IN ('MIT', 'Apache-2.0')` clause. The `Condition::any()` combined with `is_in` correctly implements union semantics -- packages matching ANY of the provided licenses are returned.

3. **Test coverage** (`tests/api/package.rs` -- `test_list_packages_multi_license_filter`):
   The test seeds three packages (MIT, Apache-2.0, GPL-3.0-only), requests `?license=MIT,Apache-2.0`, and asserts:
   - Response status is 200 OK
   - Exactly 2 items returned (MIT and Apache-2.0, excluding GPL-3.0-only)
   - All items have license equal to either "MIT" or "Apache-2.0"

### Conclusion

The comma-separated input is correctly split, each identifier is individually validated, and the resulting list is passed to the service layer where `is_in` with `Condition::any()` implements the union (OR) semantics. The integration test confirms that packages with either license are returned while packages with other licenses are excluded. This criterion is satisfied.
