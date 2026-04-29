# Criterion 2: `GET /api/v2/package?license=MIT,Apache-2.0` returns packages with either license

## Verdict: PASS

## Reasoning

The PR diff demonstrates that multi-license (comma-separated) filtering is correctly implemented and tested.

### Implementation Evidence

1. **Comma splitting** (`validate_license_param` in `list.rs`):
   - The function splits the input on commas: `license.split(',').map(|s| s.trim().to_string()).collect()`.
   - For `"MIT,Apache-2.0"`, this produces `["MIT", "Apache-2.0"]`.
   - Each identifier is validated individually via `Expression::parse(id)`.

2. **OR-based filtering** (`service/mod.rs`):
   - The filter uses `Condition::any()` with `is_in(licenses.iter().cloned())`, which generates SQL equivalent to `WHERE license IN ('MIT', 'Apache-2.0')`.
   - `Condition::any()` is the correct SeaORM construct for OR semantics -- packages matching any of the provided licenses will be returned.

3. **End-to-end flow**: The handler passes the validated `Vec<String>` with both values into the service, which applies the `IN` clause across all values. This correctly returns the union of packages matching either license.

### Test Evidence

The test `test_list_packages_multi_license_filter` in `tests/api/package.rs`:
- Seeds three packages: `pkg-a` (MIT), `pkg-b` (Apache-2.0), `pkg-c` (GPL-3.0-only)
- Requests `GET /api/v2/package?license=MIT,Apache-2.0`
- Asserts response status is 200 OK
- Asserts exactly 2 items are returned (MIT and Apache-2.0, not GPL-3.0-only)
- Asserts all returned items have license equal to either `"MIT"` or `"Apache-2.0"`

This test directly validates the criterion's requirement that comma-separated license values return the union of matching packages, excluding non-matching ones.
