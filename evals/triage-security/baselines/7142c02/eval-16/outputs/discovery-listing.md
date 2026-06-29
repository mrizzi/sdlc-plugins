# Security Vulnerability Discovery — Project TC

## Configuration Validated

- Project key: TC
- Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- Vulnerability issue type ID: 10024
- Component label pattern: pscomponent:
- Jira version prefix: RHTPA
- Product pages URL: https://access.example.com/product-life-cycle/rhtpa
- VEX Justification custom field: customfield_12345

---

## Untriaged Vulnerability Issues (4 issues)

Issues without the `ai-cve-triaged` label, ordered by status then created date.

### New (3 issues)

1. **TC-9001** | New | CVE-2026-40112 | h2 - HTTP/2 rapid reset vulnerability [rhtpa-2.2] | Created: 2026-06-08
2. **TC-9002** | New | CVE-2026-40297 | serde_json - Stack overflow on deeply nested input [rhtpa-2.1] | Created: 2026-06-07
3. **TC-9004** | New | CVE-2026-40518 | ring - Timing side-channel in RSA verification [rhtpa-2.2] | Created: 2026-06-04

### In Progress (1 issue)

4. **TC-9003** | In Progress | CVE-2026-40455 | tokio - Race condition in task cancellation [rhtpa-2.2] | Created: 2026-06-05

---

## Triaged but still New (1 issue)

These issues have been triaged (`ai-cve-triaged` label present) but remain in New status. They may need follow-up or re-triage.

1. **TC-9010** | New | CVE-2026-39874 | quinn-proto - Panic on malformed QUIC frame [rhtpa-2.2] | Created: 2026-05-28

---

## Ready for QA (1 issue)

Triaged CVEs where all linked remediation Tasks (Depend link type) are completed (Done or Closed). These are candidates for transition to ON_QA.

| Issue | Status | CVE | Summary | Created | Remediation Tasks |
|-------|--------|-----|---------|---------|-------------------|
| TC-9020 | Modified | CVE-2026-38901 | hyper - HTTP request smuggling [rhtpa-2.2] | 2026-05-15 | TC-9021 (Done), TC-9022 (Closed) |

**Recommendation for TC-9020**: Consider transitioning to ON_QA. All linked remediation Tasks have been completed.

### Excluded from Ready for QA

- **TC-9023** (CVE-2026-39102, rustls - Certificate validation bypass [rhtpa-2.1]) — Excluded: TC-9025 is still In Progress. Remediation is not yet complete.
- **TC-9026** (CVE-2026-39330, openssl - Buffer overflow in X.509 parsing [rhtpa-2.2]) — Excluded: No linked Tasks with Depend link type. No remediation to verify.

---

To triage a specific issue, re-invoke with the issue key: `/sdlc-workflow:triage-security TC-XXXX`
