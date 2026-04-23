# Criterion 2: GET /api/v2/package?license=MIT,Apache-2.0 returns packages with either license

## Result: PASS

## Analysis

The implementation satisfies this criterion through the following code path:

**1. Comma-separated parsing (list.rs):**
The `validate_license_param` function splits the input on commas:
```rust
let identifiers: Vec<String> = license.split(',').map(|s| s.trim().to_string()).collect();
```
For input `"MIT,Apache-2.0"`, this produces `vec!["MIT", "Apache-2.0"]`. Each identifier is individually validated against the SPDX expression parser.

**2. OR-based filtering (service/mod.rs):**
The service layer uses `Condition::any()` with `is_in`, which generates a SQL `WHERE license IN ('MIT', 'Apache-2.0')` clause:
```rust
query = query.filter(
    Condition::any()
        .add(package_license::Column::License.is_in(licenses.iter().cloned()))
);
```
`Condition::any()` produces an OR condition, meaning packages with *either* MIT or Apache-2.0 license will match. The `is_in` method on SeaORM columns generates the correct SQL IN clause.

**3. Test coverage:**
The test `test_list_packages_multi_license_filter` explicitly verifies this behavior: it seeds packages with MIT, Apache-2.0, and GPL-3.0-only licenses, filters by `"MIT,Apache-2.0"`, and asserts that exactly 2 packages are returned (the MIT and Apache-2.0 ones), and that the GPL-3.0-only package is excluded.

The union semantics (returning packages with *either* license) are correctly implemented via the OR condition.
