# Step 3 -- Affects Versions Correction: TC-8005

## 3.1 -- Jira Version Discovery

Versions matching prefix "RHTPA" (from getJiraIssueTypeMetaWithFields):

| Jira ID | Name | Released | Release Date |
|---------|------|----------|--------------|
| (dynamic) | RHTPA 2.1.0 | yes | 2025-09-15 |
| (dynamic) | RHTPA 2.1.1 | yes | 2025-11-20 |
| (dynamic) | RHTPA 2.2.0 | yes | 2025-12-03 |
| (dynamic) | RHTPA 2.2.1 | yes | 2026-02-05 |
| (dynamic) | RHTPA 2.2.2 | yes | 2026-02-23 |
| (dynamic) | RHTPA 2.2.3 | yes | 2026-03-23 |
| (dynamic) | RHTPA 2.2.4 | yes | 2026-05-04 |

## 3.2 -- Affects Versions Comparison

**Issue stream scope**: 2.2.x (from summary suffix `[rhtpa-2.2]`)

**Version impact table (scoped to 2.2.x stream):**
- RHTPA 2.2.0: YES (affected)
- RHTPA 2.2.1: YES (affected)
- RHTPA 2.2.2: YES (affected, retag of 2.2.1)
- RHTPA 2.2.3: NO (ships fixed version)
- RHTPA 2.2.4: NO (ships fixed version)

**PSIRT-assigned Affects Versions**: RHTPA 2.0.0

**PSIRT version is wrong** -- "RHTPA 2.0.0" does not correspond to any version in the supportability matrix or Jira version registry. No 2.0.x stream exists.

### Proposed Correction

```
Current:  [RHTPA 2.0.0]
Proposed: [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]
```

Rationale: Lock file analysis at pinned commits from security-matrix.md shows
that openssl-libs versions before 3.0.7-28.el9_4 are present in versions
2.2.0 (3.0.7-25.el9_3), 2.2.1 (3.0.7-27.el9_4), and 2.2.2 (retag of 2.2.1).
Versions 2.2.3 and 2.2.4 ship the fixed version 3.0.7-28.el9_4 and are not affected.
Correction is scoped to stream 2.2.x per issue suffix `[rhtpa-2.2]`.

The 2.1.x versions (2.1.0, 2.1.1) are also affected but belong to a sibling
issue's scope -- they are not included in this issue's Affects Versions.

### Jira Mutation (pending confirmation)

```
jira.edit_issue("TC-8005", fields={
  "versions": [
    {"id": "<RHTPA-2.2.0-jira-id>"},
    {"id": "<RHTPA-2.2.1-jira-id>"},
    {"id": "<RHTPA-2.2.2-jira-id>"}
  ]
})
```

### Comment (pending confirmation)

```
Corrected Affects Versions: [RHTPA 2.0.0] --> [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2].
Based on rpms.lock.yaml analysis at pinned commits from security-matrix.md.
Scoped to stream 2.2.x per issue suffix [rhtpa-2.2].

RHTPA 2.0.0 does not correspond to any known product version.
Versions 2.2.3+ ship the fixed openssl-libs 3.0.7-28.el9_4 and are not affected.
```
