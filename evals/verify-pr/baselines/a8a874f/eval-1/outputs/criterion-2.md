# Criterion 2: `GET /api/v2/package?license=MIT,Apache-2.0` returns packages with either license

## Verdict: PASS

## Reasoning

The `validate_license_param` function in `list.rs` splits the comma-separated license string into individual identifiers:

```rust
let identifiers: Vec<String> = license.split(',').map(|s| s.trim().to_string()).collect();
```

Each identifier is validated individually against SPDX expressions. The resulting vector is passed to `PackageService::list()` as `license_filter`.

In `service/mod.rs`, the filter uses `Condition::any()` with `is_in()`, which produces a SQL `WHERE license IN ('MIT', 'Apache-2.0')` clause. This returns the union of packages matching any of the specified licenses.

The integration test `test_list_packages_multi_license_filter` seeds packages with MIT, Apache-2.0, and GPL-3.0-only licenses, requests `?license=MIT,Apache-2.0`, and asserts that exactly 2 packages are returned with licenses matching either MIT or Apache-2.0. The GPL-3.0-only package is correctly excluded.

This criterion is satisfied by both the implementation and the test coverage.
