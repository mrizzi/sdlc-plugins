# Step 4: Duplicate / Sibling Check

## JQL Search

**Query**: `project = TC AND type = Vulnerability AND labels = "CVE-2026-31812" AND key != TC-8003`

**Result**: 1 issue found.

## Sibling Issue

| Field | TC-7999 (Sibling) | TC-8003 (Current) |
|-------|--------------------|--------------------|
| **Summary** | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] |
| **Status** | In Progress | New |
| **Labels** | CVE-2026-31812, pscomponent:org/rhtpa-server | CVE-2026-31812, pscomponent:org/rhtpa-server |
| **Affects Versions** | RHTPA 2.2.0, RHTPA 2.2.1 | RHTPA 2.2.0 |
| **Stream suffix** | [rhtpa-2.2] | [rhtpa-2.2] |

## Step 4.1: Same-Stream Duplicate Analysis

Both TC-8003 and TC-7999 share:

1. **Same CVE**: CVE-2026-31812
2. **Same stream suffix**: [rhtpa-2.2] -- both target the 2.2.x version stream
3. **Same component**: pscomponent:org/rhtpa-server
4. **Same library**: quinn-proto

TC-7999 is already **In Progress**, meaning triage and remediation work has already begun. TC-8003 is a **same-stream duplicate** of TC-7999.

Additionally, TC-7999 has broader version coverage (RHTPA 2.2.0 and RHTPA 2.2.1) compared to TC-8003 (RHTPA 2.2.0 only), making TC-7999 the more complete tracking issue.

## Conclusion

**TC-8003 is a same-stream duplicate of TC-7999.** The duplicate detection short-circuits further triage -- no remediation task creation or version-by-version analysis is needed.
