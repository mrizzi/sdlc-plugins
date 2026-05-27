## Criterion 2: `GET /api/v2/package?license=MIT,Apache-2.0` returns packages with either license

### Verdict: PASS

### Reasoning

**Endpoint layer** (`modules/fundamental/src/package/endpoints/list.rs`):
- The `license` query parameter value `"MIT,Apache-2.0"` is passed to `validate_license_param`.
- `validate_license_param` splits on `,` and trims whitespace, producing `["MIT", "Apache-2.0"]`.
- Each identifier is validated individually via `Expression::parse`. Both "MIT" and "Apache-2.0" are valid SPDX identifiers, so validation passes.
- The resulting `Vec<String>` is passed as `Some(&["MIT", "Apache-2.0"])` to the service.

**Service layer** (`modules/fundamental/src/package/service/mod.rs`):
- The `is_in(licenses.iter().cloned())` call generates a SQL `WHERE package_license.license IN ('MIT', 'Apache-2.0')` clause wrapped in `Condition::any()`.
- The `InnerJoin` on `PackageLicense` ensures only packages with a matching license row are included.
- This implements OR/union semantics: packages with either MIT or Apache-2.0 license are returned.

**Test coverage** (`tests/api/package.rs`):
- `test_list_packages_multi_license_filter` seeds three packages (MIT, Apache-2.0, GPL-3.0-only), requests `?license=MIT,Apache-2.0`, and asserts:
  - Response status is 200 OK
  - Exactly 2 items returned (GPL-3.0-only is excluded)
  - All items have license equal to either "MIT" or "Apache-2.0"

The implementation correctly handles comma-separated license values with union semantics, and the test validates this behavior.
