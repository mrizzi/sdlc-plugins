# Duplicate Analysis — Step 4

## JQL Query

```
project = TC AND labels = 'CVE-2026-31812' AND issuetype = 10024 AND key != TC-8003
```

Note: The query excludes the current issue key TC-8003 to find only sibling issues tracking the same CVE.

## Sibling Found

- **TC-7999** — CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2]
  - **Status**: In Progress
  - **Stream suffix**: [rhtpa-2.2] (same as TC-8003)
  - **Affects Versions**: RHTPA 2.2.0, RHTPA 2.2.1

## Classification

**Same-stream sibling** — both TC-8003 and TC-7999 have the stream suffix [rhtpa-2.2], meaning they track the same CVE (CVE-2026-31812) for the same product version stream (2.2.x).

## Recommendation

TC-8003 is a **duplicate** of TC-7999 (Step 4.1).

TC-7999 is already In Progress, so it is the primary tracker for CVE-2026-31812 in the 2.2.x stream. There is no need for a second issue tracking the same vulnerability in the same stream. TC-8003 should be closed as a duplicate.
