# Step 7 -- Concurrent Triage Detection for TC-8020

## Configuration

The Upstream Affected Component custom field (`customfield_10632`) is configured in Security Configuration. This step is **not skipped**.

## Current Issue Component

- **Upstream Affected Component (customfield_10632)**: `quinn-proto`

## JQL Search Executed

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

## Analysis

Concurrent triage **detected**. Another engineer (`engineer-b@example.com`) is actively triaging TC-8019, which affects the same upstream component (`quinn-proto`). TC-8019 is currently `In Progress`, meaning that engineer is likely in the middle of their own triage workflow (Steps 1-8) and may be about to create remediation tasks for the same component.

Creating remediation tasks for TC-8020 now risks producing duplicate tasks if TC-8019's triage also reaches Step 8 and creates tasks that bump `quinn-proto` to a version that covers both CVEs.

## Warning Presented to Engineer

```
Warning: Concurrent triage detected on the same upstream component (quinn-proto):

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

**Option 1 (Wait)** is the safest choice. Since TC-8019 is already `In Progress` on the same component (`quinn-proto`), the engineer triaging TC-8019 may create remediation tasks that bump `quinn-proto` past both CVEs' fix thresholds. Waiting avoids duplicate task creation and allows Step 4.3 (cross-CVE overlap detection) to reconcile coverage when this triage resumes.

If waiting is not feasible (e.g., due to the due date of 2026-07-15), **Option 3 (Proceed)** is acceptable. The `concurrent-triage-overlap` label ensures the other engineer's Step 4.3 will detect the overlap and reconcile any duplicates.

**Option 2 (Skip)** should only be used if the engineer confirms that TC-8019's remediation will definitively cover TC-8020's fix threshold.

## Impact on Triage Flow

The engineer must choose one of the three options before the triage can continue to Case A/B/C branching in Step 8:

- **If Wait**: Stop execution. Inform the user to re-run after TC-8019's triage completes.
- **If Skip**: Skip Step 8 entirely. Post a Jira comment on TC-8020 explaining that remediation task creation was skipped pending TC-8019's completion.
- **If Proceed**: Add the `concurrent-triage-overlap` label to TC-8020 and continue to Step 8 (Case A for the 2.2.x stream, Case B for the 2.1.x cross-stream impact).
