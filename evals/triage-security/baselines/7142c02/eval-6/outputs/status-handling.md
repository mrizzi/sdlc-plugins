# Status-Aware Handling Decisions

This document describes the status-aware handling decision for each issue found during discovery, following the protocol defined in the triage-security skill.

---

## Handling Rules

| Current Status | Action |
|----------------|--------|
| **New** | Proceed with full triage (Steps 1-7) |
| **In Progress / Code Review / QA** | Warn: issue is actively worked on. Ask user to proceed or skip. |
| **Closed / Done / Resolved** | Warn: issue is already closed. Ask user to re-triage or skip. |

---

## Query 1: Untriaged Issues

### TC-9001 -- CVE-2026-40112 (h2 - HTTP/2 rapid reset vulnerability)

- **Status**: New
- **Handling**: Proceed with full triage. This is an untriaged issue in New status -- the default path. Execute Steps 1 through 7 in sequence: data extraction, external CVE enrichment, version impact analysis, Affects Versions correction, duplicate/sibling check, lifecycle check, already-fixed check, and remediation.

### TC-9002 -- CVE-2026-40297 (serde_json - Stack overflow on deeply nested input)

- **Status**: New
- **Handling**: Proceed with full triage. This is an untriaged issue in New status -- the default path. Execute Steps 1 through 7 in sequence.

### TC-9003 -- CVE-2026-40455 (tokio - Race condition in task cancellation)

- **Status**: In Progress
- **Handling**: **Warning** -- This issue is already in `In Progress`. It may be actively worked on. Before triaging, ask the user:
  1. Proceed with triage anyway (e.g., to verify version impact or update Affects Versions)
  2. Skip this issue
- If the user chooses to skip, return to the discovery list or end the session.

### TC-9004 -- CVE-2026-40518 (ring - Timing side-channel in RSA verification)

- **Status**: New
- **Handling**: Proceed with full triage. This is an untriaged issue in New status -- the default path. Execute Steps 1 through 7 in sequence.

---

## Query 2: Triaged but still New

### TC-9010 -- CVE-2026-39874 (quinn-proto - Panic on malformed QUIC frame)

- **Status**: New
- **Handling**: This issue carries the `ai-cve-triaged` label but remains in New status, indicating it was triaged previously but never actioned. It may need follow-up or re-triage. Since the status is New, proceed with full triage if the user selects it.

---

## Query 3: Ready for QA Candidates

### TC-9020 -- CVE-2026-38901 (hyper - HTTP request smuggling)

- **Status**: Modified
- **Handling**: All linked remediation Tasks are completed (TC-9021 Done, TC-9022 Closed). This issue qualifies for transition to ON_QA. Suggest to the user: "Consider transitioning TC-9020 to ON_QA." No triage action needed -- remediation is complete.

### TC-9023 -- CVE-2026-39102 (rustls - Certificate validation bypass)

- **Status**: In Progress
- **Handling**: **Warning** -- This issue is in `In Progress` and has an active remediation task (TC-9025 still In Progress). It is excluded from the Ready for QA list because not all remediation tasks are completed. If the user selects this issue for triage, warn that it is actively being worked on and ask whether to proceed or skip.

### TC-9026 -- CVE-2026-39330 (openssl - Buffer overflow in X.509 parsing)

- **Status**: Modified
- **Handling**: Excluded from Ready for QA because no linked Tasks with type "Depend" were found. There is no remediation work to verify. If the user selects this issue, it may need remediation tasks created (re-triage), or the links may need to be added manually.
