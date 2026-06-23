# Discovery Mode: Untriaged Vulnerability Issues

**Project**: TC
**Vulnerability issue type ID**: 10024
**Jira version prefix**: RHTPA
**Component label pattern**: pscomponent:

---

## Query 1: Untriaged Issues

**JQL**:
```
project = TC AND issuetype = 10024 AND labels NOT IN (ai-cve-triaged) ORDER BY status ASC, created DESC
```

4 issues found, grouped by status:

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

**JQL**:
```
project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status = New ORDER BY created DESC
```

1 issue found:

| # | Issue Key | Status | CVE ID | Summary | Created |
|---|-----------|--------|--------|---------|---------|
| 1 | TC-9010 | New | CVE-2026-39874 | quinn-proto - Panic on malformed QUIC frame [rhtpa-2.2] | 2026-05-28 |

This issue was previously triaged (has `ai-cve-triaged` label) but remains in New status. It may need follow-up or re-triage to determine why it was never actioned.

---

## Summary

- **4 untriaged issues** awaiting initial triage (3 New, 1 In Progress)
- **1 triaged-but-stale issue** that was triaged but never moved past New status
- All issues are associated with component `pscomponent:org/rhtpa-server`
- Stream distribution: 3 issues scoped to stream 2.2.x (`[rhtpa-2.2]`), 1 issue scoped to stream 2.1.x (`[rhtpa-2.1]`)

Select an issue key to begin full triage, or provide a specific issue key to proceed.
