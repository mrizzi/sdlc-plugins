# Triage Outcome for TC-8002 (CVE-2026-28940)

## Step 3 -- Affects Versions Correction

### Current state

- PSIRT-assigned Affects Versions: **RHTPA 2.2.0**
- Issue stream scope: **2.2.x** (from summary suffix `[rhtpa-2.2]`)

### Analysis

The version impact table shows that **no versions in the 2.2.x stream are affected**.
All 2.2.x versions ship serde_json >= 1.0.138, which is above the fix threshold of
1.0.135. The PSIRT-assigned Affects Version of RHTPA 2.2.0 is incorrect -- version
2.2.0 ships serde_json 1.0.138, which is not vulnerable.

Since the triage outcome is Case C (close as Not a Bug), the Affects Versions
correction is subsumed by the close action. The close comment will document that
no versions are affected.

### PROPOSED Jira mutation

No Affects Versions update needed -- the issue will be closed as Not a Bug (see below).

## Step 4 -- Duplicate, Sibling, Overlap, and Reconciliation Check

### 4.1-4.2 -- Sibling search

PROPOSED JQL query (not executed in eval mode):
```
project = TC AND labels = 'CVE-2026-28940' AND issuetype = 10024 AND key != TC-8002
```

Would search for sibling Vulnerability issues with the same CVE label in different
streams. Since this issue is being closed as Not a Bug, sibling detection is
informational only.

### 4.3 -- Cross-CVE overlap detection

Skipped -- Upstream Affected Component custom field is not configured in Security
Configuration.

### 4.4 -- Preemptive task reconciliation

PROPOSED JQL query (not executed in eval mode):
```
project = TC AND issuetype = Task AND labels = 'security-preemptive' AND labels = 'CVE-2026-28940' ORDER BY created DESC
```

Would search for preemptive remediation tasks. Since no versions are affected,
any preemptive tasks found would also be candidates for closure.

## Step 5 -- Version Lifecycle Check

PROPOSED action (not executed in eval mode):
Would fetch https://access.example.com/product-life-cycle/rhtpa to verify lifecycle
status of affected versions. Since no versions are affected (Case C), lifecycle
status does not change the outcome.

## Step 6 -- Already Fixed Check

Not applicable in the traditional sense. The vulnerability was never present in any
shipped version -- all versions already ship serde_json >= 1.0.135. This is distinct
from "already fixed by a sibling issue" (Step 6's usual scenario). The correct
classification is Case C (not affected), not "already fixed."

## Step 7 -- Concurrent Triage Detection

Skipped -- Upstream Affected Component custom field is not configured in Security
Configuration.

## Step 8 -- Remediation Decision

### Determination: Case C -- No supported versions affected

The version impact table conclusively shows that **no supported version** ships a
vulnerable version of serde_json:

| Version | serde_json | Affected? |
|---------|------------|-----------|
| 2.1.0 | 1.0.137 | NO |
| 2.1.1 | 1.0.137 | NO |
| 2.2.0 | 1.0.138 | NO |
| 2.2.1 | 1.0.138 | NO |
| 2.2.2 | -- | NO (retag of 2.2.1) |
| 2.2.3 | 1.0.139 | NO |
| 2.2.4 | 1.0.139 | NO |

All shipped versions include serde_json >= 1.0.137, which is above the fix threshold
of 1.0.135. The stack overflow vulnerability (fixed by introducing a configurable
recursion limit in 1.0.135) does not affect any supported product version.

**Recommendation: Close TC-8002 as Not a Bug (not affected).**

### VEX Justification

VEX Justification custom field (customfield_12345) is configured.

Proposed VEX value: **Component not Present**

Rationale: The vulnerable package version (serde_json < 1.0.135) is not included in
any supported product version. All shipped versions contain serde_json >= 1.0.137,
which is outside the affected range.

---

## PROPOSED Jira Mutations

All mutations below require engineer confirmation before execution.

### 1. Add triage comment to TC-8002

PROPOSED comment:
```
No supported versions ship a vulnerable version of serde_json.

Version impact analysis for CVE-2026-28940 (serde_json < 1.0.135):

| Version | serde_json | Affected? | Notes |
|---------|------------|-----------|-------|
| 2.1.0   | 1.0.137    | NO        | ships patched version |
| 2.1.1   | 1.0.137    | NO        | ships patched version |
| 2.2.0   | 1.0.138    | NO        | ships patched version |
| 2.2.1   | 1.0.138    | NO        | ships patched version |
| 2.2.2   | --         | NO        | retag of 2.2.1 |
| 2.2.3   | 1.0.139    | NO        | ships patched version |
| 2.2.4   | 1.0.139    | NO        | ships patched version |

All supported versions ship serde_json >= 1.0.137, which is outside the
affected range (< 1.0.135). The fix (configurable recursion limit) was
already present before any supported version was built.

Closing as Not a Bug -- not affected.

@<reporter-account-id> (reporter mention)

[Comment Footnote: triage-security]
```

### 2. Set VEX Justification field

PROPOSED mutation:
```
jira.edit_issue("TC-8002", fields={
  "customfield_12345": "Component not Present"
})
```

Rationale: The vulnerable version of serde_json (< 1.0.135) is not present in any
supported product version.

### 3. Transition TC-8002 to Closed

PROPOSED mutation:
```
jira.transition_issue("TC-8002", transition_id=<close-transition-id>,
  resolution="Not a Bug")
```

Resolution: **Not a Bug** (product does not ship the vulnerable version)

### 4. Add ai-cve-triaged label

PROPOSED mutation:
```
jira.edit_issue("TC-8002", fields={
  "labels": ["CVE-2026-28940", "pscomponent:org/rhtpa-server", "ai-cve-triaged"]
})
```

### 5. No remediation tasks created

Since no supported versions are affected (Case C), no remediation Tasks are created.
No upstream backport task. No downstream propagation task.

---

## Summary

| Aspect | Detail |
|--------|--------|
| Issue | TC-8002 |
| CVE | CVE-2026-28940 |
| Library | serde_json |
| Affected range | < 1.0.135 |
| Fix threshold | 1.0.135 |
| Versions checked | 7 (2.1.0, 2.1.1, 2.2.0, 2.2.1, 2.2.2, 2.2.3, 2.2.4) |
| Versions affected | 0 |
| Triage outcome | Case C -- Close as Not a Bug |
| VEX Justification | Component not Present |
| Remediation tasks | None |
| Reason | All shipped versions include serde_json >= 1.0.137, already above the fix threshold |
