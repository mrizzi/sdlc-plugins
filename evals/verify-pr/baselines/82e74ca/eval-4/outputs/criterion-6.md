# Criterion 6: Existing package list endpoint tests continue to pass (backward compatible)

## Result: PASS (with caveat)

## Analysis

The acceptance criterion requires that existing tests for the package list endpoint continue to pass, demonstrating backward compatibility.

### Evidence

1. **CI checks pass**: Per the task setup, all CI checks pass. This indicates that existing test suites, including any pre-existing package list endpoint tests, execute successfully.

2. **API response shape change**: Adding `vulnerability_count` to `PackageSummary` changes the JSON response shape by adding a new field. This is generally backward-compatible for API consumers (adding fields does not break existing consumers that ignore unknown fields). However, it could require updates to tests that perform strict equality checks on response bodies.

3. **Existing test files**: The repository structure in `repo-backend.md` does not list a pre-existing `tests/api/package.rs` file (unlike `sbom.rs`, `advisory.rs`, and `search.rs`). This suggests that there may not have been pre-existing integration tests specifically for the package endpoint that would break.

4. **New test file**: The PR creates `tests/api/package_vuln_count.rs` with new tests that construct and assert on the new field.

### Caveat

While CI passes (per the eval setup), the hardcoded `vulnerability_count: 0` in the service layer means that the new test `test_package_with_vulnerabilities_has_count` (which expects `vulnerability_count == 3`) and `test_vulnerability_count_deduplicates_across_sboms` (which expects `vulnerability_count == 2`) would actually fail at runtime. This is a contradiction between the "CI passes" setup instruction and the actual code behavior. For the purpose of this criterion (backward compatibility of existing tests), the criterion is evaluated as satisfied since no pre-existing package tests appear to exist in the repository structure.

### Conclusion

There are no pre-existing package endpoint integration tests visible in the repository structure that would break. The addition of a new field to the response struct is backward compatible for API consumers. CI is reported as passing. This criterion is satisfied.
