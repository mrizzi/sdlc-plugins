# Ready for QA — Filtering Analysis

**Project:** TC
**Date:** 2026-07-22

## Overview

Query 3 searched for triaged Vulnerability issues (labeled `ai-cve-triaged`) that are not yet in a terminal or QA status:

```
project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged)
AND status NOT IN (Closed, Verified, 'ON_QA') ORDER BY created DESC
```

3 candidate issues were returned. Each was evaluated by inspecting its `issuelinks` for linked Tasks with link type "Depend" to determine whether all remediation work is complete.

## Filtering Criteria

An issue qualifies as "Ready for QA" only when **all** of the following are true:
1. The issue has at least one linked Task with link type "Depend"
2. Every linked Depend Task has a status of Done or Closed
3. No linked Depend Task is still open (any status other than Done/Closed)

## Candidate Analysis

### TC-9020 — CVE-2026-38901 hyper - HTTP request smuggling [rhtpa-2.2]

- **Status:** Modified
- **CVE:** CVE-2026-38901
- **Created:** 2026-05-15

**Linked remediation Tasks (Depend):**

| Task | Status | Completed? |
|------|--------|------------|
| TC-9021 | Done | Yes |
| TC-9022 | Closed | Yes |

**Result: QUALIFIED — Ready for QA**

All 2 linked remediation Tasks are in a completed state (Done or Closed). This CVE has completed remediation and is a candidate for ON_QA transition.

---

### TC-9023 — CVE-2026-39102 rustls - Certificate validation bypass [rhtpa-2.1]

- **Status:** In Progress
- **CVE:** CVE-2026-39102
- **Created:** 2026-05-10

**Linked remediation Tasks (Depend):**

| Task | Status | Completed? |
|------|--------|------------|
| TC-9024 | Done | Yes |
| TC-9025 | In Progress | No |

**Result: EXCLUDED — Remediation in progress**

TC-9025 is still In Progress. Not all linked remediation Tasks are complete, so this issue cannot move to ON_QA yet. 1 of 2 Tasks remain open.

---

### TC-9026 — CVE-2026-39330 openssl - Buffer overflow in X.509 parsing [rhtpa-2.2]

- **Status:** Modified
- **CVE:** CVE-2026-39330
- **Created:** 2026-05-05

**Linked remediation Tasks (Depend):** None

**Result: EXCLUDED — No remediation tasks to verify**

This issue has no linked Tasks with link type "Depend". Without remediation tasks, there is no work to verify as complete. The issue may need remediation tasks created, or remediation may be tracked differently.

---

## Summary

| Issue | CVE | Status | Depend Tasks | All Complete? | Ready for QA? |
|-------|-----|--------|-------------|---------------|---------------|
| TC-9020 | CVE-2026-38901 | Modified | TC-9021 (Done), TC-9022 (Closed) | Yes | Yes |
| TC-9023 | CVE-2026-39102 | In Progress | TC-9024 (Done), TC-9025 (In Progress) | No | No |
| TC-9026 | CVE-2026-39330 | Modified | (none) | N/A | No |

**1 of 3 candidates qualified as Ready for QA.**

### Recommended Action

- **TC-9020**: Consider transitioning to ON_QA — all remediation is complete.
