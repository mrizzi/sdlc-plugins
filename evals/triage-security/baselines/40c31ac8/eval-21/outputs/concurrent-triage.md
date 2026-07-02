# Step 7 -- Concurrent Triage Detection for TC-8020

## Prerequisite Check

- Upstream Affected Component custom field: **configured** (customfield_10632)
- Current issue's Upstream Affected Component value: **quinn-proto**
- Field is populated: **yes**

Step 7 proceeds.

## JQL Search

Query executed:

```
project = TC
  AND issuetype = 10024
  AND cf[10632] ~ 'quinn-proto'
  AND status IN ('In Progress', 'Code Review')
  AND key != TC-8020
```

## Search Results

The JQL search returned **1 result**:

| CVE Issue | Status | Assignee |
|-----------|--------|----------|
| TC-8019 | In Progress | engineer-b@example.com |

## WARNING: Concurrent Triage Detected

**WARNING** -- Concurrent triage detected on the same upstream component (quinn-proto):

| CVE Issue | Status | Assignee |
|-----------|--------|----------|
| TC-8019 | In Progress | engineer-b@example.com |

Another engineer is actively triaging a related CVE that affects the same upstream component (`quinn-proto`). Creating remediation tasks now may produce duplicates if TC-8019's triage also reaches Step 8 and creates tasks that bump quinn-proto.

## Options Presented to Engineer

1. **Wait** -- Pause triage until TC-8019's triage completes, then re-run from Step 4.3 to detect any overlap from TC-8019's remediation tasks. This is the safest option to avoid duplicate work.

2. **Skip remediation task creation** -- Complete the triage analysis (Steps 1-6 results are retained) but skip Step 8 entirely. No remediation tasks will be created. A Jira comment will be added to TC-8020 explaining that task creation was skipped due to concurrent triage on the same component (TC-8019).

3. **Proceed with `concurrent-triage-overlap` label** -- Create remediation tasks as normal, but add the `concurrent-triage-overlap` label to TC-8020. This label ensures that when TC-8019's triage reaches Step 4.3 (cross-CVE overlap detection), it will detect TC-8020's remediation tasks and can reconcile any overlap.

## Execution Note

Step 7 runs **before** Case A/B/C branching in Step 8. The engineer must choose one of the three options above before the triage proceeds to determine the remediation outcome (Case A: create tasks, Case B: cross-stream impact, or Case C: close as not affected).

No Jira mutations occur at this step -- the warning is purely informational until the engineer makes a selection.
