## Criterion 6: Existing package list endpoint tests continue to pass (backward compatible)

**Result: PASS**

### Analysis

The changes in this PR are additive in nature:

1. **Model change**: A new field (`vulnerability_count`) is added to `PackageSummary`. No existing fields are modified or removed. This is a backward-compatible struct change.

2. **Service change**: The service layer in `modules/fundamental/src/package/service/mod.rs` adds a mapping step that constructs `PackageSummary` with the new field set to 0. The existing query logic (offset, limit, database fetch) is unchanged. The existing fields (`id`, `name`, `version`, `license`) are all preserved in the mapping.

3. **Endpoint change**: The endpoint in `modules/fundamental/src/package/endpoints/list.rs` has only a comment change on an existing line -- no behavioral modification.

4. **Test file**: A new test file (`tests/api/package_vuln_count.rs`) is created. No existing test files are modified or deleted.

5. **CI status**: All CI checks pass (as reported), which confirms existing tests are not broken by this change.

The change is purely additive -- a new field with a default value of 0, a new test file, and no modifications to existing test logic. Existing package list endpoint tests would continue to pass because the response structure is extended, not altered.

This criterion is satisfied.
