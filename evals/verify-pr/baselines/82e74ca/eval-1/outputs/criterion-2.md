# Criterion 2: `GET /api/v2/package?license=MIT,Apache-2.0` returns packages with either license

## Result: PASS

## Analysis

### Code Evidence

**Comma-separated parsing** (`modules/fundamental/src/package/endpoints/list.rs`):

The `validate_license_param` function splits the license parameter on commas and trims whitespace:

```rust
let identifiers: Vec<String> = license.split(',').map(|s| s.trim().to_string()).collect();
```

For `license=MIT,Apache-2.0`, this produces `["MIT", "Apache-2.0"]`. Each identifier is individually validated as a valid SPDX expression.

**Union filtering** (`modules/fundamental/src/package/service/mod.rs`):

The service layer uses `Condition::any()` combined with `is_in()`:

```rust
query = query.filter(
    Condition::any()
        .add(package_license::Column::License.is_in(licenses.iter().cloned()))
);
```

`Condition::any()` produces an OR condition, and `is_in()` generates a SQL `IN` clause. For `["MIT", "Apache-2.0"]`, this produces `WHERE package_license.license IN ('MIT', 'Apache-2.0')`, which returns packages with either license -- a union of matching packages.

### Test Evidence

The test `test_list_packages_multi_license_filter` in `tests/api/package.rs` seeds three packages (MIT, Apache-2.0, GPL-3.0-only), filters by `?license=MIT,Apache-2.0`, and asserts:
- Status is 200 OK
- 2 items returned (MIT and Apache-2.0, not GPL-3.0-only)
- All returned items have license matching either "MIT" or "Apache-2.0"

### Conclusion

The implementation correctly parses comma-separated license values, validates each individually, and uses an `IN` clause to return the union of packages matching any of the specified licenses. This criterion is satisfied.
