# Criterion 5: Existing package list endpoint tests continue to pass (backward compatible)

## Verdict: PASS (with caveat)

## Evidence

The diff does not modify any existing test files. The only test file in the diff is the newly created `tests/api/package_vuln_count.rs`. The existing test files (`tests/api/sbom.rs`, `tests/api/advisory.rs`, `tests/api/search.rs`) are untouched.

However, adding a new field to `PackageSummary` could break existing tests if they perform exact struct matching or exhaustive deserialization. In Rust with Serde, the default behavior for `Deserialize` is to ignore unknown fields, so adding a field is typically backward compatible for JSON consumers. For internal tests that construct `PackageSummary` directly, they would need to be updated -- but since CI passes (given), this is not an issue.

## Assessment

Given that CI passes and no existing tests were modified, backward compatibility is maintained.
