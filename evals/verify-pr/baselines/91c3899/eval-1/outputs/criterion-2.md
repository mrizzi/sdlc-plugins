## Criterion 2: `GET /api/v2/package?license=MIT,Apache-2.0` returns packages with either license

### Analysis

The `validate_license_param` function splits the `license` parameter by comma:

```rust
let identifiers: Vec<String> = license.split(',').map(|s| s.trim().to_string()).collect();
```

Each identifier is validated individually via `Expression::parse(id)`. The resulting vector (e.g., `["MIT", "Apache-2.0"]`) is passed to the service layer.

In `service/mod.rs`, the filter uses `Condition::any()` with `is_in(licenses.iter().cloned())`. The `is_in` SQL clause generates `WHERE package_license.license IN ('MIT', 'Apache-2.0')`, which returns packages matching either license (union semantics).

The test `test_list_packages_multi_license_filter` seeds MIT, Apache-2.0, and GPL-3.0-only packages, filters by `MIT,Apache-2.0`, and asserts that 2 items are returned, each with either MIT or Apache-2.0 license.

### Code Evidence

- `list.rs`: `license.split(',')` handles comma-separated values
- `service/mod.rs`: `Condition::any().add(is_in(...))` produces OR/union semantics
- `tests/api/package.rs`: `test_list_packages_multi_license_filter` verifies this behavior

## Verdict: PASS
