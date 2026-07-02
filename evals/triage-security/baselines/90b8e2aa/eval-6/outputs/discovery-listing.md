# Security Vulnerability Discovery — Project TC

## Step 0 — Configuration Validation

Extracted from CLAUDE.md Security Configuration:

| Parameter | Value |
|-----------|-------|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Vulnerability issue type ID | 10024 |
| Jira version prefix | RHTPA |
| Component label pattern | pscomponent: |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| VEX Justification custom field | customfield_12345 |

Version Streams: 2.1.x, 2.2.x

---

## Query 1: Untriaged Vulnerability Issues

**JQL:**
```
project = TC AND issuetype = 10024 AND labels NOT IN (ai-cve-triaged) ORDER BY status ASC, created DESC
```

**Results: 4 issues**

### Status: New (3 issues)

1. **TC-9001** — Status: New | CVE-2026-40112 | h2 - HTTP/2 rapid reset vulnerability [rhtpa-2.2] | Created: 2026-06-08
   - Component: pscomponent:org/rhtpa-server
2. **TC-9002** — Status: New | CVE-2026-40297 | serde_json - Stack overflow on deeply nested input [rhtpa-2.1] | Created: 2026-06-07
   - Component: pscomponent:org/rhtpa-server
3. **TC-9004** — Status: New | CVE-2026-40518 | ring - Timing side-channel in RSA verification [rhtpa-2.2] | Created: 2026-06-04
   - Component: pscomponent:org/rhtpa-server

### Status: In Progress (1 issue)

4. **TC-9003** — Status: In Progress | CVE-2026-40455 | tokio - Race condition in task cancellation [rhtpa-2.2] | Created: 2026-06-05
   - Component: pscomponent:org/rhtpa-server

---

## Query 2: Triaged but Still New (Stale Issues)

**JQL:**
```
project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status = New ORDER BY created DESC
```

These issues were previously triaged (carry the `ai-cve-triaged` label) but remain in New status — they may need follow-up or re-triage.

**Results: 1 issue**

1. **TC-9010** — Status: New | CVE-2026-39874 | quinn-proto - Panic on malformed QUIC frame [rhtpa-2.2] | Created: 2026-05-28
   - Component: pscomponent:org/rhtpa-server
   - Labels: CVE-2026-39874, pscomponent:org/rhtpa-server, ai-cve-triaged

---

## Query 3: Ready for QA Candidates

**JQL:**
```
project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status NOT IN (Closed, Verified, 'ON_QA') ORDER BY created DESC
```

For each result, linked Tasks with link type "Depend" were inspected to determine readiness:
- ALL linked remediation Tasks Done or Closed --> Ready for QA
- ANY linked Task still open --> Excluded (remediation in progress)
- NO linked Tasks with type "Depend" --> Excluded (no remediation to verify)

### Ready for QA

| Issue | Status | CVE | Summary | Created | Remediation Tasks |
|-------|--------|-----|---------|---------|-------------------|
| TC-9020 | Modified | CVE-2026-38901 | hyper - HTTP request smuggling [rhtpa-2.2] | 2026-05-15 | TC-9021 (Done), TC-9022 (Closed) |

Consider transitioning TC-9020 to ON_QA.

### Excluded from Ready for QA

| Issue | Status | CVE | Summary | Reason |
|-------|--------|-----|---------|--------|
| TC-9023 | In Progress | CVE-2026-39102 | rustls - Certificate validation bypass [rhtpa-2.1] | Remediation in progress: TC-9025 still In Progress |
| TC-9026 | Modified | CVE-2026-39330 | openssl - Buffer overflow in X.509 parsing [rhtpa-2.2] | No linked remediation Tasks with type "Depend" |

---

## Summary

| Category | Count |
|----------|-------|
| Untriaged issues | 4 |
| Triaged but still New (stale) | 1 |
| Ready for QA | 1 |
| Total issues discovered | 6 |

Select an issue key to begin triage, or specify an action for Ready for QA candidates.
