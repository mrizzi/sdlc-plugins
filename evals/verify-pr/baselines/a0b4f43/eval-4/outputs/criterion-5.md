## Criterion 5: Existing package list endpoint tests continue to pass (backward compatible)

### Verdict: PASS

### Analysis

The PR adds a new field (`vulnerability_count`) to `PackageSummary`. This is generally backward compatible for API consumers because adding a new field to a JSON response does not break clients that ignore unknown fields. Several factors support this assessment:

1. **Existing test assertions**: If existing tests deserialize the response into `PackageSummary` and the struct previously did not have `vulnerability_count`, those tests would need to be updated to include the new field. However, since the field is always populated (hardcoded to 0), deserialization should succeed as long as the test code uses the updated struct definition.

2. **No existing package tests in the repo**: The repository structure (`repo-backend.md`) shows test files at `tests/api/sbom.rs`, `tests/api/advisory.rs`, and `tests/api/search.rs`, but no existing `tests/api/package.rs` or similar. The only package test file is the newly created `tests/api/package_vuln_count.rs`. This suggests there may not be pre-existing package list endpoint tests to break.

3. **Endpoint change**: The diff in `list.rs` shows only a comment change on the existing `list()` call -- no functional change to the endpoint handler logic. The service method signature appears unchanged (still takes `offset` and `limit`).

4. **CI checks**: The task states that all CI checks pass, which would include any existing test suites. This provides indirect evidence of backward compatibility.

Given the CI passes and the minimal change to endpoint code, this criterion is satisfied.

### Evidence

- File: `modules/fundamental/src/package/endpoints/list.rs` -- only a comment change, no functional modification to the endpoint.
- Repository structure shows no pre-existing package-specific test file.
- CI checks reportedly pass.
- The new field is additive (does not remove or rename existing fields).
