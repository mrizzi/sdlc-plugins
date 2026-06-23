# Status-Aware Handling Decisions

Per SKILL.md "Status-aware handling" (Discovery Mode), each issue's current Jira status determines how triage should proceed. Below are the handling decisions for every issue returned from both discovery queries.

---

## Query 1: Untriaged Issues

### TC-9001 -- CVE-2026-40112 h2 - HTTP/2 rapid reset vulnerability [rhtpa-2.2]

- **Current Status**: New
- **Handling Decision**: Proceed with full triage (Steps 1-7)
- **Rationale**: Status is "New" -- this is the default triage path. No warnings or special handling required.
- **Stream Scope**: 2.2.x (from summary suffix `[rhtpa-2.2]`, maps to Version Stream `2.2.x` with Konflux release repo `git.example.com/rhtpa/rhtpa-release.0.4.z`)
- **Ecosystem**: Cargo (h2 is a Rust crate)

### TC-9002 -- CVE-2026-40297 serde_json - Stack overflow on deeply nested input [rhtpa-2.1]

- **Current Status**: New
- **Handling Decision**: Proceed with full triage (Steps 1-7)
- **Rationale**: Status is "New" -- this is the default triage path. No warnings or special handling required.
- **Stream Scope**: 2.1.x (from summary suffix `[rhtpa-2.1]`, maps to Version Stream `2.1.x` with Konflux release repo `git.example.com/rhtpa/rhtpa-release.0.3.z`)
- **Ecosystem**: Cargo (serde_json is a Rust crate)

### TC-9003 -- CVE-2026-40455 tokio - Race condition in task cancellation [rhtpa-2.2]

- **Current Status**: In Progress
- **Handling Decision**: Warn before proceeding
- **Rationale**: Status is "In Progress" -- this issue may be actively worked on. Per the SKILL.md status-aware handling rules, the engineer must be warned:

  > "This issue is already in `In Progress`. It may be actively worked on."

  The engineer should be asked whether to:
  1. **Proceed with triage anyway** -- e.g., to verify version impact or update Affects Versions even though someone is already working on it
  2. **Skip this issue** -- defer to the person currently working on it

  If the engineer chooses to skip, return to the discovery list or end the session.
- **Stream Scope**: 2.2.x (from summary suffix `[rhtpa-2.2]`, maps to Version Stream `2.2.x`)
- **Ecosystem**: Cargo (tokio is a Rust crate)

### TC-9004 -- CVE-2026-40518 ring - Timing side-channel in RSA verification [rhtpa-2.2]

- **Current Status**: New
- **Handling Decision**: Proceed with full triage (Steps 1-7)
- **Rationale**: Status is "New" -- this is the default triage path. No warnings or special handling required.
- **Stream Scope**: 2.2.x (from summary suffix `[rhtpa-2.2]`, maps to Version Stream `2.2.x` with Konflux release repo `git.example.com/rhtpa/rhtpa-release.0.4.z`)
- **Ecosystem**: Cargo (ring is a Rust crate)

---

## Query 2: Triaged but still New

### TC-9010 -- CVE-2026-39874 quinn-proto - Panic on malformed QUIC frame [rhtpa-2.2]

- **Current Status**: New
- **Labels**: Includes `ai-cve-triaged` (previously triaged)
- **Handling Decision**: Proceed with full triage (Steps 1-7) -- status is "New" so no warning is required
- **Rationale**: Although this issue has the `ai-cve-triaged` label (indicating it was previously triaged), its status remains "New" -- it was never moved forward. This is a stale triaged issue. The status-aware handling rules apply based on current Jira status, and "New" means full triage is the default path. However, the engineer should be informed that this issue was previously triaged and may need re-triage or follow-up to understand why it stalled:

  > "This issue was previously triaged (ai-cve-triaged label present, created 2026-05-28) but remains in New status. It may need re-triage or follow-up to determine why remediation was not started."

  Possible reasons for stalling:
  - Previous triage determined no fix was needed but the issue was not closed
  - Remediation tasks were created but the vulnerability issue was not transitioned
  - The triage was incomplete or interrupted

  The engineer may choose to:
  1. **Re-triage** -- run the full triage process again to verify findings and complete any missing steps
  2. **Skip** -- if the original triage outcome is known and the situation is understood

- **Stream Scope**: 2.2.x (from summary suffix `[rhtpa-2.2]`, maps to Version Stream `2.2.x`)
- **Ecosystem**: Cargo (quinn-proto is a Rust crate)

---

## Summary of Handling Decisions

| Issue Key | Status | Handling | Action Required |
|-----------|--------|----------|-----------------|
| TC-9001 | New | Full triage | None -- proceed directly |
| TC-9002 | New | Full triage | None -- proceed directly |
| TC-9003 | In Progress | Warn + ask engineer | Engineer must confirm: proceed with triage or skip |
| TC-9004 | New | Full triage | None -- proceed directly |
| TC-9010 | New (stale triaged) | Full triage / re-triage | Inform engineer of prior triage; confirm re-triage or skip |

### Status handling rules reference (from SKILL.md):

| Status | Action |
|--------|--------|
| **New** | Proceed with full triage (default path) |
| **In Progress / Code Review / QA** | Warn: "This issue is already in `<status>`. It may be actively worked on." Ask to proceed or skip. |
| **Closed / Done / Resolved** | Warn: "This issue is already closed." Ask to re-triage or skip. |
