# Step 7 -- Concurrent Triage Detection for TC-8020

## Prerequisites

- Upstream Affected Component custom field: **configured** (customfield_10632)
- Current issue's Upstream Affected Component value: **quinn-proto**
- Step 7 runs BEFORE Case A/B/C branching in Step 8

Since the Upstream Affected Component custom field is configured and populated, Step 7 proceeds (not skipped).

## JQL Search

The following JQL query was executed to detect in-progress triages on the same upstream component:

```
project = TC
  AND issuetype = 10024
  AND cf[10632] ~ 'quinn-proto'
  AND status IN ('In Progress', 'Code Review')
  AND key != TC-8020
```

Fields requested: summary, status, labels, assignee

## Search Results

The search returned **1 result**:

| CVE Issue | Status | Assignee |
|-----------|--------|----------|
| TC-8019 | In Progress | engineer-b@example.com |

## Concurrent Triage Warning

A concurrent triage was detected. Another engineer (engineer-b@example.com) is actively triaging TC-8019, which affects the same upstream component (quinn-proto). Creating remediation tasks now may produce duplicates if both triages reach Step 8 simultaneously.

The following warning is presented to the engineer:

> **Concurrent triage detected** on the same upstream component (quinn-proto):
>
> | CVE Issue | Status | Assignee |
> |-----------|--------|----------|
> | TC-8019 | In Progress | engineer-b@example.com |
>
> Another engineer is actively triaging a related CVE. Creating remediation
> tasks now may produce duplicates.
>
> Options:
> 1. **Wait** -- pause until the other triage completes, then re-run Step 4.3
>    to detect any overlap
> 2. **Skip** -- skip remediation task creation for this CVE
> 3. **Proceed** -- create tasks anyway with a `concurrent-triage-overlap` label
>    so the other engineer's Step 4.3 catches the overlap

## Option Details

### Option 1: Wait
Stop execution and inform the user to re-run triage after TC-8019's triage completes. When re-run, Step 4.3 (cross-CVE overlap detection) will detect whether TC-8019's remediation already covers CVE-2026-31812's fix threshold (quinn-proto >= 0.11.14), potentially eliminating the need for a new remediation task.

### Option 2: Skip
Skip Step 8 entirely -- do not create remediation tasks. A Jira comment is added to TC-8020 explaining why task creation was skipped:

> "Remediation task creation skipped due to concurrent triage on the same upstream component (quinn-proto). TC-8019 is currently In Progress, assigned to engineer-b@example.com. Re-run triage after TC-8019 completes to check for cross-CVE overlap."

### Option 3: Proceed
Add the `concurrent-triage-overlap` label to TC-8020 and continue to Case A/B/C branching. The label ensures that when TC-8019's triage reaches Step 4.3, the cross-CVE overlap detection will find TC-8020 and check whether its remediation covers TC-8019 (or vice versa). This prevents silent duplication while still allowing both triages to move forward.

## Sequence in Triage Flow

Step 7 executes after Steps 3-6 (Affects Versions correction, duplicate/sibling/overlap check, lifecycle check, already-fixed check) and before Step 8 (Remediation Case A/B/C branching). The triage does not proceed to create remediation tasks until the engineer selects one of the three options above.
