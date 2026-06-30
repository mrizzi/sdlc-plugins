# Ready for QA — Detailed Filtering Analysis

## Overview

Query 3 searched for triaged Vulnerability issues (`ai-cve-triaged` label) that are not yet Closed, Verified, or ON_QA. The goal is to identify CVEs where all linked remediation Tasks are complete, making them candidates for ON_QA transition.

**JQL used:**
```
project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status NOT IN (Closed, Verified, 'ON_QA') ORDER BY created DESC
```

**Results returned:** 3 issues

---

## Filtering Criteria

For each candidate issue, inspect its `issuelinks` for links with type "Depend":

1. **ALL linked remediation Tasks are Done or Closed** --> Ready for QA
2. **ANY linked Task is still open** --> Excluded (remediation in progress)
3. **NO linked Tasks with type "Depend" exist** --> Excluded (no remediation to verify)

---

## Issue-by-Issue Analysis

### TC-9020 — CVE-2026-38901 hyper - HTTP request smuggling [rhtpa-2.2]

- **Status**: Modified
- **CVE**: CVE-2026-38901
- **Created**: 2026-05-15
- **Depend links**:
  - TC-9021 (Task) — Status: **Done**
  - TC-9022 (Task) — Status: **Closed**
- **Analysis**: Both linked remediation Tasks are in terminal states (Done and Closed). All remediation work for this CVE is complete.
- **Result**: **QUALIFIED — Ready for QA**
- **Recommendation**: Consider transitioning TC-9020 to ON_QA. All linked remediation tasks have been completed.

---

### TC-9023 — CVE-2026-39102 rustls - Certificate validation bypass [rhtpa-2.1]

- **Status**: In Progress
- **CVE**: CVE-2026-39102
- **Created**: 2026-05-10
- **Depend links**:
  - TC-9024 (Task) — Status: **Done**
  - TC-9025 (Task) — Status: **In Progress**
- **Analysis**: TC-9025 is still In Progress. Not all remediation Tasks are complete — at least one linked Task remains open.
- **Result**: **EXCLUDED — Remediation in progress**
- **Reason**: TC-9025 (Task) is still In Progress. This CVE cannot move to QA until all remediation work is finished.

---

### TC-9026 — CVE-2026-39330 openssl - Buffer overflow in X.509 parsing [rhtpa-2.2]

- **Status**: Modified
- **CVE**: CVE-2026-39330
- **Created**: 2026-05-05
- **Depend links**: (none)
- **Analysis**: This issue has no linked Tasks with link type "Depend". Without remediation tasks, there is nothing to verify in QA.
- **Result**: **EXCLUDED — No remediation to verify**
- **Reason**: No Depend-linked Tasks exist. This may indicate remediation tasks have not yet been created, or the issue was resolved through other means. Investigate whether remediation tasks need to be created.

---

## Summary

| Issue | CVE | Status | Depend Links | All Tasks Complete? | Ready for QA? |
|-------|-----|--------|--------------|---------------------|---------------|
| TC-9020 | CVE-2026-38901 | Modified | TC-9021 (Done), TC-9022 (Closed) | Yes | Yes |
| TC-9023 | CVE-2026-39102 | In Progress | TC-9024 (Done), TC-9025 (In Progress) | No | No — remediation in progress |
| TC-9026 | CVE-2026-39330 | Modified | (none) | N/A | No — no remediation to verify |

**Total candidates evaluated:** 3
**Qualified for QA:** 1 (TC-9020)
**Excluded:** 2 (TC-9023 — open task; TC-9026 — no Depend links)
