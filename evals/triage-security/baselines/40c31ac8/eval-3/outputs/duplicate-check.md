# Duplicate Check -- TC-8003

## Step 4 -- Duplicate, Sibling, Overlap, and Reconciliation Check

### JQL Search

Query: `project = TC AND labels = 'CVE-2026-31812' AND issuetype = 10024 AND key != TC-8003`

Result: **1 sibling found**

| Issue | Summary | Status | Labels | Affects Versions | Stream Suffix |
|-------|---------|--------|--------|------------------|---------------|
| TC-7999 | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] | In Progress | CVE-2026-31812, pscomponent:org/rhtpa-server | RHTPA 2.2.0, RHTPA 2.2.1 | [rhtpa-2.2] |

### Stream Classification

- **TC-8003** stream suffix: `[rhtpa-2.2]` --> stream 2.2.x
- **TC-7999** stream suffix: `[rhtpa-2.2]` --> stream 2.2.x

Both issues have the **same stream suffix**. TC-7999 is classified as a **same-stream sibling**.

### 4.1 -- Same-Stream Duplicate Detection

TC-7999 is a same-stream sibling for CVE-2026-31812 in the 2.2.x stream:

| Attribute | TC-8003 (current) | TC-7999 (sibling) |
|-----------|-------------------|-------------------|
| CVE | CVE-2026-31812 | CVE-2026-31812 |
| Stream | [rhtpa-2.2] (2.2.x) | [rhtpa-2.2] (2.2.x) |
| Status | New | In Progress |
| Affects Versions | RHTPA 2.2.0 | RHTPA 2.2.0, RHTPA 2.2.1 |
| Labels | CVE-2026-31812, pscomponent:org/rhtpa-server | CVE-2026-31812, pscomponent:org/rhtpa-server |

TC-7999 is already **In Progress** and tracks the same CVE for the same stream. It has a broader Affects Versions set (includes RHTPA 2.2.1 in addition to RHTPA 2.2.0).

**Result: TC-8003 is a DUPLICATE of TC-7999.**

Per Step 4.1 of the triage-security skill: "If a same-stream sibling exists and is open or in progress, recommend closing the current issue as Duplicate."

### Recommended Actions

1. **Add comment to TC-8003**: "Duplicate of TC-7999 -- same CVE (CVE-2026-31812) tracked for the same stream [rhtpa-2.2]. Version impact analysis confirms overlap. TC-7999 is already In Progress with Affects Versions [RHTPA 2.2.0, RHTPA 2.2.1]."
2. **Transition TC-8003** to Closed with resolution "Duplicate".
3. **Assign TC-8003** to current user.

### 4.2 -- Cross-Stream Coordination

Not applicable. No different-stream siblings were found (TC-7999 is same-stream).

### 4.3 -- Cross-CVE Overlap Detection

Skipped. The Upstream Affected Component custom field, PS Component custom field, and Stream custom field are not configured in the Security Configuration. All three fields are required for cross-CVE overlap detection.

### 4.4 -- Preemptive Task Reconciliation

Not applicable. TC-8003 is being closed as a duplicate -- no preemptive task search needed.

## Steps 5-8 -- Skipped

Because TC-8003 is a same-stream duplicate of TC-7999 (which is already In Progress), the remaining triage steps are not executed:

- **Step 5 (Version Lifecycle Check)** -- skipped, issue will be closed as duplicate
- **Step 6 (Already Fixed Check)** -- skipped, issue will be closed as duplicate
- **Step 7 (Concurrent Triage Detection)** -- skipped, no remediation tasks to create
- **Step 8 (Remediation)** -- skipped, TC-7999 already owns remediation for this CVE and stream
