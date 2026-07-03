# Duplicate Check -- TC-8003

## Step 4: Duplicate, Sibling, and Overlap Check

### JQL Search Results

A JQL search for sibling Vulnerability issues with the same CVE label (`CVE-2026-31812`) in project TC, excluding the current issue TC-8003, returned one result:

| Issue | Summary | Status | Stream Suffix | Affects Versions |
|-------|---------|--------|---------------|------------------|
| TC-7999 | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] | In Progress | [rhtpa-2.2] | RHTPA 2.2.0, RHTPA 2.2.1 |

### Classification

**TC-7999 is a same-stream sibling.** Both TC-8003 and TC-7999 share the same stream suffix `[rhtpa-2.2]`, meaning they both track the same CVE for the same version stream (2.2.x).

Per Step 4.1 (Same-stream duplicates): when a same-stream sibling exists and is open or in progress, the recommendation is to close the current issue as Duplicate.

### Analysis

- TC-7999 is already **In Progress**, indicating active remediation work.
- TC-7999's Affects Versions (`RHTPA 2.2.0, RHTPA 2.2.1`) already cover the affected versions within the 2.2.x stream. In fact, TC-7999 has broader Affects Versions coverage than TC-8003, which only lists `RHTPA 2.2.0`.
- The version impact analysis confirms that only RHTPA 2.2.0 and 2.2.1 (plus 2.2.2 as a retag) are affected in this stream. Versions 2.2.3 and 2.2.4 already ship the fixed quinn-proto 0.11.14. TC-7999 already covers the affected versions.
- There is no value in keeping TC-8003 open -- it duplicates the tracking and remediation already underway in TC-7999.

### Recommendation

**Close TC-8003 as Duplicate of TC-7999.**

Proposed Jira actions (require engineer confirmation):
1. Add comment to TC-8003: "Duplicate of TC-7999 -- same CVE (CVE-2026-31812) tracked for the same stream [rhtpa-2.2]. TC-7999 is already In Progress with Affects Versions [RHTPA 2.2.0, RHTPA 2.2.1]. Version impact analysis confirms overlap."
2. Transition TC-8003 to Closed with resolution "Duplicate".
3. Assign TC-8003 to the current user.

### Affects Versions Note

TC-7999 already carries `RHTPA 2.2.0, RHTPA 2.2.1` as Affects Versions, which correctly covers the affected versions in the 2.2.x stream. TC-8003 only had `RHTPA 2.2.0` -- this gap is moot since TC-8003 will be closed as a duplicate, and TC-7999 already has the correct coverage.
