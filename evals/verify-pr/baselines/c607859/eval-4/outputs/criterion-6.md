# Criterion 6: Existing package list endpoint tests continue to pass (backward compatible)

## Criterion Text
Existing package list endpoint tests continue to pass (backward compatible)

## Verdict: PASS

## Reasoning

The task states "All CI checks pass," which indicates that the existing test suite, including any pre-existing package list endpoint tests, passes successfully with the changes in this PR.

Examining the diff for backward compatibility:

1. **Struct change**: The addition of `vulnerability_count: i64` to `PackageSummary` is an additive change. In JSON serialization, adding a new field to a response does not break existing consumers that ignore unknown fields.

2. **Service layer**: The service in `modules/fundamental/src/package/service/mod.rs` now maps the query results through a new iterator that constructs `PackageSummary` instances with all fields including `vulnerability_count`. The existing fields (`id`, `name`, `version`, `license`) are preserved.

3. **Endpoint**: The change in `modules/fundamental/src/package/endpoints/list.rs` is only a comment addition -- no functional change to the endpoint logic.

4. **CI status**: Per the eval instructions, all CI checks pass, which means existing tests are not broken.

The change is additive and backward compatible. Existing API consumers will simply see a new `vulnerability_count` field in the response, which they can ignore if they don't need it.

## Evidence

- CI status: All checks pass (per eval fixture)
- The struct change is purely additive (new field, no fields removed or renamed)
- The endpoint handler logic is unchanged
- No existing test files were modified (only a new test file was added)
