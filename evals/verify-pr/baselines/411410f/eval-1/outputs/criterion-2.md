## Criterion 2: `GET /api/v2/package?license=MIT,Apache-2.0` returns packages with either license

### Verdict: PASS

### Reasoning

The PR implements comma-separated multi-license filtering through the same code path as single-license filtering, with the comma-split logic naturally handling multiple values:

1. **Endpoint layer** (`modules/fundamental/src/package/endpoints/list.rs`): The `validate_license_param` function splits the license string on commas: `license.split(',').map(|s| s.trim().to_string()).collect()`. For input `"MIT,Apache-2.0"`, this produces `vec!["MIT", "Apache-2.0"]`. Each identifier is individually validated against the SPDX expression parser.

2. **Service layer** (`modules/fundamental/src/package/service/mod.rs`): The `is_in(licenses.iter().cloned())` filter generates a SQL `WHERE license IN ('MIT', 'Apache-2.0')` clause. Combined with `Condition::any()`, this returns packages matching either license (union semantics), which is the correct behavior for an `IN` clause.

3. **Test coverage** (`tests/api/package.rs`): The `test_list_packages_multi_license_filter` test seeds three packages (MIT, Apache-2.0, GPL-3.0-only), requests `?license=MIT,Apache-2.0`, and asserts:
   - Response status is 200 OK
   - Result contains exactly 2 items (MIT and Apache-2.0, excluding GPL-3.0-only)
   - All items have license matching either `"MIT"` or `"Apache-2.0"`

   This directly validates the criterion for union semantics with comma-separated values.

### Evidence

- `list.rs`: `license.split(',').map(|s| s.trim().to_string()).collect()` handles comma separation
- `mod.rs`: `Condition::any().add(package_license::Column::License.is_in(...))` implements OR/union semantics via SQL IN
- `package.rs` test: `test_list_packages_multi_license_filter` tests comma-separated `MIT,Apache-2.0` and asserts union behavior
