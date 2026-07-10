# Step 7 -- Concurrent Triage Detection for TC-8020

## Prerequisite Check

The Upstream Affected Component custom field (`customfield_10632`) is configured in Security Configuration. The current issue TC-8020 has `customfield_10632` set to `quinn-proto`. Proceeding with concurrent triage detection.

## JQL Search

Query executed (simulated):

```
project = TC
  AND issuetype = 10024
  AND cf[10632] ~ 'quinn-proto'
  AND status IN ('In Progress', 'Code Review')
  AND key != TC-8020
```

## Search Results

The JQL search returned **one result**:

| CVE Issue | Status | Assignee |
|-----------|--------|----------|
| TC-8019 | In Progress | engineer-b@example.com |

## Analysis

A concurrent triage has been detected. TC-8019 is actively being triaged by `engineer-b@example.com` and affects the same upstream component (`quinn-proto`). This means another engineer is currently working on a different CVE that also involves the quinn-proto library.

### Risk Assessment

Creating remediation tasks now could produce **duplicate remediation tasks** if both triages reach Step 8 independently. Specifically:

1. **TC-8019** (In Progress) may create its own remediation tasks to bump quinn-proto to a fixed version.
2. **TC-8020** (this triage) would also create remediation tasks to bump quinn-proto to >= 0.11.14.
3. If TC-8019's remediation already bumps quinn-proto to >= 0.11.14, the tasks would overlap -- a single dependency bump covers both CVEs.

### Recommended Action

Present the following options to the engineer:

```
Warning: Concurrent triage detected on the same upstream component (quinn-proto):

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

### Option Details

- **Option 1 (Wait)**: Stop execution and inform the user to re-run triage after TC-8019's triage completes. This is the safest option to avoid duplicate work. Once TC-8019 completes, re-running this triage would allow Step 4.3 (Cross-CVE Overlap Detection) to detect whether TC-8019's remediation already covers CVE-2026-31812's fix threshold (quinn-proto >= 0.11.14).

- **Option 2 (Skip)**: Skip Step 8 entirely (do not create remediation tasks) and add a Jira comment explaining why task creation was skipped. Use this if the engineer determines TC-8019's fix will cover this CVE.

- **Option 3 (Proceed)**: Add the `concurrent-triage-overlap` label to TC-8020 and continue to Case A/B/C branching. The label ensures that when TC-8019's triage reaches Step 4.3, the cross-CVE overlap detection picks up TC-8020 and avoids creating additional duplicate tasks. This option is appropriate when the engineer wants to proceed despite the overlap risk, relying on the label-based deduplication mechanism.

## Conclusion

Concurrent triage is confirmed. The engineer must choose one of the three options before triage can proceed to remediation (Case A/B/C branching in Step 8). No Jira mutations should occur until the engineer responds.
