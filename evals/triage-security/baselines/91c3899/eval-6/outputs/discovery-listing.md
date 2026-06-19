# Discovery Mode: Vulnerability Issue Listing

## Configuration Used

- **Project key**: TC (from Jira Configuration)
- **Vulnerability issue type ID**: 10024 (from Security Configuration > Product Lifecycle)

---

## Query 1: Untriaged Issues

Issues that have not yet been triaged by the AI assistant (no `ai-cve-triaged` label).

**JQL Query**:
```
project = TC AND issuetype = 10024 AND labels NOT IN (ai-cve-triaged) ORDER BY status ASC, created DESC
```

**Results**: 4 issues

### Status: In Progress

| # | Issue Key | Status | CVE ID | Summary | Created |
|---|-----------|--------|--------|---------|---------|
| 1 | TC-9003 | In Progress | CVE-2026-40455 | tokio - Race condition in task cancellation [rhtpa-2.2] | 2026-06-05 |

### Status: New

| # | Issue Key | Status | CVE ID | Summary | Created |
|---|-----------|--------|--------|---------|---------|
| 2 | TC-9001 | New | CVE-2026-40112 | h2 - HTTP/2 rapid reset vulnerability [rhtpa-2.2] | 2026-06-08 |
| 3 | TC-9002 | New | CVE-2026-40297 | serde_json - Stack overflow on deeply nested input [rhtpa-2.1] | 2026-06-07 |
| 4 | TC-9004 | New | CVE-2026-40518 | ring - Timing side-channel in RSA verification [rhtpa-2.2] | 2026-06-04 |

---

## Query 2: Triaged but still New

Issues that were previously triaged (have `ai-cve-triaged` label) but remain in New status, indicating they may need follow-up or re-triage.

**JQL Query**:
```
project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status = New ORDER BY created DESC
```

**Results**: 1 issue

| # | Issue Key | Status | CVE ID | Summary | Created |
|---|-----------|--------|--------|---------|---------|
| 1 | TC-9010 | New | CVE-2026-39874 | quinn-proto - Panic on malformed QUIC frame [rhtpa-2.2] | 2026-05-28 |

> **Note**: These issues were previously triaged but never moved beyond New status. They may need follow-up action or re-triage to determine if remediation tasks were created and acted upon.

---

## Summary

- **Total untriaged issues**: 4
  - 3 in New status (ready for full triage)
  - 1 in In Progress status (requires caution -- may be actively worked on)
- **Triaged but stale issues**: 1
  - 1 in New status (previously triaged, never actioned)
