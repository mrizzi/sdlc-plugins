# Ready for QA — Filtering Analysis

**Project key:** TC
**Date:** 2026-07-10

## Query

```
project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status NOT IN (Closed, Verified, 'ON_QA') ORDER BY created DESC
```

This query returns triaged Vulnerability issues that are not yet Closed, Verified, or ON_QA. Each candidate is then evaluated based on its linked remediation Tasks (link type "Depend") to determine readiness.

## Candidates Evaluated

3 issues returned from Query 3.

---

### TC-9020 — CVE-2026-38901 hyper - HTTP request smuggling [rhtpa-2.2]

- **Status:** Modified
- **Created:** 2026-05-15
- **Linked remediation Tasks (Depend):**
  - TC-9021 (Task) — **Done**
  - TC-9022 (Task) — **Closed**
- **Assessment:** ALL linked remediation Tasks are in a terminal state (Done or Closed). No open work remains.
- **Result: QUALIFIED — Ready for QA**
- **Recommendation:** Consider transitioning TC-9020 to ON_QA.

---

### TC-9023 — CVE-2026-39102 rustls - Certificate validation bypass [rhtpa-2.1]

- **Status:** In Progress
- **Created:** 2026-05-10
- **Linked remediation Tasks (Depend):**
  - TC-9024 (Task) — **Done**
  - TC-9025 (Task) — **In Progress**
- **Assessment:** TC-9025 is still In Progress. Not all remediation Tasks are completed.
- **Result: EXCLUDED — Remediation in progress**
- **Reason:** TC-9025 remains open (In Progress). This CVE cannot move to QA until all linked remediation Tasks reach Done or Closed status.

---

### TC-9026 — CVE-2026-39330 openssl - Buffer overflow in X.509 parsing [rhtpa-2.2]

- **Status:** Modified
- **Created:** 2026-05-05
- **Linked remediation Tasks (Depend):** None
- **Assessment:** No linked Tasks with link type "Depend" exist on this issue.
- **Result: EXCLUDED — No remediation to verify**
- **Reason:** Without linked remediation Tasks, there is no completed work to validate in QA. This issue may need remediation tasks created, or may have been addressed through a different mechanism not yet linked.

---

## Summary

| Issue | CVE | Status | Linked Tasks | All Complete? | Ready for QA? |
|-------|-----|--------|--------------|---------------|---------------|
| TC-9020 | CVE-2026-38901 | Modified | TC-9021 (Done), TC-9022 (Closed) | Yes | Yes |
| TC-9023 | CVE-2026-39102 | In Progress | TC-9024 (Done), TC-9025 (In Progress) | No | No — remediation in progress |
| TC-9026 | CVE-2026-39330 | Modified | (none) | N/A | No — no remediation to verify |

**Result:** 1 of 3 candidates qualified for QA transition.

### Filtering Rules Applied

1. **ALL linked remediation Tasks are Done or Closed** — include in Ready for QA list. These CVEs have completed remediation and are candidates for ON_QA transition.
2. **ANY linked Task is still open** — exclude. Remediation is still in progress.
3. **NO linked Tasks with type "Depend" exist** — exclude. No remediation to verify.
