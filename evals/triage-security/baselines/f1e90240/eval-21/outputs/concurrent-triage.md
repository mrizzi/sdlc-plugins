# Step 7 -- Concurrent Triage Detection for TC-8020

## Configuration

The Upstream Affected Component custom field is configured as `customfield_10632` in Security Configuration. The current issue (TC-8020) has this field set to `quinn-proto`.

## JQL Query

The following JQL query was executed to detect concurrent triages on the same upstream component:

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

Concurrent triage detected on the same upstream component (`quinn-proto`).

Another engineer (`engineer-b@example.com`) is actively triaging a related CVE (TC-8019) that affects the same upstream component `quinn-proto`. TC-8019 is currently in **In Progress** status, meaning that engineer is likely in the middle of their triage workflow (potentially at or near Step 8 remediation task creation).

Creating remediation tasks for TC-8020 now risks producing duplicate tasks if both triages independently create tasks to bump `quinn-proto` to a fixed version. The existing triage on TC-8019 may already be creating (or have created) remediation tasks that cover the same library bump.

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

## Recommendation

**Option 1 (Wait)** is the recommended choice. Since TC-8019 is already In Progress on the same component (`quinn-proto`), waiting for that triage to complete avoids creating duplicate remediation tasks. Once TC-8019's triage finishes and its remediation tasks are created, re-running Step 4.3 (Cross-CVE Overlap Detection) for TC-8020 will detect whether TC-8019's remediation already covers the fix threshold for CVE-2026-31812 (quinn-proto >= 0.11.14). If it does, TC-8020 can be resolved without creating redundant tasks.

If the engineer chooses **Option 3 (Proceed)**, the `concurrent-triage-overlap` label will be added to TC-8020 so that when TC-8019's triage reaches its own Step 4.3, the overlap will be detected and reconciled.

## Impact on Triage Flow

- If **Wait**: Stop execution. Inform engineer to re-run `/sdlc-workflow:triage-security TC-8020` after TC-8019 triage completes.
- If **Skip**: Skip Step 8 entirely (no remediation tasks created). Add a Jira comment explaining that task creation was skipped due to concurrent triage on TC-8019.
- If **Proceed**: Add `concurrent-triage-overlap` label to TC-8020 and continue to Case A/B/C branching for remediation task creation.
