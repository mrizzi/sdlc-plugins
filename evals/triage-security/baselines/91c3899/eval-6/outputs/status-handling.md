# Status-Aware Handling Decisions

This document details the handling decision for each issue found in the discovery mode queries, based on the status-aware handling rules defined in the triage-security skill.

---

## Handling Rules Reference

| Current Status | Handling |
|----------------|----------|
| **New** | Proceed with full triage (Steps 1-7) -- default path |
| **In Progress / Code Review / QA** | Warn: issue may be actively worked on. Ask engineer whether to proceed with triage or skip. |
| **Closed / Done / Resolved** | Warn: issue is already closed. Ask engineer whether to re-triage or skip. |

---

## Query 1 Issues: Untriaged

### TC-9001 -- New

- **CVE**: CVE-2026-40112
- **Summary**: h2 - HTTP/2 rapid reset vulnerability [rhtpa-2.2]
- **Status**: New
- **Created**: 2026-06-08
- **Handling Decision**: **Proceed with full triage.** This issue is in New status, which is the default path. Execute Steps 1 through 7 in sequence: data extraction, version impact analysis, Affects Versions correction, duplicate/sibling check, lifecycle check, already-fixed check, and remediation.

### TC-9002 -- New

- **CVE**: CVE-2026-40297
- **Summary**: serde_json - Stack overflow on deeply nested input [rhtpa-2.1]
- **Status**: New
- **Created**: 2026-06-07
- **Handling Decision**: **Proceed with full triage.** This issue is in New status, which is the default path. Execute Steps 1 through 7 in sequence: data extraction, version impact analysis, Affects Versions correction, duplicate/sibling check, lifecycle check, already-fixed check, and remediation.

### TC-9003 -- In Progress

- **CVE**: CVE-2026-40455
- **Summary**: tokio - Race condition in task cancellation [rhtpa-2.2]
- **Status**: In Progress
- **Created**: 2026-06-05
- **Handling Decision**: **WARNING -- This issue is already in `In Progress`. It may be actively worked on.** Before proceeding, the engineer must be asked:
  1. **Proceed with triage anyway** -- useful to verify version impact or update Affects Versions even while work is underway.
  2. **Skip this issue** -- if the engineer confirms active work is covering the triage concerns.

  This issue should NOT be triaged automatically. The In Progress status indicates someone may already be investigating or remediating this vulnerability. Proceeding without confirmation risks conflicting with ongoing work.

### TC-9004 -- New

- **CVE**: CVE-2026-40518
- **Summary**: ring - Timing side-channel in RSA verification [rhtpa-2.2]
- **Status**: New
- **Created**: 2026-06-04
- **Handling Decision**: **Proceed with full triage.** This issue is in New status, which is the default path. Execute Steps 1 through 7 in sequence: data extraction, version impact analysis, Affects Versions correction, duplicate/sibling check, lifecycle check, already-fixed check, and remediation.

---

## Query 2 Issues: Triaged but still New

### TC-9010 -- New (previously triaged)

- **CVE**: CVE-2026-39874
- **Summary**: quinn-proto - Panic on malformed QUIC frame [rhtpa-2.2]
- **Status**: New
- **Labels**: CVE-2026-39874, pscomponent:org/rhtpa-server, ai-cve-triaged
- **Created**: 2026-05-28
- **Handling Decision**: **Eligible for re-triage or follow-up.** This issue was previously triaged (has `ai-cve-triaged` label) but remains in New status. This is unusual -- after triage, issues should either have remediation tasks created (moving the work forward) or be closed (if not affected). The engineer should investigate:
  - Were remediation tasks created during the previous triage? If so, are they progressing?
  - Has something changed since the original triage that warrants re-analysis?
  - Should this issue be re-triaged with fresh version impact analysis?

  Since the status is New, full triage (Steps 1-7) can proceed if the engineer chooses to re-triage.

---

## Summary Table

| Issue Key | Status | CVE ID | Handling |
|-----------|--------|--------|----------|
| TC-9001 | New | CVE-2026-40112 | Full triage (default path) |
| TC-9002 | New | CVE-2026-40297 | Full triage (default path) |
| TC-9003 | In Progress | CVE-2026-40455 | WARNING: may be actively worked on -- ask engineer before proceeding |
| TC-9004 | New | CVE-2026-40518 | Full triage (default path) |
| TC-9010 | New (triaged) | CVE-2026-39874 | Follow-up needed -- triaged but never actioned |
