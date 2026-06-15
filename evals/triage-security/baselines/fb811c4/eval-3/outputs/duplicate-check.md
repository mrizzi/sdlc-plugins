# Duplicate Check — TC-8003

## JQL Search for Sibling Issues

To find sibling issues tracking the same CVE, the following JQL query was executed:

```
project = TC AND labels = "CVE-2026-31812" AND key != TC-8003
```

This searches for all issues in the TC project that carry the CVE-2026-31812 label, excluding the current issue (TC-8003).

## Search Results

| Issue Key | Summary | Status | Labels | Affects Versions | Stream Suffix |
|-----------|---------|--------|--------|-------------------|---------------|
| TC-7999 | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] | In Progress | CVE-2026-31812, pscomponent:org/rhtpa-server | RHTPA 2.2.0, RHTPA 2.2.1 | [rhtpa-2.2] |

**1 sibling issue found.**

## Stream Comparison

| Field | TC-8003 (current) | TC-7999 (sibling) |
|-------|--------------------|--------------------|
| CVE | CVE-2026-31812 | CVE-2026-31812 |
| Stream suffix | [rhtpa-2.2] | [rhtpa-2.2] |
| Mapped stream | 2.2.x | 2.2.x |
| Status | New | In Progress |
| Affects Versions | RHTPA 2.2.0 | RHTPA 2.2.0, RHTPA 2.2.1 |

## Classification

**TC-7999 is a same-stream sibling.** Both TC-8003 and TC-7999 share:

- The same CVE identifier: **CVE-2026-31812**
- The same stream suffix: **[rhtpa-2.2]** (mapping to the 2.2.x version stream)

This means both issues are tracking the same vulnerability (CVE-2026-31812 in quinn-proto) for the same product stream (2.2.x). They are duplicates.

## Conclusion

**TC-8003 is a duplicate of TC-7999.**

TC-7999 is the original issue and is already in **In Progress** status, meaning remediation work is already underway. TC-7999 also has broader version coverage (RHTPA 2.2.0 and RHTPA 2.2.1) compared to TC-8003 (RHTPA 2.2.0 only).

The duplicate detection short-circuits further triage processing. No remediation tasks, version exposure analysis, or fix verification steps will be performed for TC-8003.
