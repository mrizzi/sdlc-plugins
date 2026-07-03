# Triage Outcome for TC-8003

## Decision: Close as Duplicate

TC-8003 is a **same-stream duplicate** of TC-7999 and should be closed.

## Rationale

TC-8003 (CVE-2026-31812 quinn-proto [rhtpa-2.2]) is a duplicate of TC-7999, which
tracks the identical CVE for the identical stream:

| Criterion | TC-7999 (original) | TC-8003 (duplicate) |
|-----------|--------------------|--------------------|
| CVE | CVE-2026-31812 | CVE-2026-31812 |
| Library | quinn-proto | quinn-proto |
| Stream suffix | [rhtpa-2.2] | [rhtpa-2.2] |
| Stream | 2.2.x | 2.2.x |
| Status | In Progress | New |
| Affects Versions | RHTPA 2.2.0, RHTPA 2.2.1 | RHTPA 2.2.0 |

TC-7999 is already **In Progress**, meaning an engineer is actively triaging or
remediating it. TC-7999 also has broader Affects Versions coverage (RHTPA 2.2.0
and RHTPA 2.2.1) compared to TC-8003 (RHTPA 2.2.0 only).

Per the triage-security skill Step 4.1 procedure: when a same-stream sibling
exists and is open or in progress, the recommendation is to close the current
issue as Duplicate.

## Proposed Jira Mutations

All mutations require explicit engineer confirmation before execution.

### 1. Comment on TC-8003

Post a comment documenting the duplicate finding:

> Duplicate of TC-7999 -- same CVE tracked for the same stream [rhtpa-2.2].
> Version impact analysis confirms overlap.
>
> [Comment Footnote per shared/comment-footnote.md, skill: triage-security]

### 2. Close TC-8003

- Transition: **Closed**
- Resolution: **Duplicate**

### 3. Assign TC-8003

- Assign to current user

### 4. Add ai-cve-triaged label

- Add label `ai-cve-triaged` to TC-8003 to mark it as triaged

## Steps Skipped

Because the issue is identified as a same-stream duplicate in Step 4.1, the
following steps are short-circuited and not executed:

- **Step 2 (Version Impact Analysis)** -- not needed; the original issue TC-7999
  already covers this analysis
- **Step 3 (Affects Versions Correction)** -- not needed; the issue will be closed
- **Step 4.2 (Cross-stream coordination)** -- not applicable (same-stream duplicate)
- **Step 4.3 (Cross-CVE overlap detection)** -- not applicable (issue being closed)
- **Step 4.4 (Preemptive task reconciliation)** -- not applicable (issue being closed)
- **Step 5 (Version Lifecycle Check)** -- not needed; the issue will be closed
- **Step 6 (Already Fixed Check)** -- not needed; the issue will be closed
- **Step 7 (Concurrent Triage Detection)** -- not needed; no remediation tasks to create
- **Step 8 (Remediation)** -- not needed; no remediation tasks to create

## Summary

TC-8003 is a duplicate of TC-7999. Both issues track CVE-2026-31812 (quinn-proto,
versions before 0.11.14) for the same stream 2.2.x. TC-7999 is already In Progress
with correct Affects Versions coverage. The recommended action is to close TC-8003
as Duplicate, assign to the current user, and add the ai-cve-triaged label.
