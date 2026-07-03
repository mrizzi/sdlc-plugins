# Step 7 -- Concurrent Triage Detection for TC-8020

## Prerequisite Check

- **Upstream Affected Component custom field**: Configured (customfield_10632)
- **Field value on TC-8020**: quinn-proto
- **Result**: Field is configured and populated. Proceeding with concurrent triage detection.

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

## Concurrent Triage Warning

A concurrent triage has been detected on the same upstream component (quinn-proto):

```
Concurrent triage detected on the same upstream component (quinn-proto):

| CVE Issue | Status      | Assignee                |
|-----------|-------------|-------------------------|
| TC-8019   | In Progress | engineer-b@example.com  |

Another engineer is actively triaging a related CVE. Creating remediation
tasks now may produce duplicates.

Options:
1. Wait -- pause until the other triage completes, then re-run Step 4.3
   to detect any overlap
2. Skip -- skip remediation task creation for this CVE
3. Proceed -- create tasks anyway with a `concurrent-triage-overlap` label
   so the other engineer's Step 4.3 catches the overlap
```

## Analysis

TC-8019 is currently In Progress, meaning engineer-b@example.com is actively triaging a different CVE that also affects the quinn-proto upstream component. Both TC-8019 and TC-8020 target the same library, so their remediation tasks could overlap -- if both triages independently create upstream backport tasks to bump quinn-proto, duplicate work would result.

### Risk Assessment

- **Component overlap**: Both issues affect quinn-proto in the same project
- **Active triage**: TC-8019 is In Progress (not just queued), indicating Step 8 remediation task creation may be imminent or already complete
- **Duplicate risk**: High -- if both triages create upstream backport tasks for quinn-proto, the same source repository branch would receive competing PRs

### Recommended Action

The engineer must choose one of the three options before Step 8 (Remediation) can proceed:

1. **Wait** (safest): Pause triage. After TC-8019's triage completes, re-run from Step 4.3 to check whether TC-8019's remediation already covers CVE-2026-31812's fix threshold (quinn-proto >= 0.11.14). If it does, TC-8020 can be closed via cross-CVE overlap (Step 4.3). If not, proceed with new remediation tasks.

2. **Skip**: Do not create remediation tasks. Add a Jira comment to TC-8020 documenting why task creation was skipped (concurrent triage on same component). The engineer can re-run triage later.

3. **Proceed**: Create remediation tasks with the `concurrent-triage-overlap` label added to TC-8020. This label ensures that when TC-8019's triage runs Step 4.3 (cross-CVE overlap detection), it will find TC-8020's remediation tasks and reconcile any overlap. This is appropriate when the engineer is confident the two CVEs require different fix thresholds or when urgency demands parallel work.

## Dependency on User Choice

Step 8 (Remediation) is blocked until the engineer selects an option. The triage analysis (Steps 1-6) is complete, but no remediation tasks will be created until the concurrent triage situation is resolved.
