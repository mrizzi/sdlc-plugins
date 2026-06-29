## Criterion 2: `GET /api/v2/package?license=MIT,Apache-2.0` returns packages with either license

### Verdict: PASS

### Analysis

**Endpoint layer (`modules/fundamental/src/package/endpoints/list.rs`):**

The `validate_license_param` function splits the license parameter on commas:
```rust
let identifiers: Vec<String> = license.split(',').map(|s| s.trim().to_string()).collect();
```

For `license=MIT,Apache-2.0`, this produces `["MIT", "Apache-2.0"]`. Each identifier is individually validated against the SPDX expression parser. Both MIT and Apache-2.0 are valid SPDX identifiers, so validation passes and the vector is forwarded to the service layer.

**Service layer (`modules/fundamental/src/package/service/mod.rs`):**

The filter uses `Condition::any()` with `is_in()`:
```rust
Condition::any()
    .add(package_license::Column::License.is_in(licenses.iter().cloned()))
```

For `["MIT", "Apache-2.0"]`, this generates `WHERE package_license.license IN ('MIT', 'Apache-2.0')`, which is a union/OR semantic -- any package matching either license is included. The `INNER JOIN` on `PackageLicense` ensures only packages with a matching license record are returned.

**Test coverage (`tests/api/package.rs`):**

The test `test_list_packages_multi_license_filter` seeds three packages (MIT, Apache-2.0, GPL-3.0-only), queries `?license=MIT,Apache-2.0`, and asserts:
- Response status is 200 OK
- Exactly 2 items returned (MIT and Apache-2.0 packages; GPL-3.0-only excluded)
- All returned items have `license == "MIT"` or `license == "Apache-2.0"`

This validates the union/OR behavior of comma-separated license filtering.

### Conclusion

The comma-splitting logic in the endpoint layer combined with `is_in()` in the service layer correctly implements union semantics for multiple license values. The integration test confirms the expected behavior. This criterion is satisfied.
