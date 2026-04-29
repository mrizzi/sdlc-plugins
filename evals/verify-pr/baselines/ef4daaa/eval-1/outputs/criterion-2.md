# Criterion 2: `GET /api/v2/package?license=MIT,Apache-2.0` returns packages with either license

## Verdict: PASS

## Reasoning

The `validate_license_param` function in `list.rs` splits the comma-separated `license` parameter:

```rust
let identifiers: Vec<String> = license.split(',').map(|s| s.trim().to_string()).collect();
```

This produces `["MIT", "Apache-2.0"]` for the input `MIT,Apache-2.0`. Each identifier is validated against SPDX expressions. The resulting vector is passed to `PackageService::list()`.

In `service/mod.rs`, the filter uses `Condition::any()` with `is_in(licenses.iter().cloned())`:

```rust
query = query.filter(
    Condition::any()
        .add(package_license::Column::License.is_in(licenses.iter().cloned()))
);
```

The `is_in` clause with `Condition::any()` produces a SQL `WHERE license IN ('MIT', 'Apache-2.0')` query, which returns the union of packages matching either license. This is correct OR semantics.

The integration test `test_list_packages_multi_license_filter` seeds three packages (MIT, Apache-2.0, GPL-3.0-only), queries with `?license=MIT,Apache-2.0`, and asserts:
- Response status is 200 OK
- Exactly 2 items returned (MIT and Apache-2.0, excluding GPL-3.0-only)
- All items have `license == "MIT" || license == "Apache-2.0"`

The implementation correctly handles comma-separated license values and returns the union of matching packages.
