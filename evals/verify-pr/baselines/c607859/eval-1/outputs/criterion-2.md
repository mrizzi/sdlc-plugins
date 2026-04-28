# Criterion 2: `GET /api/v2/package?license=MIT,Apache-2.0` returns packages with either license

## Verdict: PASS

## Analysis

The `validate_license_param` function in `modules/fundamental/src/package/endpoints/list.rs` splits the license parameter by commas:

```rust
let identifiers: Vec<String> = license.split(',').map(|s| s.trim().to_string()).collect();
```

This produces a vector of individual license identifiers (e.g., `["MIT", "Apache-2.0"]`).

In the service layer (`modules/fundamental/src/package/service/mod.rs`), the filter uses `Condition::any()` with `is_in`:

```rust
Condition::any()
    .add(package_license::Column::License.is_in(licenses.iter().cloned()))
```

The `is_in` clause generates a SQL `IN (...)` predicate, which matches packages whose license is any of the provided values. This correctly implements union semantics -- packages with either MIT or Apache-2.0 license are returned.

The integration test `test_list_packages_multi_license_filter` seeds three packages with MIT, Apache-2.0, and GPL-3.0-only licenses, then requests `?license=MIT,Apache-2.0` and asserts:
- 2 items returned (MIT and Apache-2.0, excluding GPL-3.0-only)
- All items have license == "MIT" or license == "Apache-2.0"

## Conclusion

Comma-separated license values correctly produce a union filter, and the test validates this behavior.
