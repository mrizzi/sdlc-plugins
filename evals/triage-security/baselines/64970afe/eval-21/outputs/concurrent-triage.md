# Step 7 -- Concurrent Triage Detection for TC-8020

## Prerequisite Check

The Upstream Affected Component custom field (customfield_10632) is configured in Security Configuration. The current issue TC-8020 has this field set to `quinn-proto`. Proceeding with concurrent triage detection.

## JQL Search

Query executed:

```
project = TC
  AND issuetype = 10024
  AND cf[10632] ~ 'quinn-proto'
  AND status IN ('In Progress', 'Code Review')
  AND key != TC-8020
```

## Results

The search returned **1 result**:

| CVE Issue | Status | Assignee |
|-----------|--------|----------|
| TC-8019 | In Progress | engineer-b@example.com |

## Analysis

Concurrent triage detected on the same upstream component (quinn-proto). Another engineer (engineer-b@example.com) is actively triaging TC-8019, which also affects the quinn-proto component. Both TC-8019 and TC-8020 target the same upstream library.

Creating remediation tasks now risks producing duplicate tasks if both triages independently create upstream backport and downstream propagation tasks for quinn-proto in overlapping streams.

## Warning Presented to Engineer

```
Concurrent triage detected on the same upstream component (quinn-proto):

| CVE Issue | Status      | Assignee                  |
|-----------|-------------|---------------------------|
| TC-8019   | In Progress | engineer-b@example.com    |

Another engineer is actively triaging a related CVE. Creating remediation
tasks now may produce duplicates.

Options:
1. Wait -- pause until the other triage completes, then re-run Step 4.3
   to detect any overlap
2. Skip -- skip remediation task creation for this CVE
3. Proceed -- create tasks anyway with a `concurrent-triage-overlap` label
   so the other engineer's Step 4.3 catches the overlap
```

## Recommended Action

**Option 3 (Proceed)** is recommended in this case because:

1. TC-8020 has a due date of 2026-07-15, which is imminent -- waiting could delay remediation past the deadline.
2. The `concurrent-triage-overlap` label provides a safety net: when TC-8019's triage reaches Step 4.3 (cross-CVE overlap detection), it will detect TC-8020's remediation tasks and avoid creating duplicates.
3. If the engineer selects Proceed, the `concurrent-triage-overlap` label will be added to TC-8020 before continuing to Case A/B/C branching.

## Outcome

The engineer must choose one of the three options before the triage can proceed to Step 8 (Remediation). No remediation tasks are created until the concurrent triage concern is resolved.

- If **Wait**: execution stops; the engineer should re-run triage after TC-8019 completes.
- If **Skip**: Step 8 is skipped entirely; a Jira comment is posted explaining why task creation was skipped.
- If **Proceed**: the `concurrent-triage-overlap` label is added to TC-8020, and triage continues to Case A/B/C branching.
