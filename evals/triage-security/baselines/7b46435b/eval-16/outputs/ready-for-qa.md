# Ready for QA — Filtering Analysis

## Query

```
project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status NOT IN (Closed, Verified, 'ON_QA') ORDER BY created DESC
```

This query returns triaged Vulnerability issues that are not yet closed, verified, or on QA. Each candidate is then checked for linked remediation Tasks (link type "Depend") to determine whether all remediation work is complete.

## Candidates (3 issues returned)

### TC-9020 — CVE-2026-38901 hyper - HTTP request smuggling [rhtpa-2.2]

- **Status**: Modified
- **Depend links**: TC-9021 (Task, **Done**), TC-9022 (Task, **Closed**)
- **Analysis**: All linked remediation Tasks are in a terminal state (Done or Closed). No open work remains.
- **Result**: **QUALIFIED — Ready for QA**
- **Recommendation**: Consider transitioning TC-9020 to ON_QA.

---

### TC-9023 — CVE-2026-39102 rustls - Certificate validation bypass [rhtpa-2.1]

- **Status**: In Progress
- **Depend links**: TC-9024 (Task, **Done**), TC-9025 (Task, **In Progress**)
- **Analysis**: TC-9025 is still In Progress. Remediation is not yet complete — at least one linked Task remains open.
- **Result**: **EXCLUDED — remediation in progress**
- **Reason**: ANY linked Task is still open (TC-9025 is In Progress).

---

### TC-9026 — CVE-2026-39330 openssl - Buffer overflow in X.509 parsing [rhtpa-2.2]

- **Status**: Modified
- **Depend links**: (none)
- **Analysis**: No linked Tasks with link type "Depend" exist on this issue. Without remediation tasks, there is nothing to verify as complete.
- **Result**: **EXCLUDED — no remediation to verify**
- **Reason**: NO linked Tasks with type "Depend" exist.

---

## Summary

| Issue | Status | Linked Tasks | All Complete? | Ready for QA? |
|-------|--------|--------------|---------------|---------------|
| TC-9020 | Modified | TC-9021 (Done), TC-9022 (Closed) | Yes | Yes |
| TC-9023 | In Progress | TC-9024 (Done), TC-9025 (In Progress) | No | No — open task |
| TC-9026 | Modified | (none) | N/A | No — no tasks |

**1 of 3** candidates qualified for Ready for QA: **TC-9020**.
