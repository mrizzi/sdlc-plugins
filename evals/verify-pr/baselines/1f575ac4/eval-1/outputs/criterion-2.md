## Criterion 2: `GET /api/v2/package?license=MIT,Apache-2.0` returns packages with either license

**Verdict: PASS**

### Reasoning

The `validate_license_param` function in `list.rs` splits the license parameter by comma:

```rust
let identifiers: Vec<String> = license.split(',').map(|s| s.trim().to_string()).collect();
```

This produces `["MIT", "Apache-2.0"]` from the input `"MIT,Apache-2.0"`. Each identifier is validated individually via `Expression::parse`, then the full vector is passed to the service layer.

In the service, the filter uses `Condition::any()` with `is_in`:

```rust
Condition::any()
    .add(package_license::Column::License.is_in(licenses.iter().cloned()))
```

`Condition::any()` creates an OR condition, and `is_in` with both values generates `WHERE license IN ('MIT', 'Apache-2.0')`. This correctly returns the union of packages matching either license.

### Test Coverage

The integration test `test_list_packages_multi_license_filter` validates this criterion:
- Seeds 3 packages: MIT, Apache-2.0, and GPL-3.0-only
- Queries `?license=MIT,Apache-2.0`
- Asserts exactly 2 results and that all have `license == "MIT"` or `license == "Apache-2.0"`

This criterion is satisfied by the implementation.
