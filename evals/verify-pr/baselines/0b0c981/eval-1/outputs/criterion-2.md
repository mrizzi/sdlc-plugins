## Criterion 2: Comma-Separated License Filter

**Text:** `GET /api/v2/package?license=MIT,Apache-2.0` returns packages with either license

**Verdict:** PASS

**Reasoning:**

In `validate_license_param`, the license string is split by comma: `license.split(',').map(|s| s.trim().to_string())`. Each identifier is validated individually via `Expression::parse(id)`. The resulting `Vec<String>` is passed to the service.

In `service/mod.rs`, the filter uses `Condition::any()` with `is_in(licenses.iter().cloned())`, which creates SQL `WHERE license IN ('MIT', 'Apache-2.0')` union semantics.

The test `test_list_packages_multi_license_filter` seeds MIT, Apache-2.0, and GPL-3.0-only packages, filters by `MIT,Apache-2.0`, and asserts `body.items.len() == 2` with items matching either license.
