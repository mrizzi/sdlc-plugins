# Duplicate Check -- TC-8003

## Step 4 -- Duplicate, Sibling, and Overlap Check

### JQL Search

A JQL search for sibling Vulnerability issues with the same CVE label was performed:

```
project = TC AND labels = 'CVE-2026-31812' AND issuetype = 10024 AND key != TC-8003
```

### Search Results

One sibling issue was found:

| Field | Value |
|-------|-------|
| Key | TC-7999 |
| Summary | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] |
| Status | In Progress |
| Labels | CVE-2026-31812, pscomponent:org/rhtpa-server |
| Affects Versions | RHTPA 2.2.0, RHTPA 2.2.1 |
| Stream suffix | [rhtpa-2.2] |

### Step 4.1 -- Same-Stream Duplicate Analysis

**Stream comparison:**
- TC-8003 stream suffix: `[rhtpa-2.2]` --> stream 2.2.x
- TC-7999 stream suffix: `[rhtpa-2.2]` --> stream 2.2.x

Both issues have the **same stream suffix** `[rhtpa-2.2]`, placing them in the same version stream (2.2.x).

**Status check:**
- TC-7999 is **In Progress** -- it is an open, active sibling in the same stream.

**Affects Versions comparison:**
- TC-8003 (current issue): RHTPA 2.2.0
- TC-7999 (existing sibling): RHTPA 2.2.0, RHTPA 2.2.1

TC-7999 already has broader Affects Versions coverage (includes both RHTPA 2.2.0 and RHTPA 2.2.1), while TC-8003 only has RHTPA 2.2.0. The existing sibling already tracks the full set of affected versions for this stream.

### Classification

**TC-8003 is a DUPLICATE of TC-7999.**

Both issues track the same CVE (CVE-2026-31812), the same library (quinn-proto), the same component (pscomponent:org/rhtpa-server), and the same stream ([rhtpa-2.2] / 2.2.x). TC-7999 is already In Progress with the correct Affects Versions.

### Companion Issues Table

```
CVE-2026-31812 sibling issues:

| Issue      | Stream | Status      | Affects Versions              |
|------------|--------|-------------|-------------------------------|
| TC-7999    | 2.2.x  | In Progress | RHTPA 2.2.0, RHTPA 2.2.1     |
| TC-8003 <- | 2.2.x  | New         | RHTPA 2.2.0                   |
```

Arrow indicates the current issue being triaged.

### Steps 4.2, 4.3, 4.4

- **Step 4.2 (Cross-stream coordination):** Not applicable -- TC-7999 is a same-stream sibling, not a different-stream companion.
- **Step 4.3 (Cross-CVE overlap):** Skipped -- the Upstream Affected Component custom field is not configured in the Security Configuration.
- **Step 4.4 (Preemptive task reconciliation):** Not applicable -- the issue is being closed as duplicate, so no remediation task search is needed.
