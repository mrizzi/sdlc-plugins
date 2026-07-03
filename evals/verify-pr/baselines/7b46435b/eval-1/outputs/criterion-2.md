# Criterion 2: GET /api/v2/package?license=MIT,Apache-2.0 returns packages with either license

## Verdict: PASS

## Analysis

### Comma Separation Handling (list.rs)

The `validate_license_param` function handles comma-separated values:

```rust
let identifiers: Vec<String> = license.split(',').map(|s| s.trim().to_string()).collect();
```

When the input is `"MIT,Apache-2.0"`, this produces `["MIT", "Apache-2.0"]`. The `.trim()` call also handles whitespace around values (e.g., `"MIT, Apache-2.0"` would also work).

Each identifier is individually validated against the SPDX standard via `Expression::parse(id)`. Both "MIT" and "Apache-2.0" are valid SPDX identifiers, so validation succeeds, and the function returns `Ok(vec!["MIT".to_string(), "Apache-2.0".to_string()])`.

### OR Semantics in Service Layer (mod.rs)

The service method applies the filter using:

```rust
query = query.filter(
    Condition::any()
        .add(package_license::Column::License.is_in(licenses.iter().cloned()))
);
```

The `is_in` method generates a SQL `IN ('MIT', 'Apache-2.0')` clause, which inherently provides OR semantics -- a row matches if the license column equals any of the provided values. The `Condition::any()` wrapper is redundant with a single `is_in` predicate but does not change the semantics.

Combined with the `INNER JOIN` to `package_license`, this returns all packages whose license record matches either "MIT" or "Apache-2.0".

### Test Coverage

`test_list_packages_multi_license_filter` validates this criterion:
- Seeds 3 packages: pkg-a (MIT), pkg-b (Apache-2.0), pkg-c (GPL-3.0-only)
- Queries `GET /api/v2/package?license=MIT,Apache-2.0`
- Asserts response status is 200 OK
- Asserts exactly 2 items returned (pkg-a and pkg-b)
- Asserts all returned items have `license == "MIT" || license == "Apache-2.0"`

This directly verifies the union/OR behavior for comma-separated license values.

## Conclusion

The implementation correctly splits comma-separated license values, validates each independently against the SPDX standard, and applies an OR-based SQL IN filter. The test confirms that packages matching either license in the comma-separated list are returned.
