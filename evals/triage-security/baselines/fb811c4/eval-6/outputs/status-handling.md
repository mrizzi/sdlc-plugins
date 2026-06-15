# Status-Aware Handling Decisions

## Untriaged Issues

### TC-9001 | New | CVE-2026-40112 | h2 - HTTP/2 rapid reset vulnerability [rhtpa-2.2]

**Decision**: Present for full triage -- standard path.

This issue is in New status with no `ai-cve-triaged` label. It should proceed through the normal triage workflow: CVE analysis, affected component identification, impact assessment, and disposition.

---

### TC-9002 | New | CVE-2026-40297 | serde_json - Stack overflow on deeply nested input [rhtpa-2.1]

**Decision**: Present for full triage -- standard path.

This issue is in New status with no `ai-cve-triaged` label. It should proceed through the normal triage workflow: CVE analysis, affected component identification, impact assessment, and disposition.

---

### TC-9003 | In Progress | CVE-2026-40455 | tokio - Race condition in task cancellation [rhtpa-2.2]

**Decision**: WARNING -- This issue is already in In Progress status. It may be actively worked on.

This issue has moved beyond New into In Progress, which indicates someone may already be investigating or remediating it. Presenting it for full triage without acknowledgment could conflict with ongoing work or produce duplicate effort. The operator should confirm whether active work is underway before proceeding with triage actions. If the issue was moved to In Progress prematurely or by automation, it may still need triage, but that determination requires human acknowledgment first.

---

### TC-9004 | New | CVE-2026-40518 | ring - Timing side-channel in RSA verification [rhtpa-2.2]

**Decision**: Present for full triage -- standard path.

This issue is in New status with no `ai-cve-triaged` label. It should proceed through the normal triage workflow: CVE analysis, affected component identification, impact assessment, and disposition.

---

## Triaged but still New

### TC-9010 | New | CVE-2026-39874 | quinn-proto - Panic on malformed QUIC frame [rhtpa-2.2]

**Decision**: Flag for follow-up or re-triage.

This issue was previously triaged (it carries the `ai-cve-triaged` label) but remains in New status, meaning it was never moved forward after triage. This could indicate:

- The triage disposition was to defer or accept risk, but the issue was not transitioned to reflect that decision.
- The triage was completed but follow-up actions were not taken.
- The issue may need re-triage if conditions have changed since the original assessment.

This issue should be reviewed to determine why it stalled and whether the original triage decision is still valid or needs to be revisited.
