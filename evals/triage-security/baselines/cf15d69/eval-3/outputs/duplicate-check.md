# Step 4 -- Duplicate and Sibling Check: TC-8003

## JQL Search for Sibling Issues

Search query:

```
project = TC AND labels = 'CVE-2026-31812' AND issuetype = 10024 AND key != TC-8003
```

The JQL explicitly excludes the current issue key (`key != TC-8003`) to avoid self-matching. The issue type ID 10024 is the Vulnerability issue type from Security Configuration.

### Search Results

One sibling issue found:

| Issue | Summary | Status | Labels | Affects Versions | Stream Suffix |
|-------|---------|--------|--------|------------------|---------------|
| TC-7999 | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] | In Progress | CVE-2026-31812, pscomponent:org/rhtpa-server | RHTPA 2.2.0, RHTPA 2.2.1 | [rhtpa-2.2] |

## Sibling Classification

### TC-7999 Analysis

- **TC-7999 stream suffix**: `[rhtpa-2.2]` maps to stream **2.2.x**
- **TC-8003 stream suffix**: `[rhtpa-2.2]` maps to stream **2.2.x**
- **Classification**: **Same-stream sibling (DUPLICATE)**

Both TC-8003 and TC-7999 track the same CVE (CVE-2026-31812) for the same product stream (2.2.x). TC-7999 is already In Progress with a broader set of Affects Versions (RHTPA 2.2.0 and RHTPA 2.2.1), while TC-8003 only has RHTPA 2.2.0.

This is NOT a cross-stream companion. Cross-stream companions would have different stream suffixes (e.g., `[rhtpa-2.1]` vs `[rhtpa-2.2]`), indicating they track the same CVE for different product streams. In this case, both issues have identical stream suffixes `[rhtpa-2.2]`, making TC-8003 a duplicate of TC-7999.

## Step 4.1 -- Same-Stream Duplicate Detection

A same-stream sibling (TC-7999) exists and is in an active state (In Progress).

Per the triage methodology (Step 4.1):
- TC-7999 is already tracking CVE-2026-31812 for stream 2.2.x
- TC-7999 is In Progress, meaning remediation work has already begun
- TC-7999 has Affects Versions: RHTPA 2.2.0, RHTPA 2.2.1 (superset of TC-8003's RHTPA 2.2.0)
- TC-8003 is a duplicate and should be closed

### Recommended Actions

1. **Add comment to TC-8003**:

   > Duplicate of TC-7999 -- same CVE (CVE-2026-31812) tracked for the same stream [rhtpa-2.2]. TC-7999 is already In Progress with Affects Versions [RHTPA 2.2.0, RHTPA 2.2.1]. Version impact analysis confirms overlap. Closing as Duplicate.

2. **Transition TC-8003** to Closed with resolution "Duplicate".

3. **Assign TC-8003** to current user.

## Duplicate Detection Short-Circuit

Because TC-8003 is a duplicate of TC-7999, the triage flow is short-circuited. The following steps are skipped:

- Step 5 (Version Lifecycle Check) -- not needed; TC-7999 already covers this
- Step 6 (Already Fixed Check) -- not needed; TC-7999 is the active tracker
- Step 7 (Remediation) -- not needed; remediation is managed via TC-7999
- Remediation Task Creation -- not needed; duplicate issues do not spawn tasks

No remediation tasks will be created for TC-8003. All remediation work should continue under TC-7999.
