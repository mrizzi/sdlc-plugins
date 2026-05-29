## Criterion 2

**Text**: `GET /api/v2/package?license=MIT,Apache-2.0` returns packages with either license

### What was checked

Examined the comma-separation parsing logic, the database filter construction for multiple values, and the corresponding test.

### Code evidence

1. **Comma splitting** (`modules/fundamental/src/package/endpoints/list.rs`): `validate_license_param` splits the input on `,` and trims each entry:
   ```rust
   let identifiers: Vec<String> = license.split(',').map(|s| s.trim().to_string()).collect();
   ```
   For `MIT,Apache-2.0`, this produces `["MIT", "Apache-2.0"]`. Each is individually validated via `Expression::parse()`.

2. **OR-based filtering** (`modules/fundamental/src/package/service/mod.rs`): The filter uses `Condition::any()` with `is_in(licenses.iter().cloned())`, which generates `WHERE license IN ('MIT', 'Apache-2.0')`. This returns the union of packages matching either license.

3. **Test coverage** (`tests/api/package.rs`): `test_list_packages_multi_license_filter` seeds three packages (MIT, Apache-2.0, GPL-3.0-only), queries `?license=MIT,Apache-2.0`, and asserts:
   - Status is 200 OK
   - Exactly 2 items returned
   - All items have license equal to either `MIT` or `Apache-2.0`

### Verdict: PASS

The comma-separated license parameter is correctly split, each value is independently validated, and the `is_in` clause produces a union query. The test confirms that only packages matching either license are returned, excluding the GPL-3.0-only package.
