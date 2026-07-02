# Step 7 -- Concurrent Triage Detection

## Configuration

- Upstream Affected Component custom field: `customfield_10632` (configured in Security Configuration)
- Current issue: TC-8020
- Upstream Affected Component value: `quinn-proto`

## JQL Query

```
project = TC
  AND issuetype = 10024
  AND cf[10632] ~ 'quinn-proto'
  AND status IN ('In Progress', 'Code Review')
  AND key != TC-8020
```

## Results

The JQL search returned **1 result**:

| CVE Issue | Status | Assignee |
|-----------|--------|----------|
| TC-8019 | In Progress | engineer-b@example.com |

## Analysis

Concurrent triage detected on the same upstream component (`quinn-proto`). Another engineer (`engineer-b@example.com`) is actively triaging TC-8019, a different CVE that also affects `quinn-proto`. Both triages may produce remediation tasks that bump the same dependency, risking duplicate work.

## Warning Presented to Engineer

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

## Implications for Remediation

The engineer must choose one of three options before proceeding to Case A/B/C branching in Step 8:

1. **Wait**: Stop execution. The engineer re-runs triage after TC-8019 completes, allowing Step 4.3 cross-CVE overlap detection to check whether TC-8019's remediation already covers TC-8020's fix threshold (quinn-proto >= 0.11.14).

2. **Skip**: No remediation tasks are created for TC-8020. A Jira comment is added explaining that task creation was skipped due to concurrent triage on the same component.

3. **Proceed**: Remediation tasks are created with the `concurrent-triage-overlap` label added to TC-8020. This label ensures that when TC-8019's triage runs Step 4.3, it will detect the overlap and reconcile the remediation tasks.

The concurrent triage detection is particularly relevant here because both CVEs affect `quinn-proto`, and if TC-8019's remediation already bumps quinn-proto to or past 0.11.14, then TC-8020 would be covered without needing its own remediation tasks.
