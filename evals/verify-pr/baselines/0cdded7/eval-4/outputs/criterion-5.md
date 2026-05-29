# Criterion 5: Existing package list endpoint tests continue to pass (backward compatible)

## Verdict: PASS (with caveat)

## Reasoning

The PR adds a new field (`vulnerability_count`) to `PackageSummary` but does not remove or rename any existing fields (`id`, `name`, `version`, `license`). This is an additive change to the struct.

Looking at the repository structure, existing tests are in `tests/api/` and include `sbom.rs`, `advisory.rs`, and `search.rs`. There are no pre-existing package endpoint tests listed in the repository structure (the `tests/api/` directory does not include a `package.rs` file).

The PR creates new test file `tests/api/package_vuln_count.rs` with three test functions. These are new tests, not modifications to existing ones.

From a backward compatibility perspective:
- The JSON response now includes an additional field (`vulnerability_count`). Consumers that ignore unknown fields (the typical JSON parsing approach) will not be affected.
- No existing fields were modified or removed.
- The service method signature (`list(offset, limit)`) was not changed.

The CI checks are reported as passing, which indicates existing tests are not broken by this change.

However, there is a significant caveat: the new tests `test_package_with_vulnerabilities_has_count` (expects count=3) and `test_vulnerability_count_deduplicates_across_sboms` (expects count=2) would fail at runtime because the implementation always returns 0. The fact that CI passes despite these tests being present is suspicious and suggests either these tests are not being run, or the CI status report is unreliable.

The criterion itself -- that existing tests continue to pass -- is satisfied since no existing tests were modified, and the changes are additive.
