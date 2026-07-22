# Criterion 2: `GET /api/v2/package?license=MIT,Apache-2.0` returns packages with either license

## Verdict: PASS

## Analysis

### Code Changes

The `validate_license_param` function in `modules/fundamental/src/package/endpoints/list.rs` handles comma-separated values by splitting the input string on commas:

```rust
let identifiers: Vec<String> = license.split(',').map(|s| s.trim().to_string()).collect();
```

Each identifier is individually validated via `Expression::parse(id)`, so both `MIT` and `Apache-2.0` must be valid SPDX expressions for the request to succeed.

In the service layer (`modules/fundamental/src/package/service/mod.rs`), the filter uses:

```rust
Condition::any()
    .add(package_license::Column::License.is_in(licenses.iter().cloned()))
```

`Condition::any()` in SeaORM generates an OR condition, and `is_in` generates a SQL `IN` clause. Together, this produces a query like `WHERE package_license.license IN ('MIT', 'Apache-2.0')`, which returns packages matching either license. The `InnerJoin` on `PackageLicense` ensures only packages with a matching license record are included.

### Test Coverage

The test `test_list_packages_multi_license_filter` in `tests/api/package.rs` validates this criterion:
- Seeds three packages: `pkg-a` (MIT), `pkg-b` (Apache-2.0), `pkg-c` (GPL-3.0-only)
- Sends `GET /api/v2/package?license=MIT,Apache-2.0`
- Asserts response status is 200 OK
- Asserts exactly 2 items returned (MIT and Apache-2.0, excluding GPL-3.0-only)
- Asserts all returned items have either `license == "MIT"` or `license == "Apache-2.0"`

This confirms the union semantics: packages matching any of the provided licenses are included, and non-matching packages are excluded.

### Conclusion

The comma-separated parsing, per-identifier SPDX validation, and OR-based database filter correctly implement the union behavior. The test directly validates that multiple license values return the union of matching packages.
