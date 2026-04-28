# Criterion 2: GET /api/v2/package?license=MIT,Apache-2.0 returns packages with either license

## Verdict: PASS

## Reasoning

### Code Analysis

The `validate_license_param` function in `list.rs` handles comma-separated values:

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

For `?license=MIT,Apache-2.0`, this produces `["MIT", "Apache-2.0"]`. Both are valid SPDX identifiers, so validation passes.

In the service layer, the filter uses `Condition::any()` with `is_in()`:

```rust
query = query.filter(
    Condition::any()
        .add(package_license::Column::License.is_in(licenses.iter().cloned()))
);
```

`Condition::any()` with `is_in(["MIT", "Apache-2.0"])` generates a SQL `WHERE license IN ('MIT', 'Apache-2.0')` clause, which returns packages with either license. This is a union/OR semantic, matching the requirement.

### Test Verification

The test `test_list_packages_multi_license_filter` in `tests/api/package.rs`:
- Seeds packages with MIT, Apache-2.0, and GPL-3.0-only licenses.
- Requests `?license=MIT,Apache-2.0`.
- Asserts the response is 200 OK.
- Asserts exactly 2 items are returned (MIT and Apache-2.0 packages; GPL-3.0-only excluded).
- Asserts all returned items have `license == "MIT" || license == "Apache-2.0"`.

This directly validates the criterion.

### Conclusion

The implementation correctly splits comma-separated license values, validates each one independently, and uses `is_in()` to match packages with any of the specified licenses. The test confirms union behavior. Criterion is satisfied.
