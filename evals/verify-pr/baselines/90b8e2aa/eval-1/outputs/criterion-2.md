## Criterion 2: Comma-Separated License Filter

**Requirement**: `GET /api/v2/package?license=MIT,Apache-2.0` returns packages with either license.

**Verdict**: PASS

### Analysis

**Comma Splitting**: The `validate_license_param` function handles comma-separated values:

```rust
let identifiers: Vec<String> = license.split(',').map(|s| s.trim().to_string()).collect();
```

For input `"MIT,Apache-2.0"`, this produces `["MIT", "Apache-2.0"]`. Each identifier is individually validated against the SPDX expression parser.

**Union Semantics**: The service layer uses `Condition::any()` with `is_in()`:

```rust
Condition::any()
    .add(package_license::Column::License.is_in(licenses.iter().cloned()))
```

`is_in` generates a SQL `WHERE license IN ('MIT', 'Apache-2.0')` clause, which returns rows matching any of the specified values -- this is union/OR semantics as required.

**Test Coverage**: `test_list_packages_multi_license_filter` seeds 3 packages (MIT, Apache-2.0, GPL-3.0-only), queries with `?license=MIT,Apache-2.0`, and asserts:
- Response status is 200 OK
- Exactly 2 items are returned (MIT and Apache-2.0, excluding GPL-3.0-only)
- All returned items have license == "MIT" or license == "Apache-2.0"
