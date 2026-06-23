# Criterion 2: `GET /api/v2/package?license=MIT,Apache-2.0` returns packages with either license

## Verdict: PASS

## Reasoning

The implementation correctly handles comma-separated license values to produce a union (OR) filter:

### Parsing Logic (`modules/fundamental/src/package/endpoints/list.rs`)

1. **Comma splitting**: `validate_license_param` splits the input string by comma: `license.split(',').map(|s| s.trim().to_string()).collect()`. For `"MIT,Apache-2.0"`, this produces `["MIT", "Apache-2.0"]`.

2. **Per-identifier validation**: Each identifier is individually validated against the SPDX expression parser. Both `MIT` and `Apache-2.0` are valid SPDX identifiers, so validation passes.

3. **Trim handling**: The `.trim()` call ensures whitespace-padded values like `"MIT, Apache-2.0"` are also handled correctly.

### Query Construction (`modules/fundamental/src/package/service/mod.rs`)

4. **OR semantics**: The filter uses `Condition::any()` which generates SQL `OR` logic. With `is_in(["MIT", "Apache-2.0"])`, the generated SQL is effectively `WHERE license IN ('MIT', 'Apache-2.0')`, which returns packages matching either license.

5. **Union behavior**: The `is_in` clause with multiple values produces a set membership check, which is semantically equivalent to a union of individual filters -- exactly what the criterion requires.

### Test Coverage

The test `test_list_packages_multi_license_filter` directly validates this criterion:
- Seeds 3 packages: MIT, Apache-2.0, and GPL-3.0-only
- Queries `?license=MIT,Apache-2.0`
- Asserts status 200, exactly 2 results, and all results have `license == "MIT"` or `license == "Apache-2.0"`
- The GPL-3.0-only package is correctly excluded

## Evidence

- `"MIT,Apache-2.0".split(',')` produces `["MIT", "Apache-2.0"]`
- `Condition::any()` with `is_in(["MIT", "Apache-2.0"])` generates OR/IN semantics
- Test asserts `body.items.len() == 2` and `body.items.iter().all(|p| p.license == "MIT" || p.license == "Apache-2.0")`
