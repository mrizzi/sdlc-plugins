## Criterion 2: `GET /api/v2/package?license=MIT,Apache-2.0` returns packages with either license

### Result: PASS

### Reasoning

The PR implements comma-separated license filtering as follows:

**Parsing** (`modules/fundamental/src/package/endpoints/list.rs`):
- `validate_license_param` splits the `license` string on commas: `license.split(',').map(|s| s.trim().to_string()).collect()`. This correctly handles the comma-separated format `MIT,Apache-2.0` and produces a `Vec<String>` containing `["MIT", "Apache-2.0"]`.
- Each individual identifier is validated via `spdx::Expression::parse(id)`.

**Query construction** (`modules/fundamental/src/package/service/mod.rs`):
- The filter uses `Condition::any()` with `is_in(licenses.iter().cloned())`. The `is_in` clause generates a SQL `WHERE license IN ('MIT', 'Apache-2.0')`, which inherently returns the union of packages matching either license. The `Condition::any()` wrapper is semantically consistent with OR logic.

**Test coverage** (`tests/api/package.rs`):
- `test_list_packages_multi_license_filter` seeds packages with MIT, Apache-2.0, and GPL-3.0-only licenses, requests `?license=MIT,Apache-2.0`, and asserts that exactly 2 packages are returned and each has either `MIT` or `Apache-2.0` as its license.

The implementation correctly handles multi-value license filtering with union semantics.
