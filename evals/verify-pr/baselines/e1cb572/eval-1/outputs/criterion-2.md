# Criterion 2: GET /api/v2/package?license=MIT,Apache-2.0 returns packages with either license

## Verdict: PASS

## Analysis

The `validate_license_param` function splits the comma-separated `license` parameter into individual identifiers:

```rust
let identifiers: Vec<String> = license.split(',').map(|s| s.trim().to_string()).collect();
```

This produces `["MIT", "Apache-2.0"]` for the input `MIT,Apache-2.0`.

In the service layer, the filter uses `Condition::any()` with `is_in()`:

```rust
Condition::any()
    .add(package_license::Column::License.is_in(licenses.iter().cloned()))
```

`Condition::any()` combined with `is_in` produces a SQL `WHERE license IN ('MIT', 'Apache-2.0')`, which returns the union of packages matching either license. This is semantically an OR operation, matching the requirement for "packages with either license."

The integration test `test_list_packages_multi_license_filter` validates this: it seeds packages with MIT, Apache-2.0, and GPL-3.0-only licenses, queries `?license=MIT,Apache-2.0`, and asserts that exactly 2 packages are returned (MIT and Apache-2.0), confirming via `body.items.iter().all(|p| p.license == "MIT" || p.license == "Apache-2.0")`.

## Evidence

- `modules/fundamental/src/package/endpoints/list.rs`: `validate_license_param` splits on commas and trims whitespace
- `modules/fundamental/src/package/service/mod.rs`: `Condition::any().add(is_in(...))` produces a union (OR) query
- `tests/api/package.rs`: `test_list_packages_multi_license_filter` confirms multi-license filtering returns the union
