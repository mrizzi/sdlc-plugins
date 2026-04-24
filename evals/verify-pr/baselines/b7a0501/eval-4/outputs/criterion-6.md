# Criterion 6: Existing package list endpoint tests continue to pass (backward compatible)

## Status: PASS (conditional)

## Evidence

The diff does not modify any existing test files. The only test file in the diff is a newly created file `tests/api/package_vuln_count.rs`. The existing tests under `tests/api/` (e.g., `sbom.rs`, `advisory.rs`, `search.rs`) are untouched.

However, backward compatibility depends on whether existing tests deserialize `PackageSummary` and would break from the new field. Since the new field is additive (a new field in the JSON response), existing test assertions that check specific fields should not break -- additional fields in JSON are typically ignored during deserialization unless strict mode is enabled.

Without evidence of existing tests failing, this criterion passes conditionally. Full confirmation would require running the test suite.
