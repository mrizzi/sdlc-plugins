# Ready for QA Filtering Analysis

## Query

```
project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status NOT IN (Closed, Verified, 'ON_QA') ORDER BY created DESC
```

This query returns triaged Vulnerability issues that are not yet closed, verified, or on QA. Each result is then evaluated by inspecting its `issuelinks` for linked Tasks with link type "Depend".

## Filtering Criteria

A triaged CVE qualifies as **Ready for QA** only when:

1. It has at least one linked Task with link type "Depend".
2. **ALL** such linked Tasks have a terminal status (Done or Closed).

An issue is **excluded** if:
- Any linked Depend Task is still open (status other than Done/Closed) -- remediation is still in progress.
- No linked Tasks with type "Depend" exist -- there is no remediation work to verify.

## Candidates Evaluated

3 issues returned by the query.

---

### TC-9020 -- CVE-2026-38901 hyper - HTTP request smuggling [rhtpa-2.2]

- **Status**: Modified
- **CVE**: CVE-2026-38901
- **Created**: 2026-05-15

**Linked Depend Tasks:**

| Task | Type | Status | Terminal? |
|------|------|--------|-----------|
| TC-9021 | Task | Done | Yes |
| TC-9022 | Task | Closed | Yes |

**Assessment**: ALL linked remediation Tasks are in a terminal status (TC-9021 Done, TC-9022 Closed).

**Result: QUALIFIED -- Ready for QA**

Recommendation: Consider transitioning TC-9020 to ON_QA.

---

### TC-9023 -- CVE-2026-39102 rustls - Certificate validation bypass [rhtpa-2.1]

- **Status**: In Progress
- **CVE**: CVE-2026-39102
- **Created**: 2026-05-10

**Linked Depend Tasks:**

| Task | Type | Status | Terminal? |
|------|------|--------|-----------|
| TC-9024 | Task | Done | Yes |
| TC-9025 | Task | In Progress | No |

**Assessment**: TC-9025 is still In Progress. Not all linked remediation Tasks have reached a terminal status.

**Result: EXCLUDED -- Remediation in progress**

TC-9025 must reach Done or Closed before TC-9023 can be considered for QA.

---

### TC-9026 -- CVE-2026-39330 openssl - Buffer overflow in X.509 parsing [rhtpa-2.2]

- **Status**: Modified
- **CVE**: CVE-2026-39330
- **Created**: 2026-05-05

**Linked Depend Tasks:** None

**Assessment**: No linked Tasks with link type "Depend" found. Without remediation tasks to verify, the issue cannot be moved to QA.

**Result: EXCLUDED -- No remediation tasks to verify**

---

## Summary

| Issue | CVE | Status | Depend Links | All Done/Closed? | Ready for QA? |
|-------|-----|--------|--------------|-------------------|---------------|
| TC-9020 | CVE-2026-38901 | Modified | TC-9021 (Done), TC-9022 (Closed) | Yes | Yes |
| TC-9023 | CVE-2026-39102 | In Progress | TC-9024 (Done), TC-9025 (In Progress) | No | No |
| TC-9026 | CVE-2026-39330 | Modified | (none) | N/A | No |

**1 of 3** candidates qualified for QA transition: **TC-9020**.
