# Duplicate Check — TC-8003

## Step 4 — Duplicate, Sibling, and Overlap Check

### JQL Search

Searched for sibling Vulnerability issues with the same CVE label:

```
project = TC AND labels = 'CVE-2026-31812' AND issuetype = 10024 AND key != TC-8003
```

**Result**: 1 sibling issue found.

### Sibling Analysis

| Issue | Summary | Stream Suffix | Status | Affects Versions |
|-------|---------|---------------|--------|------------------|
| TC-7999 | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] | [rhtpa-2.2] | In Progress | RHTPA 2.2.0, RHTPA 2.2.1 |
| TC-8003 (current) | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] | [rhtpa-2.2] | New | RHTPA 2.2.0 |

### Step 4.1 — Same-Stream Duplicate Classification

TC-7999 has the **same stream suffix** `[rhtpa-2.2]` as TC-8003. Both issues track CVE-2026-31812 for the 2.2.x stream.

**Classification: Same-stream duplicate.**

TC-7999 is already **In Progress**, meaning triage and remediation are actively underway for this CVE in this stream. TC-7999 also has a more complete Affects Versions list (RHTPA 2.2.0, RHTPA 2.2.1) compared to TC-8003 (RHTPA 2.2.0 only).

### Recommendation

**Close TC-8003 as Duplicate of TC-7999.**

Rationale:
- Both issues track the same CVE (CVE-2026-31812) for the same stream (2.2.x)
- TC-7999 is already In Progress, indicating active remediation
- TC-7999 has a more complete Affects Versions list (includes RHTPA 2.2.1)
- Keeping TC-8003 open would create redundant tracking

### Proposed Jira Actions (pending engineer confirmation)

1. **Add comment to TC-8003**:
   > Duplicate of TC-7999 -- same CVE (CVE-2026-31812) tracked for the same stream [rhtpa-2.2]. TC-7999 is already In Progress with Affects Versions [RHTPA 2.2.0, RHTPA 2.2.1]. Version impact analysis confirms overlap: both issues cover the 2.2.x stream where quinn-proto < 0.11.14 is vulnerable in versions 2.2.0, 2.2.1, and 2.2.2 (retag).

2. **Transition TC-8003 to Closed** with resolution "Duplicate"

3. **Assign TC-8003** to current user

4. **Add `ai-cve-triaged` label** to TC-8003

Note: Steps 4.2 (cross-stream coordination), 4.3 (cross-CVE overlap), and 4.4 (preemptive task reconciliation) are not applicable since this issue is being closed as a duplicate. Steps 5, 6, and 7 are also skipped -- the existing sibling TC-7999 handles remediation for this stream.
