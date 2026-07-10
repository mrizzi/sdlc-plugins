# Status-Aware Handling Decisions

This document applies the status-aware handling rules from the triage-security skill to each issue found in discovery mode.

## Handling Rules Reference

| Current Status | Handling |
|----------------|----------|
| **New** | Proceed with full triage (default path) |
| **In Progress / Code Review / QA** | Warn: issue may be actively worked on. Ask whether to proceed or skip. |
| **Closed / Done / Resolved** | Warn: issue is already closed. Ask whether to re-triage or skip. |
| **Modified** | Not explicitly covered by status-aware rules; treat as active (similar to In Progress). |

---

## Query 1: Untriaged Issues

### TC-9001 — CVE-2026-40112 — h2 - HTTP/2 rapid reset vulnerability [rhtpa-2.2]

- **Status:** New
- **Handling:** Proceed with full triage (default path). No warnings required. This issue is untriaged and in initial state — standard triage flow applies starting from Step 0.7 (Assign and Transition to Assigned).

### TC-9002 — CVE-2026-40297 — serde_json - Stack overflow on deeply nested input [rhtpa-2.1]

- **Status:** New
- **Handling:** Proceed with full triage (default path). No warnings required. Standard triage flow applies.

### TC-9003 — CVE-2026-40455 — tokio - Race condition in task cancellation [rhtpa-2.2]

- **Status:** In Progress
- **Handling:** Warn the user before proceeding:

  > "This issue is already in `In Progress`. It may be actively worked on."

  Options presented to the engineer:
  1. **Proceed with triage anyway** — e.g., to verify version impact or update Affects Versions
  2. **Skip this issue**

  If the user chooses to skip, return to the discovery list. The issue lacks the `ai-cve-triaged` label despite being In Progress, which suggests triage was started manually or the issue was moved forward without completing AI triage. If the user proceeds, Step 0.7 will still assign the issue but skip the transition (already past Assigned status).

### TC-9004 — CVE-2026-40518 — ring - Timing side-channel in RSA verification [rhtpa-2.2]

- **Status:** New
- **Handling:** Proceed with full triage (default path). No warnings required. Standard triage flow applies.

---

## Query 2: Triaged but still New

### TC-9010 — CVE-2026-39874 — quinn-proto - Panic on malformed QUIC frame [rhtpa-2.2]

- **Status:** New
- **Handling:** Proceed with full triage (default path). No warnings required from the status-aware rules since the status is New.

  However, this issue carries the `ai-cve-triaged` label, meaning it was previously triaged but never moved out of New status. This is a stale issue that may need:
  - **Re-triage** if the previous triage outcome was not actioned (remediation tasks may not have been created, or Affects Versions may not have been corrected)
  - **Follow-up** to determine why it remains in New despite being triaged

  The engineer should review the previous triage comments on this issue before deciding whether to re-triage or investigate.

---

## Query 3: Ready for QA Candidates

### TC-9020 — CVE-2026-38901 — hyper - HTTP request smuggling [rhtpa-2.2]

- **Status:** Modified
- **Handling:** This issue is triaged and all remediation tasks are complete (TC-9021 Done, TC-9022 Closed). It is a candidate for transition to ON_QA.

  No status-aware warning is needed for triage purposes — this issue does not need re-triage. The recommended action is:
  > Consider transitioning TC-9020 to ON_QA. All linked remediation Tasks have been completed.

### TC-9023 — CVE-2026-39102 — rustls - Certificate validation bypass [rhtpa-2.1]

- **Status:** In Progress
- **Handling:** This issue is triaged (has `ai-cve-triaged` label) and is actively being worked on. Remediation task TC-9025 is still In Progress (TC-9024 is Done).

  If the engineer selects this issue for triage, the status-aware warning applies:
  > "This issue is already in `In Progress`. It may be actively worked on."

  However, since remediation is incomplete, re-triage is not recommended at this time. The appropriate action is to wait for TC-9025 to complete, then re-evaluate for ON_QA transition.

### TC-9026 — CVE-2026-39330 — openssl - Buffer overflow in X.509 parsing [rhtpa-2.2]

- **Status:** Modified
- **Handling:** This issue is triaged but has no linked remediation Tasks with type "Depend". It cannot be evaluated for QA readiness because there is no remediation work to verify.

  Possible scenarios:
  - Remediation tasks were never created (triage may have been incomplete)
  - The issue was resolved through a different mechanism not tracked via Depend links
  - Tasks exist but are linked with a different link type

  The engineer should investigate why this triaged issue in Modified status has no remediation task linkage. If remediation tasks need to be created, re-triage may be appropriate.

---

## Summary

| Issue | Status | Decision | Action |
|-------|--------|----------|--------|
| TC-9001 | New | Full triage | Proceed (default path) |
| TC-9002 | New | Full triage | Proceed (default path) |
| TC-9003 | In Progress | Warn + ask | May be actively worked on; confirm before triaging |
| TC-9004 | New | Full triage | Proceed (default path) |
| TC-9010 | New (stale) | Full triage with review | Previously triaged but stalled; review prior comments |
| TC-9020 | Modified | Ready for QA | Transition to ON_QA recommended |
| TC-9023 | In Progress | Wait | Remediation still in progress (TC-9025) |
| TC-9026 | Modified | Investigate | No remediation tasks linked; needs follow-up |
