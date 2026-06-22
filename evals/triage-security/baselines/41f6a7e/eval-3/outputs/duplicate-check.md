# Step 4 -- Duplicate and Sibling Check: TC-8003

## JQL Search Results

A JQL search for sibling issues with the same CVE label (`CVE-2026-31812`) returned one result:

| Field | Value |
|-------|-------|
| Issue key | TC-7999 |
| Status | In Progress |
| Labels | CVE-2026-31812, pscomponent:org/rhtpa-server |
| Affects Versions | RHTPA 2.2.0, RHTPA 2.2.1 |
| Stream suffix | [rhtpa-2.2] |

## Classification

TC-8003 stream suffix: `[rhtpa-2.2]` (stream 2.2.x)
TC-7999 stream suffix: `[rhtpa-2.2]` (stream 2.2.x)

Both issues have the **same stream suffix** (`[rhtpa-2.2]`). This makes TC-7999 a **same-stream sibling** of TC-8003.

## Same-Stream Duplicate Analysis (Step 4.1)

Per the triage-security skill's Step 4.1 rules:

> If a same-stream sibling exists and is open or in progress:
> - Recommendation: Close the current issue as Duplicate.

TC-7999 is currently **In Progress**, meaning it is actively being worked on. It already has Affects Versions `RHTPA 2.2.0, RHTPA 2.2.1`, which covers the affected versions in the 2.2.x stream.

TC-8003 (the current issue) tracks the same CVE (CVE-2026-31812) for the same stream (2.2.x) and the same component (pscomponent:org/rhtpa-server). The version impact analysis confirms:
- TC-8003 Affects Versions: RHTPA 2.2.0 (PSIRT-assigned)
- TC-7999 Affects Versions: RHTPA 2.2.0, RHTPA 2.2.1
- Both are scoped to the 2.2.x stream

TC-7999 already has broader version coverage (includes RHTPA 2.2.1) and is actively In Progress. TC-8003 is therefore a **duplicate** of TC-7999.

## Companion Issues Landscape

| Issue | Stream | Status | Affects Versions | Duplicate? |
|-------|--------|--------|------------------|------------|
| TC-7999 | 2.2.x | In Progress | RHTPA 2.2.0, RHTPA 2.2.1 | -- (original) |
| TC-8003 (current) | 2.2.x | New | RHTPA 2.2.0 | YES -- duplicate of TC-7999 |

## Recommendation

**Close TC-8003 as Duplicate of TC-7999.**

Proposed actions (pending engineer confirmation):
1. Add comment to TC-8003: "Duplicate of TC-7999 -- same CVE (CVE-2026-31812) tracked for the same stream [rhtpa-2.2]. Version impact analysis confirms overlap. TC-7999 is already In Progress with Affects Versions [RHTPA 2.2.0, RHTPA 2.2.1]."
2. Transition TC-8003 to Closed with resolution "Duplicate".
3. Assign TC-8003 to the current user.
4. Add the `ai-cve-triaged` label to TC-8003.
