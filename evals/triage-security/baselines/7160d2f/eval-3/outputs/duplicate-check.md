# Duplicate Check: TC-8003

## Search Strategy

Searched for sibling Vulnerability issues sharing the same CVE label, excluding the current issue:

**JQL:** `project = TC AND issuetype = 10024 AND labels = "CVE-2026-31812" AND key != TC-8003`

## Search Results

| Field | TC-8003 (current) | TC-7999 (sibling) |
|---|---|---|
| CVE | CVE-2026-31812 | CVE-2026-31812 |
| Status | New | In Progress |
| Stream suffix | [rhtpa-2.2] | [rhtpa-2.2] |
| Labels | CVE-2026-31812, pscomponent:org/rhtpa-server | CVE-2026-31812, pscomponent:org/rhtpa-server |
| Affects Versions | RHTPA 2.2.0 | RHTPA 2.2.0, RHTPA 2.2.1 |

## Duplicate Analysis

### Same CVE?

Yes. Both TC-8003 and TC-7999 carry the label `CVE-2026-31812`.

### Same stream?

Yes. Both issues have the stream suffix `[rhtpa-2.2]`, indicating they target the same product stream.

### Version coverage

TC-7999 has a **superset** of the Affects Versions from TC-8003:
- TC-8003 affects: RHTPA 2.2.0
- TC-7999 affects: RHTPA 2.2.0, RHTPA 2.2.1

TC-7999 already covers all versions listed in TC-8003, plus an additional version (RHTPA 2.2.1).

### Status comparison

TC-7999 is already **In Progress**, meaning remediation work has begun. TC-8003 is still in **New** status with no assignee.

## Conclusion

**TC-8003 is a same-stream duplicate of TC-7999.**

Both issues track the identical CVE (CVE-2026-31812) for the identical product stream ([rhtpa-2.2]). The existing issue TC-7999 is further along in the workflow (In Progress) and covers a broader set of affected versions. There is no reason to maintain a second tracking issue for this CVE in this stream.

**Recommendation:** Close TC-8003 as Duplicate of TC-7999. Do NOT proceed to remediation task creation -- duplicate detection short-circuits the triage flow.
