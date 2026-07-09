# Criterion 6: Existing package list endpoint tests continue to pass (backward compatible)

## Verdict: PASS

## Evidence

Per the task description, all CI checks pass. The diff makes the following changes to the package list endpoint:

1. **Model change** (`summary.rs`): Adds a new field to `PackageSummary`. This is an additive change to the JSON response -- existing fields are preserved, and a new field is added. API consumers that ignore unknown fields (standard JSON behavior) are unaffected.

2. **Service change** (`service/mod.rs`): The mapping now explicitly constructs `PackageSummary` with all fields including the new one. The existing fields (`id`, `name`, `version`, `license`) are preserved with the same values.

3. **Endpoint change** (`list.rs`): Only a comment is added; the actual endpoint logic is unchanged. The same service method is called, and the same response type is returned.

## Reasoning

The changes are purely additive at the API level. No existing fields are removed, renamed, or have their types changed. The endpoint path, HTTP method, and query parameters remain the same. The struct now has an additional field, but this does not break backward compatibility for existing API consumers that tolerate extra JSON keys.

The task states all CI checks pass, which includes existing test suites. The existing `tests/api/` test files for other endpoints (sbom, advisory, search) are unmodified and would not be affected by changes to the package module.

Note: Existing package tests (if any exist but are not shown in the diff) might need updating if they deserialize the full `PackageSummary` struct, since the new field would need to be present. However, CI passing confirms this is not an issue. This criterion is satisfied.
