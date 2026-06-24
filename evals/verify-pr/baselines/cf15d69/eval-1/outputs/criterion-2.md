# Criterion 2: `GET /api/v2/package?license=MIT,Apache-2.0` returns packages with either license

## Verdict: PASS

## Reasoning

The PR diff implements comma-separated license filtering through the following mechanism:

1. **Comma splitting** (`modules/fundamental/src/package/endpoints/list.rs`):
   - The `validate_license_param` function splits the input on commas: `license.split(',').map(|s| s.trim().to_string()).collect()`.
   - Each individual identifier is validated against SPDX expressions.
   - The function returns a `Vec<String>` of validated identifiers (e.g., `["MIT", "Apache-2.0"]`).

2. **OR-based filtering** (`modules/fundamental/src/package/service/mod.rs`):
   - The service uses `Condition::any()` which produces an OR-based SQL condition.
   - `package_license::Column::License.is_in(licenses.iter().cloned())` generates a SQL `IN` clause, matching packages with any of the specified licenses.
   - This correctly returns the union of packages matching either license.

3. **Test coverage** (`tests/api/package.rs`):
   - `test_list_packages_multi_license_filter` seeds packages with MIT, Apache-2.0, and GPL-3.0-only licenses.
   - Queries with `?license=MIT,Apache-2.0`.
   - Asserts that exactly 2 packages are returned (MIT and Apache-2.0, not GPL-3.0-only).
   - Asserts each returned package has either MIT or Apache-2.0 license via `body.items.iter().all(|p| p.license == "MIT" || p.license == "Apache-2.0")`.

The `Condition::any()` with `is_in()` correctly implements union semantics for multiple license values.
