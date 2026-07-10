# Security Vulnerability Discovery — Project TC

**Project key:** TC
**Vulnerability issue type ID:** 10024
**Date:** 2026-07-10

---

## Untriaged Issues

4 Vulnerability issues awaiting triage (no `ai-cve-triaged` label):

### Status: New

1. **TC-9001** | New | CVE-2026-40112 | h2 - HTTP/2 rapid reset vulnerability [rhtpa-2.2] | Created: 2026-06-08
2. **TC-9002** | New | CVE-2026-40297 | serde_json - Stack overflow on deeply nested input [rhtpa-2.1] | Created: 2026-06-07
3. **TC-9004** | New | CVE-2026-40518 | ring - Timing side-channel in RSA verification [rhtpa-2.2] | Created: 2026-06-04

### Status: In Progress

4. **TC-9003** | In Progress | CVE-2026-40455 | tokio - Race condition in task cancellation [rhtpa-2.2] | Created: 2026-06-05

---

## Triaged but still New

1 issue has been triaged (`ai-cve-triaged` label) but remains in New status. These may need follow-up or re-triage:

1. **TC-9010** | New | CVE-2026-39874 | quinn-proto - Panic on malformed QUIC frame [rhtpa-2.2] | Created: 2026-05-28

---

## Ready for QA

Triaged CVEs where all linked remediation Tasks (link type "Depend") are completed (Done or Closed). These are candidates for ON_QA transition.

| Issue | Status | CVE | Summary | Created | Remediation Tasks |
|-------|--------|-----|---------|---------|-------------------|
| TC-9020 | Modified | CVE-2026-38901 | hyper - HTTP request smuggling [rhtpa-2.2] | 2026-05-15 | TC-9021 (Done), TC-9022 (Closed) |

**1 issue ready for QA.** Consider transitioning TC-9020 to ON_QA.

---

To triage a specific issue, run: `/sdlc-workflow:triage-security <issue-key>`
