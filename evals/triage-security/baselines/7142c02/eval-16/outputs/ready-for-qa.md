# Ready for QA Filtering Analysis

## Overview

Query 3 searches for triaged Vulnerability issues that are not yet closed, verified, or on QA:

```
project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status NOT IN (Closed, Verified, 'ON_QA') ORDER BY created DESC
```

This query returned 3 candidate issues. Each candidate is evaluated by inspecting its `issuelinks` for linked Tasks with link type "Depend". The filtering rules are:

1. **ALL linked remediation Tasks are Done or Closed** --> Include in Ready for QA list.
2. **ANY linked Task is still open** --> Exclude. Remediation is still in progress.
3. **NO linked Tasks with type "Depend" exist** --> Exclude. No remediation to verify.

---

## Candidate Analysis

### TC-9020 — CVE-2026-38901 hyper - HTTP request smuggling [rhtpa-2.2]

- **Status**: Modified
- **CVE**: CVE-2026-38901
- **Created**: 2026-05-15

**Linked Tasks (Depend type):**

| Linked Task | Type | Status | Completed? |
|-------------|------|--------|------------|
| TC-9021 | Task | Done | Yes |
| TC-9022 | Task | Closed | Yes |

**Evaluation**: All 2 linked remediation Tasks are in a completed state (Done or Closed). Both "Done" and "Closed" are terminal statuses that indicate the remediation work has been finished.

**Result**: **INCLUDED** in Ready for QA list.

**Suggested action**: Transition TC-9020 to ON_QA. All remediation work has been completed and the vulnerability fix is ready for quality assurance verification.

---

### TC-9023 — CVE-2026-39102 rustls - Certificate validation bypass [rhtpa-2.1]

- **Status**: In Progress
- **CVE**: CVE-2026-39102
- **Created**: 2026-05-10

**Linked Tasks (Depend type):**

| Linked Task | Type | Status | Completed? |
|-------------|------|--------|------------|
| TC-9024 | Task | Done | Yes |
| TC-9025 | Task | In Progress | No |

**Evaluation**: TC-9025 is still In Progress. While TC-9024 has been completed (Done), the rule requires ALL linked remediation Tasks to be completed. One open Task is sufficient to exclude the issue.

**Result**: **EXCLUDED** — Remediation is still in progress. TC-9025 must reach Done or Closed status before TC-9023 can be considered Ready for QA.

---

### TC-9026 — CVE-2026-39330 openssl - Buffer overflow in X.509 parsing [rhtpa-2.2]

- **Status**: Modified
- **CVE**: CVE-2026-39330
- **Created**: 2026-05-05

**Linked Tasks (Depend type):**

(none)

**Evaluation**: No issuelinks with link type "Depend" were found on this issue. Without any linked remediation Tasks, there is no remediation work to verify. This could indicate that remediation tasks have not yet been created, or that the triage outcome did not require remediation tasks.

**Result**: **EXCLUDED** — No linked Tasks with Depend type. No remediation to verify. This issue may need further triage attention to determine whether remediation tasks should be created.

---

## Summary

| Issue | CVE | Status | Depend Links | All Completed? | Ready for QA? |
|-------|-----|--------|--------------|----------------|---------------|
| TC-9020 | CVE-2026-38901 | Modified | TC-9021 (Done), TC-9022 (Closed) | Yes | **Yes** |
| TC-9023 | CVE-2026-39102 | In Progress | TC-9024 (Done), TC-9025 (In Progress) | No | No |
| TC-9026 | CVE-2026-39330 | Modified | (none) | N/A | No |

**1 of 3 candidates qualified for Ready for QA.**

### Recommended Actions

- **TC-9020**: Transition to ON_QA. All remediation Tasks are complete.
- **TC-9023**: Monitor TC-9025 until it reaches Done or Closed, then re-evaluate.
- **TC-9026**: Investigate whether remediation tasks need to be created or linked for this vulnerability.
