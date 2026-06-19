## Criterion 2: `GET /api/v2/package?license=MIT,Apache-2.0` returns packages with either license

### Verdict: PASS

### Analysis

This criterion requires that comma-separated license values produce a union filter (OR semantics), returning packages that match any of the specified licenses.

### Evidence

**1. Comma splitting (list.rs):**
The `validate_license_param` function splits the input on commas:
```rust
let identifiers: Vec<String> = license.split(',').map(|s| s.trim().to_string()).collect();
```
For `?license=MIT,Apache-2.0`, this produces `vec!["MIT", "Apache-2.0"]`. Each identifier is validated individually against the SPDX parser.

**2. OR condition in query (service/mod.rs):**
The filter uses `Condition::any()` which produces SQL OR semantics:
```rust
query = query.filter(
    Condition::any()
        .add(package_license::Column::License.is_in(licenses.iter().cloned()))
);
```
`Condition::any()` combined with `is_in` produces `WHERE package_license.license IN ('MIT', 'Apache-2.0')`, which returns packages matching either license. This is correct union/OR semantics.

**3. Test coverage (tests/api/package.rs):**
`test_list_packages_multi_license_filter` seeds three packages (MIT, Apache-2.0, GPL-3.0-only), queries with `?license=MIT,Apache-2.0`, and asserts:
- Response status is 200 OK
- Result contains exactly 2 items (MIT and Apache-2.0, not GPL-3.0-only)
- All returned items have license equal to either "MIT" or "Apache-2.0"

### Conclusion

The comma-separated parsing, SPDX validation of each identifier, and `Condition::any()` with `is_in` correctly implement union semantics. The test validates the expected behavior with three distinct licenses. Criterion is satisfied.
