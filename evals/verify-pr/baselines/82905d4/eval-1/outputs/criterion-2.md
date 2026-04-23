# Criterion 2: `GET /api/v2/package?license=MIT,Apache-2.0` returns packages with either license

## Result: PASS

## Analysis

### 1. Comma-separated parsing

The `validate_license_param` function in `list.rs` splits the input on commas:

```rust
let identifiers: Vec<String> = license.split(',').map(|s| s.trim().to_string()).collect();
```

For `license=MIT,Apache-2.0`, this produces `vec!["MIT", "Apache-2.0"]`. Each identifier is individually validated against `spdx::Expression::parse`.

### 2. OR-based filtering

In the service layer (`mod.rs`), the filter uses `Condition::any()`:

```rust
Condition::any()
    .add(package_license::Column::License.is_in(licenses.iter().cloned()))
```

`Condition::any()` produces an OR condition in SeaORM. Combined with `is_in`, this generates a SQL clause like `WHERE package_license.license IN ('MIT', 'Apache-2.0')`, which returns packages matching either license -- the union semantics required by the criterion.

### 3. Test coverage

The test `test_list_packages_multi_license_filter` seeds three packages (MIT, Apache-2.0, GPL-3.0-only), filters by `MIT,Apache-2.0`, and asserts:
- Exactly 2 packages are returned
- Each returned package has either MIT or Apache-2.0 as its license

## Conclusion

The implementation correctly handles comma-separated license values by splitting, validating each, and using an `IS IN` clause with OR semantics. The test confirms union behavior.
