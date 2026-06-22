# Status-Aware Handling Decisions

Per SKILL.md discovery mode "Status-aware handling" rules, each issue's current
Jira status determines how it should be handled when selected for triage.

---

## Untriaged Issues (Query 1)

### TC-9001 -- CVE-2026-40112 h2 (HTTP/2 rapid reset vulnerability)

- **Status:** New
- **Stream scope:** 2.2.x (from summary suffix `[rhtpa-2.2]`)
- **Handling decision:** Proceed with full triage (Steps 1-7). This is the default path for New issues. No warnings or confirmation gates required beyond the standard step confirmations.

### TC-9002 -- CVE-2026-40297 serde_json (Stack overflow on deeply nested input)

- **Status:** New
- **Stream scope:** 2.1.x (from summary suffix `[rhtpa-2.1]`)
- **Handling decision:** Proceed with full triage (Steps 1-7). This is the default path for New issues. No warnings or confirmation gates required beyond the standard step confirmations.

### TC-9003 -- CVE-2026-40455 tokio (Race condition in task cancellation)

- **Status:** In Progress
- **Stream scope:** 2.2.x (from summary suffix `[rhtpa-2.2]`)
- **Handling decision:** Warn the user before proceeding. Per the status-aware handling rules, issues in "In Progress" status trigger the following warning:

  > "This issue is already in `In Progress`. It may be actively worked on."

  The engineer must choose one of:
  1. **Proceed with triage anyway** -- useful to verify version impact or update Affects Versions even though work has started.
  2. **Skip this issue** -- return to the discovery list or end the session.

  Do not proceed with triage until the engineer responds.

### TC-9004 -- CVE-2026-40518 ring (Timing side-channel in RSA verification)

- **Status:** New
- **Stream scope:** 2.2.x (from summary suffix `[rhtpa-2.2]`)
- **Handling decision:** Proceed with full triage (Steps 1-7). This is the default path for New issues. No warnings or confirmation gates required beyond the standard step confirmations.

---

## Triaged but Still New Issues (Query 2)

### TC-9010 -- CVE-2026-39874 quinn-proto (Panic on malformed QUIC frame)

- **Status:** New
- **Stream scope:** 2.2.x (from summary suffix `[rhtpa-2.2]`)
- **Labels:** ai-cve-triaged (already triaged)
- **Handling decision:** This issue has the `ai-cve-triaged` label but remains in New status. It appeared in Query 2 specifically to surface stale issues that were triaged but never actioned. The engineer should determine why the issue was not moved forward after initial triage. Options:
  1. **Re-triage** -- run the full triage workflow again (Steps 1-7) to verify original findings or detect changes (e.g., new upstream fixes, version updates).
  2. **Skip** -- if the original triage outcome was correct and the issue is simply awaiting manual action.

  Since the status is New, the default triage path applies if the engineer chooses to proceed. No "In Progress" or "Closed" warnings are triggered.

---

## Handling Decision Summary

| Key | Status | Labels | Decision | Action Required |
|-----|--------|--------|----------|-----------------|
| TC-9001 | New | -- | Full triage | None -- proceed directly |
| TC-9002 | New | -- | Full triage | None -- proceed directly |
| TC-9003 | In Progress | -- | Warn + confirm | Engineer must choose: proceed or skip |
| TC-9004 | New | -- | Full triage | None -- proceed directly |
| TC-9010 | New | ai-cve-triaged | Re-triage or skip | Engineer decides: re-triage or skip |

### Status-to-Action Mapping (from SKILL.md)

| Status Category | Action |
|-----------------|--------|
| **New** | Proceed with full triage (default path) |
| **In Progress / Code Review / QA** | Warn: "This issue is already in `<status>`. It may be actively worked on." Ask engineer to proceed or skip. |
| **Closed / Done / Resolved** | Warn: "This issue is already closed." Ask engineer to re-triage or skip. |

In this discovery listing, only TC-9003 requires the In Progress warning. No issues are in Closed/Done/Resolved status.
