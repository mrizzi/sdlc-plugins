# Ready for QA — Filtering Analysis

**Project key:** TC
**Date:** 2026-07-02

---

## Query

```
project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status NOT IN (Closed, Verified, 'ON_QA') ORDER BY created DESC
```

This query returns triaged Vulnerability issues that have not yet reached ON_QA, Verified, or Closed status. Each candidate is then filtered by inspecting its linked remediation Tasks.

## Filtering Criteria

Per the discovery mode specification, a CVE qualifies as "Ready for QA" only when:

1. It has linked issues with link type **"Depend"**
2. **ALL** linked remediation Tasks (Depend links) are in **Done** or **Closed** status

An issue is **excluded** if:
- Any linked Task is still open (remediation in progress)
- No linked Tasks with type "Depend" exist (no remediation to verify)

---

## Candidate Analysis

### TC-9020 — CVE-2026-38901 hyper - HTTP request smuggling [rhtpa-2.2]

| Field | Value |
|-------|-------|
| Status | Modified |
| CVE | CVE-2026-38901 |
| Labels | CVE-2026-38901, pscomponent:org/rhtpa-server, ai-cve-triaged |
| Created | 2026-05-15 |

**Linked remediation Tasks (Depend):**

| Linked Issue | Type | Status |
|--------------|------|--------|
| TC-9021 | Task | Done |
| TC-9022 | Task | Closed |

**Analysis:** Both linked remediation Tasks are in terminal states (Done and Closed). All remediation work is complete.

**Result: QUALIFIED -- Ready for QA**

Recommendation: Consider transitioning TC-9020 to ON_QA.

---

### TC-9023 — CVE-2026-39102 rustls - Certificate validation bypass [rhtpa-2.1]

| Field | Value |
|-------|-------|
| Status | In Progress |
| CVE | CVE-2026-39102 |
| Labels | CVE-2026-39102, pscomponent:org/rhtpa-server, ai-cve-triaged |
| Created | 2026-05-10 |

**Linked remediation Tasks (Depend):**

| Linked Issue | Type | Status |
|--------------|------|--------|
| TC-9024 | Task | Done |
| TC-9025 | Task | In Progress |

**Analysis:** TC-9024 is Done, but TC-9025 is still In Progress. Not all remediation Tasks are complete. Remediation is still actively underway.

**Result: EXCLUDED -- Remediation in progress**

TC-9025 must reach Done or Closed status before TC-9023 can be considered Ready for QA.

---

### TC-9026 — CVE-2026-39330 openssl - Buffer overflow in X.509 parsing [rhtpa-2.2]

| Field | Value |
|-------|-------|
| Status | Modified |
| CVE | CVE-2026-39330 |
| Labels | CVE-2026-39330, pscomponent:org/rhtpa-server, ai-cve-triaged |
| Created | 2026-05-05 |

**Linked remediation Tasks (Depend):** None

**Analysis:** This issue has no linked Tasks with link type "Depend". Without remediation tasks, there is nothing to verify in QA. This issue may need investigation — it was triaged (ai-cve-triaged label is present) and reached Modified status, but no remediation tasks were linked.

**Result: EXCLUDED -- No remediation tasks to verify**

---

## Filtering Summary

| Issue | CVE | Status | Depend Links | All Tasks Complete? | Ready for QA? |
|-------|-----|--------|--------------|---------------------|---------------|
| TC-9020 | CVE-2026-38901 | Modified | TC-9021 (Done), TC-9022 (Closed) | Yes | Yes |
| TC-9023 | CVE-2026-39102 | In Progress | TC-9024 (Done), TC-9025 (In Progress) | No | No -- open task |
| TC-9026 | CVE-2026-39330 | Modified | (none) | N/A | No -- no tasks |

**Qualified for QA transition:** 1 of 3 candidates (TC-9020)
