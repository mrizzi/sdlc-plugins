# Status-Aware Handling Decisions

Per the triage-security SKILL.md discovery mode "Status-aware handling" rules, each issue's current Jira status determines how the skill proceeds when the engineer selects it for triage.

---

## Query 1: Untriaged Issues

### TC-9001 -- CVE-2026-40112 (h2 - HTTP/2 rapid reset vulnerability)
- **Status:** New
- **Handling:** Proceed with full triage (default path). New is the expected starting status for untriaged Vulnerability issues. Execute Steps 1-7 in sequence.

### TC-9002 -- CVE-2026-40297 (serde_json - Stack overflow on deeply nested input)
- **Status:** New
- **Handling:** Proceed with full triage (default path). New is the expected starting status for untriaged Vulnerability issues. Execute Steps 1-7 in sequence.

### TC-9003 -- CVE-2026-40455 (tokio - Race condition in task cancellation)
- **Status:** In Progress
- **Handling:** Warn the user: "This issue is already in In Progress. It may be actively worked on." Present two options:
  1. Proceed with triage anyway (e.g., to verify version impact or update Affects Versions)
  2. Skip this issue
- Wait for the engineer's choice before proceeding. If skip is chosen, return to the discovery list.

### TC-9004 -- CVE-2026-40518 (ring - Timing side-channel in RSA verification)
- **Status:** New
- **Handling:** Proceed with full triage (default path). New is the expected starting status for untriaged Vulnerability issues. Execute Steps 1-7 in sequence.

---

## Query 2: Triaged but still New

### TC-9010 -- CVE-2026-39874 (quinn-proto - Panic on malformed QUIC frame)
- **Status:** New
- **Handling:** This issue carries the `ai-cve-triaged` label but remains in New status, indicating it was previously triaged but never moved forward. Since status is New, the default path applies: proceed with full triage. However, the engineer should be alerted that this is a stale triaged issue -- it may need re-triage to verify previous findings or follow-up to understand why remediation was never started.

---

## Query 3: Ready for QA Candidates

### TC-9020 -- CVE-2026-38901 (hyper - HTTP request smuggling)
- **Status:** Modified
- **Handling:** This issue qualifies as Ready for QA because all linked remediation Tasks (TC-9021: Done, TC-9022: Closed) are complete. Since its status is Modified (not New, In Progress, or Closed), it does not trigger a status warning. The recommended action is to transition TC-9020 to ON_QA. If the engineer selects this issue for triage instead, proceed normally -- the Modified status does not block triage.

### TC-9023 -- CVE-2026-39102 (rustls - Certificate validation bypass)
- **Status:** In Progress
- **Handling:** Warn the user: "This issue is already in In Progress. It may be actively worked on." Present two options:
  1. Proceed with triage anyway (e.g., to verify version impact or update Affects Versions)
  2. Skip this issue
- Additionally, this issue is excluded from Ready for QA because TC-9025 is still In Progress. Remediation is incomplete.

### TC-9026 -- CVE-2026-39330 (openssl - Buffer overflow in X.509 parsing)
- **Status:** Modified
- **Handling:** This issue is excluded from Ready for QA because it has no linked remediation Tasks with link type "Depend" -- there is no remediation to verify. Since its status is Modified (not a terminal or active-work status that triggers a warning), triage can proceed if the engineer selects it. The absence of remediation tasks suggests this issue may need remediation task creation as part of triage.

---

## Summary Table

| Issue | Status | Status-Aware Action | Notes |
|-------|--------|---------------------|-------|
| TC-9001 | New | Proceed with full triage | Default path |
| TC-9002 | New | Proceed with full triage | Default path |
| TC-9003 | In Progress | Warn: may be actively worked on; ask to proceed or skip | Non-default status |
| TC-9004 | New | Proceed with full triage | Default path |
| TC-9010 | New | Proceed with full triage; flag as stale | Previously triaged but never actioned |
| TC-9020 | Modified | Suggest transition to ON_QA | All remediation tasks complete |
| TC-9023 | In Progress | Warn: may be actively worked on; ask to proceed or skip | Remediation still in progress (TC-9025) |
| TC-9026 | Modified | Triage can proceed; no remediation tasks exist | No "Depend" links found |
