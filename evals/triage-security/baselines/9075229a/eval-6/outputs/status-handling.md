# Status-Aware Handling Decisions

Per the triage-security skill's status-aware handling protocol, each discovered issue's current Jira status determines the triage path when the engineer selects it.

---

## Untriaged Issues

### TC-9001 — CVE-2026-40112 h2 - HTTP/2 rapid reset vulnerability [rhtpa-2.2]
- **Status:** New
- **Handling:** Proceed with full triage (default path). Steps 0 through 8 execute in sequence. No warnings or gates required before starting.

### TC-9002 — CVE-2026-40297 serde_json - Stack overflow on deeply nested input [rhtpa-2.1]
- **Status:** New
- **Handling:** Proceed with full triage (default path). Steps 0 through 8 execute in sequence. No warnings or gates required before starting.

### TC-9003 — CVE-2026-40455 tokio - Race condition in task cancellation [rhtpa-2.2]
- **Status:** In Progress
- **Handling:** Warn the engineer: "This issue is already in `In Progress`. It may be actively worked on." Present two options:
  1. Proceed with triage anyway (e.g., to verify version impact or update Affects Versions)
  2. Skip this issue
- If the engineer chooses to skip, return to the discovery list or end the session.

### TC-9004 — CVE-2026-40518 ring - Timing side-channel in RSA verification [rhtpa-2.2]
- **Status:** New
- **Handling:** Proceed with full triage (default path). Steps 0 through 8 execute in sequence. No warnings or gates required before starting.

---

## Triaged but still New

### TC-9010 — CVE-2026-39874 quinn-proto - Panic on malformed QUIC frame [rhtpa-2.2]
- **Status:** New
- **Labels:** ai-cve-triaged
- **Handling:** This issue was previously triaged but never moved beyond New status. Proceed with full triage (default path for New status). The engineer should investigate why the issue stalled after initial triage -- it may need re-triage if conditions have changed, or follow-up to action the original triage recommendations.

---

## Ready for QA Candidates

### TC-9020 — CVE-2026-38901 hyper - HTTP request smuggling [rhtpa-2.2]
- **Status:** Modified
- **Linked Tasks:** TC-9021 (Done), TC-9022 (Closed)
- **Handling:** All linked remediation tasks are complete. This issue is a candidate for ON_QA transition. Warn the engineer: "This issue is already in `Modified`. It may be actively worked on." Present two options:
  1. Proceed with triage anyway (e.g., to verify version impact or update Affects Versions)
  2. Skip this issue
- **Recommendation:** Consider transitioning to ON_QA since all remediation tasks are Done or Closed.

### TC-9023 — CVE-2026-39102 rustls - Certificate validation bypass [rhtpa-2.1]
- **Status:** In Progress
- **Linked Tasks:** TC-9024 (Done), TC-9025 (In Progress)
- **Handling:** Warn the engineer: "This issue is already in `In Progress`. It may be actively worked on." Present two options:
  1. Proceed with triage anyway (e.g., to verify version impact or update Affects Versions)
  2. Skip this issue
- **Note:** Excluded from Ready for QA -- remediation task TC-9025 is still In Progress. This issue should not transition to ON_QA until all remediation tasks complete.

### TC-9026 — CVE-2026-39330 openssl - Buffer overflow in X.509 parsing [rhtpa-2.2]
- **Status:** Modified
- **Linked Tasks:** None (no Depend links)
- **Handling:** Warn the engineer: "This issue is already in `Modified`. It may be actively worked on." Present two options:
  1. Proceed with triage anyway (e.g., to verify version impact or update Affects Versions)
  2. Skip this issue
- **Note:** Excluded from Ready for QA -- no linked remediation tasks with type "Depend" exist. There is no remediation to verify. This may indicate the issue was closed without remediation tasks, or tasks were not properly linked.
