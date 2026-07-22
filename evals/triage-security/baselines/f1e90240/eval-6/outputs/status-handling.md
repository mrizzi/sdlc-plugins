# Status-Aware Handling Decisions

Per the triage-security skill's discovery mode, each listed issue is evaluated
against its current Jira status to determine the appropriate handling path.

## Status Handling Rules

| Status | Handling |
|--------|----------|
| **New** | Proceed with full triage (default path) |
| **In Progress / Code Review / QA** | Warn: issue may be actively worked on. Offer to proceed with triage anyway or skip. |
| **Closed / Done / Resolved** | Warn: issue is already closed. Offer to re-triage or skip. |

---

## Query 1: Untriaged Issues

### TC-9001 -- CVE-2026-40112 h2 - HTTP/2 rapid reset vulnerability [rhtpa-2.2]

- **Status:** New
- **Decision:** Proceed with full triage (default path).
- **Action:** Select this issue to begin the 8-step triage workflow. The issue is in New status, so no warnings apply. Step 0.7 will assign the issue and transition it to Assigned.

### TC-9002 -- CVE-2026-40297 serde_json - Stack overflow on deeply nested input [rhtpa-2.1]

- **Status:** New
- **Decision:** Proceed with full triage (default path).
- **Action:** Select this issue to begin the 8-step triage workflow. The issue is in New status, so no warnings apply. Step 0.7 will assign the issue and transition it to Assigned.

### TC-9003 -- CVE-2026-40455 tokio - Race condition in task cancellation [rhtpa-2.2]

- **Status:** In Progress
- **Decision:** Warn before proceeding.
- **Warning:** "This issue is already in `In Progress`. It may be actively worked on."
- **Options:**
  1. Proceed with triage anyway (e.g., to verify version impact or update Affects Versions)
  2. Skip this issue
- **Rationale:** The In Progress status suggests someone may already be working on remediation. Proceeding could still be valuable to verify version impact or update Affects Versions, but the engineer should confirm.

### TC-9004 -- CVE-2026-40518 ring - Timing side-channel in RSA verification [rhtpa-2.2]

- **Status:** New
- **Decision:** Proceed with full triage (default path).
- **Action:** Select this issue to begin the 8-step triage workflow. The issue is in New status, so no warnings apply. Step 0.7 will assign the issue and transition it to Assigned.

---

## Query 2: Triaged but still New

### TC-9010 -- CVE-2026-39874 quinn-proto - Panic on malformed QUIC frame [rhtpa-2.2]

- **Status:** New
- **Decision:** Proceed with full triage (re-triage path).
- **Action:** This issue carries the `ai-cve-triaged` label but remains in New status. It was previously triaged but never moved forward. The engineer should investigate why it stalled:
  - Were remediation tasks created but not linked?
  - Was triage interrupted before task creation?
  - Does the original triage conclusion still hold?
- **Recommendation:** Re-triage to verify the original assessment and ensure remediation tasks exist and are properly linked. Since the status is New, no warnings apply -- proceed with full triage.

---

## Query 3: Ready for QA

### TC-9020 -- CVE-2026-38901 hyper - HTTP request smuggling [rhtpa-2.2]

- **Status:** Modified
- **Decision:** Ready for QA transition.
- **Action:** All linked remediation Tasks are complete (TC-9021 Done, TC-9022 Closed). This CVE has completed remediation and is a candidate for ON_QA transition.
- **Recommendation:** Consider transitioning TC-9020 to ON_QA. The "Modified" status confirms remediation work has been applied but not yet verified through QA.

### TC-9023 -- CVE-2026-39102 rustls - Certificate validation bypass [rhtpa-2.1]

- **Status:** In Progress
- **Decision:** Not ready for QA -- remediation still in progress.
- **Detail:** TC-9024 is Done, but TC-9025 is still In Progress. The issue cannot move to ON_QA until all remediation tasks are complete.
- **Handling if selected for triage:** Warn: "This issue is already in `In Progress`. It may be actively worked on." Offer to proceed or skip.

### TC-9026 -- CVE-2026-39330 openssl - Buffer overflow in X.509 parsing [rhtpa-2.2]

- **Status:** Modified
- **Decision:** Not ready for QA -- no linked remediation tasks to verify.
- **Detail:** No linked Tasks with type "Depend" exist. Without remediation tasks, there is nothing to verify as complete.
- **Handling if selected for triage:** Warn: "This issue is in `Modified` status but has no linked remediation tasks. It may need investigation to determine why no tasks were created."

---

## Decision Summary

| Issue | Status | Handling Decision |
|-------|--------|-------------------|
| TC-9001 | New | Proceed with full triage |
| TC-9002 | New | Proceed with full triage |
| TC-9003 | In Progress | Warn: may be actively worked on. Offer proceed/skip. |
| TC-9004 | New | Proceed with full triage |
| TC-9010 | New (stale) | Re-triage recommended -- previously triaged but never actioned |
| TC-9020 | Modified | Ready for QA -- consider transitioning to ON_QA |
| TC-9023 | In Progress | Not ready for QA -- TC-9025 still In Progress |
| TC-9026 | Modified | Not ready for QA -- no linked remediation tasks |
