# Criterion 2: `GET /api/v2/package?license=MIT,Apache-2.0` returns packages with either license

## Verdict: PASS

## Analysis

The comma-separated license value is split into individual identifiers by `validate_license_param`:
```rust
let identifiers: Vec<String> = license.split(',').map(|s| s.trim().to_string()).collect();
```

Each identifier is individually validated as a valid SPDX expression. The resulting vector is passed to the service layer, which uses `is_in` to generate a SQL `IN` clause (equivalent to `WHERE license IN ('MIT', 'Apache-2.0')`). The `Condition::any()` wrapper ensures OR semantics -- packages matching any of the specified licenses are included in the results.

## Evidence

- `list.rs`: `license.split(',').map(|s| s.trim().to_string()).collect()` splits comma-separated input
- `list.rs`: Each identifier validated via `Expression::parse(id)`
- `service/mod.rs`: `package_license::Column::License.is_in(licenses.iter().cloned())` generates the IN clause
- `tests/api/package.rs`: `test_list_packages_multi_license_filter` seeds MIT, Apache-2.0, and GPL-3.0-only packages, queries `?license=MIT,Apache-2.0`, asserts `body.items.len() == 2` and `body.items.iter().all(|p| p.license == "MIT" || p.license == "Apache-2.0")`
