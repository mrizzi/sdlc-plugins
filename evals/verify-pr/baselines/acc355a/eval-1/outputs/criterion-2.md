## Criterion 2: `GET /api/v2/package?license=MIT,Apache-2.0` returns packages with either license

### Verdict: PASS

### Evidence

**Endpoint layer (`list.rs`):**
- `validate_license_param` splits the `license` parameter by comma: `license.split(',').map(|s| s.trim().to_string()).collect()`. This produces a `Vec<String>` with multiple identifiers (e.g., `["MIT", "Apache-2.0"]`).
- Each identifier is individually validated via `Expression::parse(id)`.
- The resulting vector is passed to the service layer.

**Service layer (`service/mod.rs`):**
- The filter uses `Condition::any()` combined with `package_license::Column::License.is_in(licenses.iter().cloned())`. The `is_in` clause generates a SQL `IN (...)` predicate, which inherently matches any of the provided values (union semantics).

**Test evidence (`tests/api/package.rs`):**
- `test_list_packages_multi_license_filter` seeds three packages (MIT, Apache-2.0, GPL-3.0-only), requests `?license=MIT,Apache-2.0`, and asserts:
  - Response status is 200 OK
  - Exactly 2 items are returned (MIT and Apache-2.0, excluding GPL-3.0-only)
  - All returned items have license equal to either "MIT" or "Apache-2.0"

The comma-separated parsing, IN-clause filtering, and test all confirm union-style multi-license filtering works correctly.
