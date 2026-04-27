# Criterion 2: `GET /api/v2/package?license=MIT,Apache-2.0` returns packages with either license

## Verdict: PASS

## Analysis

The PR implements comma-separated license filtering through the following mechanism:

### Parsing and validation (`modules/fundamental/src/package/endpoints/list.rs`)

1. **Splitting:** The `validate_license_param` function splits the license parameter by commas: `license.split(',').map(|s| s.trim().to_string()).collect()`. For `?license=MIT,Apache-2.0`, this produces `["MIT", "Apache-2.0"]`.

2. **Individual validation:** Each identifier is validated independently via `Expression::parse(id)`. Both `MIT` and `Apache-2.0` are valid SPDX identifiers, so validation succeeds and the function returns `Ok(vec!["MIT".to_string(), "Apache-2.0".to_string()])`.

### Filtering (`modules/fundamental/src/package/service/mod.rs`)

3. **OR semantics:** The service uses `Condition::any()` with `is_in()`:
   ```rust
   Condition::any()
       .add(package_license::Column::License.is_in(licenses.iter().cloned()))
   ```
   `Condition::any()` produces an OR condition, and `is_in` generates a SQL `IN` clause. The resulting SQL is equivalent to `WHERE package_license.license IN ('MIT', 'Apache-2.0')`. This correctly implements union semantics -- packages with either license are included.

4. **Join:** The INNER JOIN on `package::Relation::PackageLicense` ensures only packages that have a matching license record are returned.

### Test coverage

The `test_list_packages_multi_license_filter` test verifies this:
- Seeds three packages: MIT, Apache-2.0, and GPL-3.0-only
- Queries `?license=MIT,Apache-2.0`
- Asserts 200 OK response
- Asserts exactly 2 items returned
- Asserts all items have license equal to either `MIT` or `Apache-2.0`

## Conclusion

The comma-separated license parameter is correctly split, individually validated, and used in an `IN` clause with OR semantics. The test confirms that only packages matching any of the specified licenses are returned, which is the expected union behavior.
