# Criterion 2: `GET /api/v2/package?license=MIT,Apache-2.0` returns packages with either license

## Verdict: PASS

## Reasoning

The PR implements comma-separated multi-license filtering through the validation and query layers:

**Parsing and validation (`modules/fundamental/src/package/endpoints/list.rs`):**
- `validate_license_param` splits the `license` string on commas: `license.split(',').map(|s| s.trim().to_string()).collect()`. For input `"MIT,Apache-2.0"`, this produces `["MIT", "Apache-2.0"]`.
- Each identifier is individually validated via `spdx::Expression::parse()`, ensuring both `MIT` and `Apache-2.0` are valid SPDX identifiers.
- The resulting `Vec<String>` with two elements is passed to the service layer.

**Query construction (`modules/fundamental/src/package/service/mod.rs`):**
- The filter uses `Condition::any().add(package_license::Column::License.is_in(licenses.iter().cloned()))`.
- `Condition::any()` creates an OR condition, and `is_in` generates a SQL `IN ('MIT', 'Apache-2.0')` clause.
- Combined with the `InnerJoin` to `PackageLicense`, this returns packages whose license is in the provided set -- i.e., a union of matches.

**Test verification (`tests/api/package.rs`):**
- `test_list_packages_multi_license_filter` seeds three packages (MIT, Apache-2.0, GPL-3.0-only), queries `?license=MIT,Apache-2.0`, and asserts that exactly 2 packages are returned, each having either `MIT` or `Apache-2.0` license.

The implementation correctly returns the union of packages matching any of the comma-separated license identifiers.
