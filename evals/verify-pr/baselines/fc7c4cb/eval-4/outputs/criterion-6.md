# Criterion 6: Existing package list endpoint tests continue to pass (backward compatible)

## Verdict: PASS

## Analysis

The criterion requires that the change is backward compatible and that existing tests continue to pass.

### Evidence from the diff

1. **Additive change only**: The PR adds a new field (`vulnerability_count`) to `PackageSummary`. It does not remove or rename any existing fields (`id`, `name`, `version`, `license`). Adding a field to a JSON response is a backward-compatible change.

2. **Endpoint signature unchanged** (`endpoints/list.rs`): The endpoint function signature, route path, and return type remain the same. The only diff line is a comment addition:

   ```rust
   -        .list(params.offset, params.limit)
   +        .list(params.offset, params.limit)  // vulnerability_count now included in response
   ```

   This is a comment-only change with no behavioral impact on the endpoint's interface.

3. **No changes to existing test files**: The diff does not modify any existing test files (`tests/api/sbom.rs`, `tests/api/advisory.rs`, `tests/api/search.rs`). Only a new test file is added (`tests/api/package_vuln_count.rs`).

4. **CI status**: All CI checks pass (per the eval prompt), which confirms existing tests are not broken.

5. **API consumers**: Clients consuming the JSON response with unknown-field tolerance (the standard behavior for JSON deserialization) will not be affected by the addition of a new field.

This criterion is satisfied. The change is purely additive and backward compatible.
