# Security Vulnerability Discovery Listing

Project: **TC** | Vulnerability Issue Type ID: **10024**

---

## Query 1: Untriaged Issues

**JQL:**
```
project = TC AND issuetype = 10024 AND labels NOT IN (ai-cve-triaged) ORDER BY status ASC, created DESC
```

**Results: 4 issues**

### Status: New (3 issues)

| # | Key | Status | CVE ID | Summary | Created |
|---|-----|--------|--------|---------|---------|
| 1 | TC-9001 | New | CVE-2026-40112 | h2 - HTTP/2 rapid reset vulnerability [rhtpa-2.2] | 2026-06-08 |
| 2 | TC-9002 | New | CVE-2026-40297 | serde_json - Stack overflow on deeply nested input [rhtpa-2.1] | 2026-06-07 |
| 3 | TC-9004 | New | CVE-2026-40518 | ring - Timing side-channel in RSA verification [rhtpa-2.2] | 2026-06-04 |

### Status: In Progress (1 issue)

| # | Key | Status | CVE ID | Summary | Created |
|---|-----|--------|--------|---------|---------|
| 4 | TC-9003 | In Progress | CVE-2026-40455 | tokio - Race condition in task cancellation [rhtpa-2.2] | 2026-06-05 |

---

## Query 2: Triaged but still New

**JQL:**
```
project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status = New ORDER BY created DESC
```

**Results: 1 issue**

These issues were previously triaged (carry the `ai-cve-triaged` label) but remain in **New** status -- they may need follow-up or re-triage.

| # | Key | Status | CVE ID | Summary | Created |
|---|-----|--------|--------|---------|---------|
| 1 | TC-9010 | New | CVE-2026-39874 | quinn-proto - Panic on malformed QUIC frame [rhtpa-2.2] | 2026-05-28 |

---

## Summary

- **4** untriaged Vulnerability issues awaiting triage
- **1** previously triaged issue still in New status (potential stale issue)
- All issues target the **rhtpa-backend** component (`pscomponent:org/rhtpa-server`)
- Stream coverage: 3 issues target stream **2.2.x**, 1 issue targets stream **2.1.x**
