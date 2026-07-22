# Triage Outcome -- TC-8003

## Decision: Close as Duplicate

TC-8003 is a **duplicate** of TC-7999. Both issues track the same CVE (CVE-2026-31812) for the same stream ([rhtpa-2.2] / 2.2.x), and TC-7999 is already In Progress with the correct Affects Versions (RHTPA 2.2.0, RHTPA 2.2.1).

## Rationale

Per Step 4.1 of the triage-security skill, when a same-stream sibling exists and is open or in progress, the current issue should be closed as Duplicate.

Key facts:
1. **Same CVE**: Both TC-8003 and TC-7999 track CVE-2026-31812 (quinn-proto panic on large stream counts).
2. **Same stream**: Both have the `[rhtpa-2.2]` stream suffix, mapping to the 2.2.x version stream.
3. **TC-7999 is already In Progress**: Active triage/remediation is underway on the existing issue.
4. **TC-7999 has broader Affects Versions**: TC-7999 covers RHTPA 2.2.0 and RHTPA 2.2.1, while TC-8003 only has RHTPA 2.2.0. The existing issue already has the more complete version coverage.

## Proposed Jira Actions

The following actions would be performed after engineer confirmation:

### 1. Add comment to TC-8003

```
Duplicate of TC-7999 -- same CVE (CVE-2026-31812) tracked for the same
stream [rhtpa-2.2]. Version impact analysis confirms overlap.

TC-7999 is In Progress with Affects Versions [RHTPA 2.2.0, RHTPA 2.2.1],
which already covers the full set of affected versions in the 2.2.x stream.

[Comment Footnote]
```

### 2. Transition TC-8003 to Closed

- Resolution: **Duplicate**
- Link TC-8003 to TC-7999 as a duplicate

### 3. Add ai-cve-triaged label

Add the `ai-cve-triaged` label to TC-8003 to mark it as triaged.

## Steps Not Executed

Because TC-8003 is a duplicate, the following steps are skipped:

- **Step 3 (Affects Versions Correction)**: Not needed -- the issue is being closed. TC-7999 already has the correct Affects Versions.
- **Step 5 (Version Lifecycle Check)**: Not needed -- lifecycle is checked on the active issue (TC-7999).
- **Step 6 (Already Fixed Check)**: Not needed -- the issue is being closed as duplicate, not as already fixed.
- **Step 7 (Concurrent Triage Detection)**: Not needed -- no remediation tasks will be created from this issue.
- **Step 8 (Remediation)**: Not needed -- remediation is handled by TC-7999.

## Version Impact Summary (for reference)

Although the issue is a duplicate, the version impact analysis was completed for context:

| Version | quinn-proto | Affected? | Notes |
|---------|-------------|-----------|-------|
| 2.2.0 | 0.11.9 | YES | |
| 2.2.1 | 0.11.12 | YES | |
| 2.2.2 | -- | YES | retag of 2.2.1 |
| 2.2.3 | 0.11.14 | NO | Fixed |
| 2.2.4 | 0.11.14 | NO | Fixed |

The fix was introduced in version 2.2.3 (tag v0.4.11), which ships quinn-proto 0.11.14 (the fix threshold).
