# Status-Aware Handling Decisions

This document details the status-aware handling decision for each discovered Vulnerability issue, following the triage-security skill's status handling rules.

---

## Status Handling Rules Reference

| Current Status | Handling |
|----------------|----------|
| **New** | Proceed with full triage (default path) |
| **In Progress / Code Review / QA** | Warn: issue may be actively worked on. Ask whether to proceed with triage anyway or skip. |
| **Closed / Done / Resolved** | Warn: issue is already closed. Ask whether to re-triage or skip. |

---

## Issue-by-Issue Handling Decisions

### TC-9001 -- CVE-2026-40112 (h2 - HTTP/2 rapid reset vulnerability)

- **Current Status:** New
- **Labels:** CVE-2026-40112, pscomponent:org/rhtpa-server
- **Stream Scope:** 2.2.x (from summary suffix `[rhtpa-2.2]`)
- **Handling Decision:** **Proceed with full triage.** This issue is in New status and is untriaged (no `ai-cve-triaged` label). Standard triage path -- execute Steps 1 through 7 in sequence.

---

### TC-9002 -- CVE-2026-40297 (serde_json - Stack overflow on deeply nested input)

- **Current Status:** New
- **Labels:** CVE-2026-40297, pscomponent:org/rhtpa-server
- **Stream Scope:** 2.1.x (from summary suffix `[rhtpa-2.1]`)
- **Handling Decision:** **Proceed with full triage.** This issue is in New status and is untriaged. Standard triage path -- execute Steps 1 through 7 in sequence.

---

### TC-9003 -- CVE-2026-40455 (tokio - Race condition in task cancellation)

- **Current Status:** In Progress
- **Labels:** CVE-2026-40455, pscomponent:org/rhtpa-server
- **Stream Scope:** 2.2.x (from summary suffix `[rhtpa-2.2]`)
- **Handling Decision:** **Warning -- this issue is already in `In Progress` status.** It may be actively worked on by another engineer or team. Before triaging, the engineer should be asked:
  1. **Proceed with triage anyway** -- useful to verify version impact, update Affects Versions, or check for cross-stream impact even while active work is underway.
  2. **Skip this issue** -- return to the discovery list or end the session.

  This issue requires explicit engineer confirmation before triage can begin.

---

### TC-9004 -- CVE-2026-40518 (ring - Timing side-channel in RSA verification)

- **Current Status:** New
- **Labels:** CVE-2026-40518, pscomponent:org/rhtpa-server
- **Stream Scope:** 2.2.x (from summary suffix `[rhtpa-2.2]`)
- **Handling Decision:** **Proceed with full triage.** This issue is in New status and is untriaged. Standard triage path -- execute Steps 1 through 7 in sequence.

---

### TC-9010 -- CVE-2026-39874 (quinn-proto - Panic on malformed QUIC frame)

- **Current Status:** New
- **Labels:** CVE-2026-39874, pscomponent:org/rhtpa-server, ai-cve-triaged
- **Stream Scope:** 2.2.x (from summary suffix `[rhtpa-2.2]`)
- **Handling Decision:** **Flagged as stale -- triaged but still New.** This issue was previously triaged (carries the `ai-cve-triaged` label) but has not progressed beyond New status since its creation on 2026-05-28 (approximately 27 days ago). Possible actions:
  1. **Re-triage** -- the original triage may be outdated, remediation tasks may not have been created or actioned, or the version landscape may have changed.
  2. **Follow up on existing remediation** -- check whether remediation tasks were created during the original triage and investigate why they have not progressed.
  3. **Skip** -- if the engineer determines no action is needed.

  This issue should be reviewed to determine why it has remained in New status despite being triaged.

---

## Summary Table

| Key | Status | Triaged? | Handling | Action Required |
|-----|--------|----------|----------|-----------------|
| TC-9001 | New | No | Full triage | None -- proceed directly |
| TC-9002 | New | No | Full triage | None -- proceed directly |
| TC-9003 | In Progress | No | Warn + confirm | Engineer must choose: proceed or skip |
| TC-9004 | New | No | Full triage | None -- proceed directly |
| TC-9010 | New | Yes (stale) | Re-triage or follow-up | Engineer must review stale status |
