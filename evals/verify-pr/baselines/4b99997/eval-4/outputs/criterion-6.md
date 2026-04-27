# Criterion 6: Existing package list endpoint tests continue to pass (backward compatible)

## Result: PASS

## Analysis

Per the evaluation context, all CI checks pass on this PR. This indicates that existing tests, including any package list endpoint tests, continue to pass with the new field added.

The change adds a new field to `PackageSummary` but does not remove or modify any existing fields (`name`, `version`, `license`). Adding a field to a JSON response is backward-compatible for consumers that ignore unknown fields.

The new test file `tests/api/package_vuln_count.rs` is additive -- it creates new integration tests rather than modifying existing ones. The existing test files in `tests/api/` (sbom.rs, advisory.rs, search.rs) are not modified by this PR.

This criterion is satisfied.
