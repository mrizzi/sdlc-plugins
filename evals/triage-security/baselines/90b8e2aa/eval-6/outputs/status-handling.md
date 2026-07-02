# Status-Aware Handling Decisions

Per the triage-security skill's status-aware handling rules, each discovered issue
is evaluated based on its current Jira status to determine the appropriate action
when selected for triage.

## Status Handling Rules

| Status | Handling |
|--------|----------|
| New | Proceed with full triage (default path) |
| In Progress / Code Review / QA | Warn: issue may be actively worked on. Offer to proceed or skip. |
| Closed / Done / Resolved | Warn: issue is already closed. Offer to re-triage or skip. |
| Modified | Issue has been modified post-triage. Offer to proceed (verify version impact / update Affects Versions) or skip. |

---

## Query 1 — Untriaged Issues

### TC-9001 — CVE-2026-40112 (h2 - HTTP/2 rapid reset vulnerability)

- **Current status:** New
- **Handling decision:** Proceed with full triage (default path).
- **Action:** Execute Steps 0.7 through 8 — assign to current user, transition to Assigned, extract CVE data, perform version impact analysis across streams 2.1.x and 2.2.x, correct Affects Versions, check for duplicates/siblings, verify lifecycle status, and create remediation tasks if affected.
- **Stream scope:** rhtpa-2.2 (maps to stream 2.2.x)

### TC-9002 — CVE-2026-40297 (serde_json - Stack overflow on deeply nested input)

- **Current status:** New
- **Handling decision:** Proceed with full triage (default path).
- **Action:** Execute Steps 0.7 through 8 — full triage workflow.
- **Stream scope:** rhtpa-2.1 (maps to stream 2.1.x)

### TC-9003 — CVE-2026-40455 (tokio - Race condition in task cancellation)

- **Current status:** In Progress
- **Handling decision:** Warn before proceeding.
- **Warning:** "This issue is already in `In Progress`. It may be actively worked on."
- **Options presented to engineer:**
  1. Proceed with triage anyway (e.g., to verify version impact or update Affects Versions)
  2. Skip this issue
- **Action if proceed:** Execute Steps 0.7 through 8. Step 0.7 will still assign to the current user but will skip the transition to Assigned since the issue is already past New status.
- **Action if skip:** Return to the discovery list or end the session.
- **Stream scope:** rhtpa-2.2 (maps to stream 2.2.x)

### TC-9004 — CVE-2026-40518 (ring - Timing side-channel in RSA verification)

- **Current status:** New
- **Handling decision:** Proceed with full triage (default path).
- **Action:** Execute Steps 0.7 through 8 — full triage workflow.
- **Stream scope:** rhtpa-2.2 (maps to stream 2.2.x)

---

## Query 2 — Triaged but Still New (Stale Issues)

### TC-9010 — CVE-2026-39874 (quinn-proto - Panic on malformed QUIC frame)

- **Current status:** New
- **Handling decision:** Proceed with full triage (default path). Although this issue carries the `ai-cve-triaged` label (indicating prior triage), it remains in New status, suggesting the triage outcome was never actioned. This issue may need follow-up or re-triage.
- **Action:** Execute Steps 0.7 through 8. The existing `ai-cve-triaged` label does not prevent re-triage — the label will remain after the updated triage completes. Review prior triage comments (if any) to determine why the issue was not moved forward.
- **Stream scope:** rhtpa-2.2 (maps to stream 2.2.x)

---

## Query 3 — Ready for QA Candidates

### TC-9020 — CVE-2026-38901 (hyper - HTTP request smuggling)

- **Current status:** Modified
- **Handling decision:** This issue is a Ready for QA candidate. All linked remediation Tasks are completed (TC-9021: Done, TC-9022: Closed).
- **Recommended action:** Transition TC-9020 to ON_QA. Present the transition to the engineer for confirmation before executing.
- **Stream scope:** rhtpa-2.2 (maps to stream 2.2.x)

### TC-9023 — CVE-2026-39102 (rustls - Certificate validation bypass)

- **Current status:** In Progress
- **Handling decision:** Excluded from Ready for QA. Remediation task TC-9025 is still In Progress.
- **Warning if selected for triage:** "This issue is already in `In Progress`. It may be actively worked on."
- **Options presented to engineer:**
  1. Proceed with triage anyway (e.g., to verify version impact or update Affects Versions)
  2. Skip this issue
- **Stream scope:** rhtpa-2.1 (maps to stream 2.1.x)

### TC-9026 — CVE-2026-39330 (openssl - Buffer overflow in X.509 parsing)

- **Current status:** Modified
- **Handling decision:** Excluded from Ready for QA. No linked remediation Tasks with link type "Depend" exist — there is no remediation to verify.
- **Action if selected:** This issue may need investigation to determine why it reached Modified status without linked remediation tasks. The engineer should review the issue history and determine whether remediation tasks need to be created or whether the issue should be closed.
- **Stream scope:** rhtpa-2.2 (maps to stream 2.2.x)

---

## Summary Table

| Issue | Status | Query Source | Handling Decision |
|-------|--------|--------------|-------------------|
| TC-9001 | New | Untriaged | Proceed with full triage |
| TC-9002 | New | Untriaged | Proceed with full triage |
| TC-9003 | In Progress | Untriaged | Warn: may be actively worked on; offer proceed/skip |
| TC-9004 | New | Untriaged | Proceed with full triage |
| TC-9010 | New | Triaged but still New | Proceed with full triage (re-triage; stale issue) |
| TC-9020 | Modified | Ready for QA | Ready for ON_QA transition (all remediation Tasks completed) |
| TC-9023 | In Progress | Ready for QA (excluded) | Warn: may be actively worked on; remediation still in progress |
| TC-9026 | Modified | Ready for QA (excluded) | Excluded: no linked remediation Tasks to verify |
