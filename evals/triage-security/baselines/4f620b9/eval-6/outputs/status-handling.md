# Status-Aware Handling Decisions

This document records the status-aware handling decision for each issue discovered in the two JQL queries, following the triage-security skill's discovery mode rules.

---

## Untriaged Issues (Query 1)

### TC-9001 -- CVE-2026-40112 (h2 - HTTP/2 rapid reset vulnerability)
- **Status**: New
- **Handling**: Proceed with full triage (default path). This issue is in New status and has not been triaged. Ready for the complete 7-step version-aware triage workflow.

### TC-9002 -- CVE-2026-40297 (serde_json - Stack overflow on deeply nested input)
- **Status**: New
- **Handling**: Proceed with full triage (default path). This issue is in New status and has not been triaged. Ready for the complete 7-step version-aware triage workflow.

### TC-9003 -- CVE-2026-40455 (tokio - Race condition in task cancellation)
- **Status**: In Progress
- **Handling**: **Warning -- this issue is already in `In Progress`. It may be actively worked on.** Before triaging, the engineer must choose:
  1. **Proceed with triage anyway** -- e.g., to verify version impact or update Affects Versions even though work has begun.
  2. **Skip this issue** -- return to the discovery list or end the session.
  This issue requires explicit engineer confirmation before triage can begin.

### TC-9004 -- CVE-2026-40518 (ring - Timing side-channel in RSA verification)
- **Status**: New
- **Handling**: Proceed with full triage (default path). This issue is in New status and has not been triaged. Ready for the complete 7-step version-aware triage workflow.

---

## Triaged but still New (Query 2)

### TC-9010 -- CVE-2026-39874 (quinn-proto - Panic on malformed QUIC frame)
- **Status**: New (with `ai-cve-triaged` label)
- **Handling**: This issue was previously triaged but remains in New status. It has not been moved forward since triage. The engineer should review whether:
  - The previous triage outcome was not actioned (remediation tasks not created or not started).
  - Circumstances have changed requiring re-triage (e.g., new version streams, updated advisory data).
  - The issue should be picked up for implementation or closed if no longer relevant.
  This issue is flagged for follow-up attention.

---

## Summary Table

| Key | Status | Triaged? | Handling Decision |
|------|--------|----------|-------------------|
| TC-9001 | New | No | Full triage |
| TC-9002 | New | No | Full triage |
| TC-9003 | In Progress | No | Warning: active work -- engineer must confirm before triage |
| TC-9004 | New | No | Full triage |
| TC-9010 | New | Yes | Flagged: triaged but never actioned -- needs follow-up |
