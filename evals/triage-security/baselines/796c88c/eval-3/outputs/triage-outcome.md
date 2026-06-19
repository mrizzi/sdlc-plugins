# Triage Outcome: TC-8003

## Decision: Close as Duplicate

TC-8003 is a **same-stream duplicate** of TC-7999. Both issues track CVE-2026-31812 (quinn-proto DoS vulnerability) for the same version stream [rhtpa-2.2]. TC-7999 is already In Progress with broader Affects Versions coverage.

**No further triage steps are required.** Duplicate detection short-circuits the workflow -- remediation task creation and version-by-version lock file analysis are skipped.

## Proposed Mutations

The following actions are **proposals only** (not executed):

### 1. Close TC-8003 as Duplicate

- **Action**: Transition TC-8003 to **Closed**
- **Resolution**: Duplicate
- **Duplicate of**: TC-7999

### 2. Add Comment to TC-8003

**Proposed comment text**:

> Closing as duplicate of TC-7999.
>
> Both issues track CVE-2026-31812 (quinn-proto) for the same version stream [rhtpa-2.2]. TC-7999 is already In Progress and covers Affects Versions RHTPA 2.2.0 and RHTPA 2.2.1, which is a superset of this issue's RHTPA 2.2.0. All triage and remediation work should continue on TC-7999.

### 3. Link TC-8003 to TC-7999

- **Action**: Create "Duplicate" issue link from TC-8003 to TC-7999
- **Link type**: duplicates / is duplicated by

## Rationale

- **Same CVE**: Both issues reference CVE-2026-31812
- **Same stream**: Both carry the stream suffix [rhtpa-2.2], indicating they target the 2.2.x product version stream
- **Existing progress**: TC-7999 is already In Progress, meaning triage has been completed and remediation work has begun
- **Broader coverage**: TC-7999 already lists RHTPA 2.2.0 and RHTPA 2.2.1 in Affects Versions, making it the more complete tracking issue
- Maintaining two open issues for the same CVE in the same stream creates confusion and duplicates effort
