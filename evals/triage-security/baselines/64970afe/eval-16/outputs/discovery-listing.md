# Security Vulnerability Discovery — Project TC

## Configuration

- **Project key**: TC
- **Vulnerability issue type ID**: 10024
- **Jira version prefix**: RHTPA
- **Component label pattern**: `pscomponent:`

---

## Untriaged Vulnerability Issues

4 issues found — not yet triaged (missing `ai-cve-triaged` label).

### Status: New (3 issues)

| # | Issue | Status | CVE | Summary | Created |
|---|-------|--------|-----|---------|---------|
| 1 | TC-9001 | New | CVE-2026-40112 | h2 - HTTP/2 rapid reset vulnerability [rhtpa-2.2] | 2026-06-08 |
| 2 | TC-9002 | New | CVE-2026-40297 | serde_json - Stack overflow on deeply nested input [rhtpa-2.1] | 2026-06-07 |
| 3 | TC-9004 | New | CVE-2026-40518 | ring - Timing side-channel in RSA verification [rhtpa-2.2] | 2026-06-04 |

### Status: In Progress (1 issue)

| # | Issue | Status | CVE | Summary | Created |
|---|-------|--------|-----|---------|---------|
| 4 | TC-9003 | In Progress | CVE-2026-40455 | tokio - Race condition in task cancellation [rhtpa-2.2] | 2026-06-05 |

---

## Triaged but Still New

1 issue found — previously triaged (`ai-cve-triaged` label present) but still in New status. These may need follow-up or re-triage.

| # | Issue | Status | CVE | Summary | Created |
|---|-------|--------|-----|---------|---------|
| 1 | TC-9010 | New | CVE-2026-39874 | quinn-proto - Panic on malformed QUIC frame [rhtpa-2.2] | 2026-05-28 |

---

## Ready for QA

Triaged CVEs where all linked remediation Tasks are completed (Done or Closed). These are candidates for transition to ON_QA.

| Issue | Status | CVE | Summary | Created | Remediation Tasks |
|-------|--------|-----|---------|---------|-------------------|
| TC-9020 | Modified | CVE-2026-38901 | hyper - HTTP request smuggling [rhtpa-2.2] | 2026-05-15 | TC-9021 (Done), TC-9022 (Closed) |

> Consider transitioning TC-9020 to ON_QA.

**Excluded from Ready for QA:**
- **TC-9023** (CVE-2026-39102): TC-9025 still In Progress — remediation in progress.
- **TC-9026** (CVE-2026-39330): No linked Tasks with type "Depend" — no remediation to verify.

---

To triage an issue, invoke: `/sdlc-workflow:triage-security <issue-key>`
