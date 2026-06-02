## Criterion 2: `GET /api/v2/package?license=MIT,Apache-2.0` returns packages with either license

**Verdict: PASS**

### Analysis

The implementation satisfies this criterion through the following code path:

1. **Comma-separated parsing:** The `validate_license_param()` function in `list.rs` splits the license string by commas: `license.split(',').map(|s| s.trim().to_string()).collect()`. For `"MIT,Apache-2.0"`, this produces `["MIT", "Apache-2.0"]`. Each identifier is individually validated via `Expression::parse()`, and both are valid SPDX identifiers.

2. **OR-based filtering:** In `service/mod.rs`, the filter uses `Condition::any()` with `is_in(licenses.iter().cloned())`. The `is_in` clause generates SQL equivalent to `WHERE license IN ('MIT', 'Apache-2.0')`, which returns packages matching **either** license. The use of `Condition::any()` (OR semantics) is correct for union-style filtering.

3. **InnerJoin on license table:** The `InnerJoin` on `package::Relation::PackageLicense` ensures the filter operates on the license relationship, returning packages that have at least one of the specified licenses in the `package_license` table.

4. **Test coverage:** The test `test_list_packages_multi_license_filter` seeds packages with MIT, Apache-2.0, and GPL-3.0-only licenses, filters by `?license=MIT,Apache-2.0`, and asserts:
   - Response status is 200 OK
   - 2 packages are returned (MIT and Apache-2.0, not GPL-3.0-only)
   - All returned packages have `license == "MIT"` or `license == "Apache-2.0"`

### Evidence

- `list.rs`: `license.split(',').map(|s| s.trim().to_string()).collect()` correctly parses comma-separated values
- `service/mod.rs`: `Condition::any().add(package_license::Column::License.is_in(licenses.iter().cloned()))` applies OR-based filtering
- `tests/api/package.rs`: `test_list_packages_multi_license_filter` covers the comma-separated scenario with union semantics
