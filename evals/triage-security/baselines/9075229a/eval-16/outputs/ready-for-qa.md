# Ready for QA — Filtering Analysis

## Overview

This analysis evaluates triaged Vulnerability issues to identify those with all remediation tasks completed, making them candidates for ON_QA transition.

**Query**: `project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status NOT IN (Closed, Verified, 'ON_QA') ORDER BY created DESC`

**Candidates evaluated**: 3
**Qualified for Ready for QA**: 1

---

## Filtering Criteria

For each candidate issue, inspect `issuelinks` for linked Tasks with link type "Depend":

1. **ALL linked remediation Tasks are Done or Closed** --> include in "Ready for QA" list
2. **ANY linked Task is still open** --> exclude (remediation still in progress)
3. **NO linked Tasks with type "Depend" exist** --> exclude (no remediation to verify)

---

## Issue-by-Issue Analysis

### TC-9020 — CVE-2026-38901 hyper - HTTP request smuggling [rhtpa-2.2]

- **Status**: Modified
- **CVE**: CVE-2026-38901
- **Created**: 2026-05-15
- **Depend links found**: 2

| Linked Task | Type | Status | Completed? |
|-------------|------|--------|------------|
| TC-9021 | Task | Done | Yes |
| TC-9022 | Task | Closed | Yes |

**Result: QUALIFIED -- Ready for QA**

All 2 linked remediation Tasks are in a terminal state (Done or Closed). This CVE has completed remediation and is a candidate for ON_QA transition.

**Recommendation**: Consider transitioning TC-9020 to ON_QA.

---

### TC-9023 — CVE-2026-39102 rustls - Certificate validation bypass [rhtpa-2.1]

- **Status**: In Progress
- **CVE**: CVE-2026-39102
- **Created**: 2026-05-10
- **Depend links found**: 2

| Linked Task | Type | Status | Completed? |
|-------------|------|--------|------------|
| TC-9024 | Task | Done | Yes |
| TC-9025 | Task | In Progress | No |

**Result: EXCLUDED -- Remediation in progress**

TC-9025 is still In Progress. 1 of 2 linked remediation Tasks remains open. This CVE cannot move to ON_QA until all remediation work is complete.

---

### TC-9026 — CVE-2026-39330 openssl - Buffer overflow in X.509 parsing [rhtpa-2.2]

- **Status**: Modified
- **CVE**: CVE-2026-39330
- **Created**: 2026-05-05
- **Depend links found**: 0

**Result: EXCLUDED -- No remediation to verify**

No linked Tasks with link type "Depend" were found. Without remediation tasks to verify, this issue cannot be moved to ON_QA. This may indicate that remediation tasks were not created, were unlinked, or that the issue was resolved through other means.

---

## Summary

| Issue | CVE | Status | Depend Links | All Complete? | Ready for QA? |
|-------|-----|--------|--------------|---------------|---------------|
| TC-9020 | CVE-2026-38901 | Modified | TC-9021 (Done), TC-9022 (Closed) | Yes | Yes |
| TC-9023 | CVE-2026-39102 | In Progress | TC-9024 (Done), TC-9025 (In Progress) | No | No |
| TC-9026 | CVE-2026-39330 | Modified | (none) | N/A | No |
