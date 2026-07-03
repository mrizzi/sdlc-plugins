# Status-Aware Handling Decisions

This document lists the handling decision for each discovered Vulnerability issue based on its current Jira status, per the triage-security skill's status-aware handling rules.

---

## Untriaged Issues

### TC-9001 — CVE-2026-40112 (h2 - HTTP/2 rapid reset vulnerability)
- **Status**: New
- **Handling**: Proceed with full triage (default path). This issue is in New status and has not been triaged. All triage steps (Data Extraction, External CVE Enrichment, Version Impact Analysis, Affects Versions Correction, Duplicate/Sibling Check, Lifecycle Check, Already Fixed Check, and Remediation) apply.

### TC-9002 — CVE-2026-40297 (serde_json - Stack overflow on deeply nested input)
- **Status**: New
- **Handling**: Proceed with full triage (default path). This issue is in New status and has not been triaged. All triage steps apply.

### TC-9003 — CVE-2026-40455 (tokio - Race condition in task cancellation)
- **Status**: In Progress
- **Handling**: **WARNING** — This issue is already in `In Progress`. It may be actively worked on. Before proceeding, the engineer must choose:
  1. **Proceed with triage anyway** — e.g., to verify version impact or update Affects Versions even though work is underway.
  2. **Skip this issue** — return to the discovery list.
  
  The skill will not proceed with triage on this issue until the engineer explicitly confirms which option to take.

### TC-9004 — CVE-2026-40518 (ring - Timing side-channel in RSA verification)
- **Status**: New
- **Handling**: Proceed with full triage (default path). This issue is in New status and has not been triaged. All triage steps apply.

---

## Triaged but still New Issues

### TC-9010 — CVE-2026-39874 (quinn-proto - Panic on malformed QUIC frame)
- **Status**: New (with `ai-cve-triaged` label)
- **Handling**: This issue was previously triaged but remains in New status, meaning no remediation work was started after triage. It should be reviewed for follow-up. The engineer may choose to:
  1. **Re-triage** — run full triage again to verify whether the previous assessment is still current (e.g., dependency versions may have changed since the original triage on 2026-05-28).
  2. **Review previous triage** — check the existing triage comment on the issue to determine why no action was taken, and decide whether remediation tasks need to be created.
  3. **Skip** — no action needed at this time.

---

## Ready for QA Issues

### TC-9020 — CVE-2026-38901 (hyper - HTTP request smuggling)
- **Status**: Modified
- **Handling**: All linked remediation Tasks are completed (TC-9021 Done, TC-9022 Closed). This issue is a candidate for transition to ON_QA. The engineer should review the completed remediation and transition the issue when satisfied.

### TC-9023 — CVE-2026-39102 (rustls - Certificate validation bypass)
- **Status**: In Progress
- **Handling**: Not ready for QA. Linked remediation Task TC-9025 is still In Progress. Remediation is incomplete; this issue should remain in its current status until all linked Tasks are resolved.

### TC-9026 — CVE-2026-39330 (openssl - Buffer overflow in X.509 parsing)
- **Status**: Modified
- **Handling**: Not ready for QA. No linked remediation Tasks with link type "Depend" were found. Without remediation tasks to verify, this issue cannot be moved to ON_QA. The engineer should investigate whether remediation tasks were never created or were linked incorrectly.

---

## Summary Table

| Key | CVE ID | Status | Handling Decision |
|-----|--------|--------|-------------------|
| TC-9001 | CVE-2026-40112 | New | Full triage |
| TC-9002 | CVE-2026-40297 | New | Full triage |
| TC-9003 | CVE-2026-40455 | In Progress | **Warning**: active work — engineer must confirm before proceeding |
| TC-9004 | CVE-2026-40518 | New | Full triage |
| TC-9010 | CVE-2026-39874 | New (triaged) | Follow-up review or re-triage recommended |
| TC-9020 | CVE-2026-38901 | Modified | **Ready for QA** — consider transitioning to ON_QA |
| TC-9023 | CVE-2026-39102 | In Progress | Not ready — remediation in progress (TC-9025) |
| TC-9026 | CVE-2026-39330 | Modified | Not ready — no linked remediation tasks |
