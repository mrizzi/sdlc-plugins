# Step 3 -- Affects Versions Correction

## Step 3.1 -- Discover Available Jira Versions

Proposed action: dynamically discover available Jira versions via API:

```
jira.getJiraIssueTypeMetaWithFields(
  projectIdOrKey: "TC",
  issueTypeId: "10024"
)
```

Filter the returned `versions` field's `allowedValues` by the Jira version prefix
**RHTPA** to exclude unrelated versions.

Expected Jira Versions matching "RHTPA":

| Jira ID | Name | Released | Release Date |
|---------|------|----------|--------------|
| (dynamic) | RHTPA 2.1.0 | yes | 2025-09-15 |
| (dynamic) | RHTPA 2.1.1 | yes | 2025-11-20 |
| (dynamic) | RHTPA 2.2.0 | yes | 2025-12-03 |
| (dynamic) | RHTPA 2.2.1 | yes | 2026-02-05 |
| (dynamic) | RHTPA 2.2.2 | yes | 2026-02-23 |
| (dynamic) | RHTPA 2.2.3 | yes | 2026-03-23 |
| (dynamic) | RHTPA 2.2.4 | yes | 2026-05-04 |

Version IDs are discovered dynamically at runtime (Important Rule 6) -- the
exact Jira IDs are not hardcoded.

## Step 3.2 -- Compare and Correct Affects Versions

**Stream scope**: This issue is scoped to stream **2.2.x** (suffix `[rhtpa-2.2]`).
Only 2.2.x versions are included in the Affects Versions correction. The 2.1.x
versions (also affected per the version impact table) belong to a companion
sibling issue, not this one.

**Affected 2.2.x versions from version impact table**: RHTPA 2.2.0 (YES),
RHTPA 2.2.1 (YES), RHTPA 2.2.2 (YES -- retag of 2.2.1)

**Comparison:**

```
Current Affects Versions:  [RHTPA 2.0.0]
Proposed Affects Versions: [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]
```

The PSIRT-assigned value **RHTPA 2.0.0** is incorrect -- there is no version
2.0.0 in the supportability matrix or Jira version registry. The lock file
analysis confirms that the actually affected 2.2.x versions are 2.2.0, 2.2.1,
and 2.2.2 (all ship quinn-proto < 0.11.14).

Versions 2.2.3 and 2.2.4 are excluded because they ship quinn-proto 0.11.14,
which is the fixed version and therefore not affected.

**Proposed Jira update** (after engineer confirmation):

```
jira.edit_issue("TC-8001", fields={
  "versions": [
    {"id": "<RHTPA-2.2.0-jira-id>"},
    {"id": "<RHTPA-2.2.1-jira-id>"},
    {"id": "<RHTPA-2.2.2-jira-id>"}
  ]
})
```

Jira version IDs are resolved from the dynamic version discovery in Step 3.1,
not hardcoded values.

**Proposed comment** (after engineer confirmation):

```
jira.add_comment("TC-8001",
  "Corrected Affects Versions: [RHTPA 2.0.0] -> [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2].
  Based on lock file analysis at pinned commits from security-matrix.md.
  Scoped to stream 2.2.x per issue suffix [rhtpa-2.2].

  Evidence:
  - RHTPA 2.2.0 (v0.4.5): quinn-proto 0.11.9 (affected, < 0.11.14)
  - RHTPA 2.2.1 (v0.4.8): quinn-proto 0.11.12 (affected, < 0.11.14)
  - RHTPA 2.2.2 (v0.4.9): retag of 2.2.1 (affected, same as 2.2.1)
  - RHTPA 2.2.3 (v0.4.11): quinn-proto 0.11.14 (not affected, >= 0.11.14)
  - RHTPA 2.2.4 (v0.4.12): quinn-proto 0.11.14 (not affected, >= 0.11.14)")
```

All Affects Versions changes, label additions, and status transitions described
above are proposals for engineer confirmation -- no Jira mutations are executed
without explicit approval.
