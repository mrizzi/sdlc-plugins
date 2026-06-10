# Criterion 2: `GET /api/v2/package?license=MIT,Apache-2.0` returns packages with either license

## Verdict: PASS

## Reasoning

The PR diff implements comma-separated multi-license filtering:

1. **Parsing** (`list.rs`): The `validate_license_param()` function splits the `license` parameter on commas (`license.split(',')`) and trims each part. For `MIT,Apache-2.0`, this produces `["MIT", "Apache-2.0"]`. Each identifier is validated individually via `spdx::Expression::parse()`.

2. **Query construction** (`service/mod.rs`): The `license_filter` slice `["MIT", "Apache-2.0"]` is passed to:
   ```rust
   Condition::any()
       .add(package_license::Column::License.is_in(licenses.iter().cloned()))
   ```
   `Condition::any()` with `is_in` generates a `WHERE package_license.license IN ('MIT', 'Apache-2.0')` SQL clause. This correctly returns the union of packages matching either license.

3. **Test coverage** (`tests/api/package.rs`): The `test_list_packages_multi_license_filter` test seeds three packages (MIT, Apache-2.0, GPL-3.0-only), requests `?license=MIT,Apache-2.0`, and asserts:
   - Response status is 200 OK
   - Exactly 2 items are returned (MIT and Apache-2.0, not GPL-3.0-only)
   - All returned items have license equal to either "MIT" or "Apache-2.0"

The union semantics are correctly implemented via SQL `IN` clause, and the test validates that only the matching licenses are returned while non-matching ones are excluded.
