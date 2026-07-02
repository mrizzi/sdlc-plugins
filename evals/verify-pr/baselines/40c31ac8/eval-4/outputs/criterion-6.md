## Criterion 6: Existing package list endpoint tests continue to pass (backward compatible)

### Result: PASS (with caveat)

### Evidence

The diff does not modify any existing test files. The changes to the package module are additive:

1. **Model change** (`summary.rs`): Adds a new field to `PackageSummary`. This is additive for JSON consumers (new field appears in output) but would require existing Rust code that constructs `PackageSummary` to include the new field. Since CI checks pass, existing tests have been updated or the struct construction is handled centrally.

2. **Service change** (`service/mod.rs`): The mapping logic now constructs `PackageSummary` explicitly with the new field. This replaces what was presumably a direct entity-to-model conversion, but the existing fields (`id`, `name`, `version`, `license`) are all preserved.

3. **Endpoint change** (`endpoints/list.rs`): Only a comment was added; no functional change to the endpoint signature or behavior.

4. **New test file** (`tests/api/package_vuln_count.rs`): This is a new file that does not modify existing tests.

The CI checks pass, which provides evidence that existing tests remain functional.

### Conclusion

This criterion is satisfied based on the additive nature of the changes and CI passing. The JSON API remains backward compatible (new fields do not break existing consumers).
