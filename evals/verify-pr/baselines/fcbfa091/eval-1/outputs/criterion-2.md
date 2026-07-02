## Criterion 2: `GET /api/v2/package?license=MIT,Apache-2.0` returns packages with either license

### Verdict: PASS

### Analysis

This criterion requires that the endpoint supports comma-separated license values and returns the union of packages matching any of the specified licenses.

#### Parsing Logic (`modules/fundamental/src/package/endpoints/list.rs`)

The `validate_license_param` function handles comma-separated values:

```rust
fn validate_license_param(license: &str) -> Result<Vec<String>, AppError> {
    let identifiers: Vec<String> = license.split(',').map(|s| s.trim().to_string()).collect();
    for id in &identifiers {
        Expression::parse(id).map_err(|_| {
            AppError::BadRequest(format!("Invalid SPDX license identifier: {}", id))
        })?;
    }
    Ok(identifiers)
}
```

Key observations:
- Splits the input string by comma: `license.split(',')`
- Trims whitespace from each identifier: `.map(|s| s.trim().to_string())`
- Validates each identifier individually against SPDX
- Returns a `Vec<String>` containing all parsed identifiers

#### Service Layer (`modules/fundamental/src/package/service/mod.rs`)

The service uses `Condition::any()` with `is_in`, which produces a SQL `IN` clause:

```rust
query = query.filter(
    Condition::any()
        .add(package_license::Column::License.is_in(licenses.iter().cloned()))
);
```

`Condition::any()` combined with `is_in` correctly implements OR semantics -- a package matches if its license is any one of the provided values. This returns the union of packages matching MIT or Apache-2.0.

#### Test Coverage

The test `test_list_packages_multi_license_filter` validates this criterion:
- Seeds packages with MIT, Apache-2.0, and GPL-3.0-only licenses
- Queries `?license=MIT,Apache-2.0`
- Asserts exactly 2 results returned (MIT and Apache-2.0 packages)
- Asserts all returned packages have either MIT or Apache-2.0 license

### Evidence

- `validate_license_param` correctly splits comma-separated input into individual identifiers
- `Condition::any()` with `is_in` produces correct SQL OR/IN semantics for union filtering
- Integration test seeds 3 packages with different licenses and confirms only the 2 requested licenses are returned
- Whitespace trimming (`s.trim()`) handles edge cases like `?license=MIT, Apache-2.0`
