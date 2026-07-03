# Step 3 -- Affects Versions Correction

## 3.1 -- Jira Version Discovery

Jira versions matching prefix "RHTPA" (from `getJiraIssueTypeMetaWithFields`):

| Jira ID | Name | Released | Release Date |
|---------|------|----------|--------------|
| 62643 | RHTPA 2.1.0 | yes | 2025-09-15 |
| 62604 | RHTPA 2.1.1 | yes | 2025-11-20 |
| 63001 | RHTPA 2.2.0 | yes | 2025-12-03 |
| 63002 | RHTPA 2.2.1 | yes | 2026-02-05 |
| 63003 | RHTPA 2.2.2 | yes | 2026-02-23 |
| 63004 | RHTPA 2.2.3 | yes | 2026-03-23 |
| 63005 | RHTPA 2.2.4 | yes | 2026-05-04 |

## 3.2 -- Compare and Correct Affects Versions

**Issue stream scope**: 2.2.x (from summary suffix `[rhtpa-2.2]`)

Only versions from the 2.2.x stream are included in the correction.

**Version impact for stream 2.2.x:**

| Version | quinn-proto | Affected? |
|---------|-------------|-----------|
| 2.2.0 | 0.11.9 | YES |
| 2.2.1 | 0.11.12 | YES |
| 2.2.2 | (retag of 2.2.1) | YES |
| 2.2.3 | 0.11.14 | NO |
| 2.2.4 | 0.11.14 | NO |

**Correction:**

```
Current:  [RHTPA 2.0.0]
Proposed: [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]
```

**Rationale**: PSIRT assigned `RHTPA 2.0.0` which does not correspond to any existing Jira version or configured stream. Lock file analysis at pinned commits from the security-matrix.md shows that versions 2.2.0, 2.2.1, and 2.2.2 ship quinn-proto < 0.11.14 and are within the issue's stream scope (2.2.x). Versions 2.2.3 and 2.2.4 already ship quinn-proto 0.11.14 (the fix version) and are NOT affected.

**Proposed Jira mutation (after engineer confirmation):**

```
jira.edit_issue("TC-8001", fields={
  "versions": [
    {"id": "63001"},
    {"id": "63002"},
    {"id": "63003"}
  ]
})
```

**Comment to post:**

```
Corrected Affects Versions: [RHTPA 2.0.0] -> [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2].
Based on lock file analysis at pinned commits from security-matrix.md.
Scoped to stream 2.2.x per issue suffix [rhtpa-2.2].
Versions 2.2.3+ ship quinn-proto 0.11.14 (fix version) and are not affected.

Note: Stream 2.1.x (versions 2.1.0, 2.1.1) is also affected but belongs to
a separate stream and is tracked by its own companion CVE issue (see Step 4).
```
