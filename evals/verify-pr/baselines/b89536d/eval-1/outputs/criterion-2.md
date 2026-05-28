## Criterion 2: `GET /api/v2/package?license=MIT,Apache-2.0` returns packages with either license

### Verdict: PASS

### Reasoning

The `validate_license_param` function in `modules/fundamental/src/package/endpoints/list.rs` splits the `license` parameter by commas and trims whitespace:

```rust
let identifiers: Vec<String> = license.split(',').map(|s| s.trim().to_string()).collect();
```

Each identifier is individually validated against the SPDX expression parser. The resulting vector of identifiers (e.g., `["MIT", "Apache-2.0"]`) is passed to the service layer.

In `modules/fundamental/src/package/service/mod.rs`, the filter uses `Condition::any()` with `is_in`:

```rust
Condition::any()
    .add(package_license::Column::License.is_in(licenses.iter().cloned()))
```

The `is_in` clause generates a SQL `WHERE license IN ('MIT', 'Apache-2.0')` condition, which returns the union of packages matching either license. The `Condition::any()` wrapper ensures this is an OR-style match.

The integration test `test_list_packages_multi_license_filter` in `tests/api/package.rs` verifies this by seeding MIT, Apache-2.0, and GPL-3.0-only packages, querying with `?license=MIT,Apache-2.0`, and asserting that exactly 2 packages are returned, all with either MIT or Apache-2.0 licenses. The GPL-3.0-only package is correctly excluded.

### Evidence

- `modules/fundamental/src/package/endpoints/list.rs`: `validate_license_param` splits on comma, validates each identifier independently
- `modules/fundamental/src/package/service/mod.rs`: `is_in(licenses.iter().cloned())` performs SQL IN clause for multiple values
- `tests/api/package.rs`: `test_list_packages_multi_license_filter` confirms union behavior across two license types
