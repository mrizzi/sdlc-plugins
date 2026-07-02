# Security Vulnerability Discovery — Project TC

**Project key:** TC
**Vulnerability issue type ID:** 10024
**Date:** 2026-07-02

---

## Step 0 — Validate Project Configuration

Configuration validated from CLAUDE.md:

| Setting | Value |
|---------|-------|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Component label pattern | pscomponent: |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| VEX Justification custom field | customfield_12345 |

Version Streams: 2.1.x, 2.2.x
Source Repositories: rhtpa-backend

---

## Untriaged Issues (4 issues)

Issues with `issuetype = 10024` and **without** the `ai-cve-triaged` label, ordered by status then created date descending.

### In Progress

1. **TC-9003** | In Progress | CVE-2026-40455 | tokio - Race condition in task cancellation [rhtpa-2.2] | Created: 2026-06-05

### New

2. **TC-9001** | New | CVE-2026-40112 | h2 - HTTP/2 rapid reset vulnerability [rhtpa-2.2] | Created: 2026-06-08
3. **TC-9002** | New | CVE-2026-40297 | serde_json - Stack overflow on deeply nested input [rhtpa-2.1] | Created: 2026-06-07
4. **TC-9004** | New | CVE-2026-40518 | ring - Timing side-channel in RSA verification [rhtpa-2.2] | Created: 2026-06-04

---

## Triaged but still New (1 issue)

Issues with `issuetype = 10024` that carry the `ai-cve-triaged` label but remain in **New** status. These were triaged but never moved forward and may need follow-up or re-triage.

### New

1. **TC-9010** | New | CVE-2026-39874 | quinn-proto - Panic on malformed QUIC frame [rhtpa-2.2] | Created: 2026-05-28

---

## Ready for QA (1 issue)

Triaged CVEs with all linked remediation tasks completed. These are candidates for transition to ON_QA.

| Issue | Status | CVE | Summary | Created | Remediation Tasks |
|-------|--------|-----|---------|---------|-------------------|
| TC-9020 | Modified | CVE-2026-38901 | hyper - HTTP request smuggling [rhtpa-2.2] | 2026-05-15 | TC-9021 (Done), TC-9022 (Closed) |

**TC-9020**: All linked remediation Tasks are complete. Consider transitioning to ON_QA.

### Excluded from Ready for QA

- **TC-9023** (CVE-2026-39102, rustls - Certificate validation bypass [rhtpa-2.1]): Excluded -- TC-9025 is still In Progress. Remediation is not yet complete.
- **TC-9026** (CVE-2026-39330, openssl - Buffer overflow in X.509 parsing [rhtpa-2.2]): Excluded -- no linked Tasks with type "Depend". No remediation to verify.

---

## Summary

| Category | Count |
|----------|-------|
| Untriaged | 4 |
| Triaged but still New | 1 |
| Ready for QA | 1 |
| **Total open Vulnerability issues** | **6** |

To triage a specific issue, run: `/sdlc-workflow:triage-security TC-XXXX`
