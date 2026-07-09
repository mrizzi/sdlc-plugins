# Ready for QA — Filtering Analysis

## Overview

Query 3 searches for triaged Vulnerability issues that are not yet Closed, Verified, or ON_QA, then checks whether all linked remediation Tasks (link type "Depend") are completed.

**JQL used:**
```
project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status NOT IN (Closed, Verified, 'ON_QA') ORDER BY created DESC
```

**Results returned:** 3 issues

---

## Filtering Criteria

For each candidate issue, the following rules are applied to its `issuelinks`:

1. **ALL linked remediation Tasks (link type "Depend") are Done or Closed** -- include in Ready for QA list. These CVEs have completed remediation and are candidates for ON_QA transition.
2. **ANY linked Task is still open (not Done or Closed)** -- exclude. Remediation is still in progress.
3. **NO linked Tasks with link type "Depend" exist** -- exclude. No remediation to verify.

---

## Per-Issue Analysis

### TC-9020 — CVE-2026-38901 hyper - HTTP request smuggling [rhtpa-2.2]

- **Status:** Modified
- **Created:** 2026-05-15

**Linked remediation Tasks (Depend):**

| Linked Task | Type | Status | Completed? |
|-------------|------|--------|------------|
| TC-9021 | Task | Done | Yes |
| TC-9022 | Task | Closed | Yes |

**Result: QUALIFIED -- Ready for QA**

All 2 linked remediation Tasks are in a completed state (Done or Closed). This CVE has completed remediation and is a candidate for transition to ON_QA.

> Consider transitioning TC-9020 to ON_QA.

---

### TC-9023 — CVE-2026-39102 rustls - Certificate validation bypass [rhtpa-2.1]

- **Status:** In Progress
- **Created:** 2026-05-10

**Linked remediation Tasks (Depend):**

| Linked Task | Type | Status | Completed? |
|-------------|------|--------|------------|
| TC-9024 | Task | Done | Yes |
| TC-9025 | Task | In Progress | No |

**Result: EXCLUDED -- Remediation in progress**

TC-9025 is still In Progress. Not all linked remediation Tasks are completed, so this issue cannot move to ON_QA yet.

---

### TC-9026 — CVE-2026-39330 openssl - Buffer overflow in X.509 parsing [rhtpa-2.2]

- **Status:** Modified
- **Created:** 2026-05-05

**Linked remediation Tasks (Depend):** None

**Result: EXCLUDED -- No remediation to verify**

This issue has no linked Tasks with link type "Depend". Without remediation tasks to verify, it cannot be promoted to ON_QA. This may indicate remediation tasks were never created, or were linked with a different link type.

---

## Summary

| Issue | CVE | Status | Depend Links | All Tasks Done? | Ready for QA? |
|-------|-----|--------|--------------|-----------------|---------------|
| TC-9020 | CVE-2026-38901 | Modified | TC-9021 (Done), TC-9022 (Closed) | Yes | Yes |
| TC-9023 | CVE-2026-39102 | In Progress | TC-9024 (Done), TC-9025 (In Progress) | No | No |
| TC-9026 | CVE-2026-39330 | Modified | (none) | N/A | No |

**1 of 3 candidates qualified for Ready for QA: TC-9020.**
