# Status-Aware Handling Decisions

For each issue surfaced in discovery mode, the following status-aware handling
applies per the triage-security skill procedure.

## Untriaged Issues (Query 1)

### TC-9001 — CVE-2026-40112 h2 - HTTP/2 rapid reset vulnerability [rhtpa-2.2]
- **Current status:** New
- **Handling:** Proceed with full triage (default path). No warnings required.

### TC-9002 — CVE-2026-40297 serde_json - Stack overflow on deeply nested input [rhtpa-2.1]
- **Current status:** New
- **Handling:** Proceed with full triage (default path). No warnings required.

### TC-9003 — CVE-2026-40455 tokio - Race condition in task cancellation [rhtpa-2.2]
- **Current status:** In Progress
- **Handling:** Warn the user: "This issue is already in `In Progress`. It may be actively worked on." Ask whether to:
  1. Proceed with triage anyway (e.g., to verify version impact or update Affects Versions)
  2. Skip this issue

### TC-9004 — CVE-2026-40518 ring - Timing side-channel in RSA verification [rhtpa-2.2]
- **Current status:** New
- **Handling:** Proceed with full triage (default path). No warnings required.

## Triaged but Still New (Query 2)

### TC-9010 — CVE-2026-39874 quinn-proto - Panic on malformed QUIC frame [rhtpa-2.2]
- **Current status:** New
- **Handling:** Proceed with full triage (default path). No warnings required. However, this issue has the `ai-cve-triaged` label, indicating it was previously triaged but never moved out of New status. This may warrant re-triage to verify the prior assessment or follow-up to understand why it stalled.

## Ready for QA Candidates (Query 3)

### TC-9020 — CVE-2026-38901 hyper - HTTP request smuggling [rhtpa-2.2]
- **Current status:** Modified
- **Handling:** Warn the user: "This issue is already in `Modified`. It may be actively worked on." Ask whether to:
  1. Proceed with triage anyway (e.g., to verify version impact or update Affects Versions)
  2. Skip this issue

  However, since this issue appears in the Ready for QA list (all remediation Tasks completed), the recommended action is to transition to ON_QA rather than re-triage.

### TC-9023 — CVE-2026-39102 rustls - Certificate validation bypass [rhtpa-2.1]
- **Current status:** In Progress
- **Handling:** Warn the user: "This issue is already in `In Progress`. It may be actively worked on." Ask whether to:
  1. Proceed with triage anyway (e.g., to verify version impact or update Affects Versions)
  2. Skip this issue

  Remediation is still in progress (TC-9025 is In Progress), so this issue is not ready for QA.

### TC-9026 — CVE-2026-39330 openssl - Buffer overflow in X.509 parsing [rhtpa-2.2]
- **Current status:** Modified
- **Handling:** Warn the user: "This issue is already in `Modified`. It may be actively worked on." Ask whether to:
  1. Proceed with triage anyway (e.g., to verify version impact or update Affects Versions)
  2. Skip this issue

  No linked remediation Tasks exist (no "Depend" links), so this issue cannot be verified as ready for QA. It may need remediation tasks created or manual investigation.
