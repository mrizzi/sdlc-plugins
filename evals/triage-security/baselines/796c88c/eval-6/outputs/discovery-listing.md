# CVE Discovery Mode - Issue Listing

## Security Configuration Used

- **Project key**: TC
- **Vulnerability issue type ID**: 10024

---

## Query 1: Untriaged Issues

**JQL**:
```
project = TC AND issuetype = 10024 AND labels NOT IN (ai-cve-triaged) ORDER BY status ASC, created DESC
```

**Results** (4 issues):

### Status: New

| Issue Key | Status | CVE ID | Summary | Created |
|-----------|--------|--------|---------|---------|
| TC-9001 | New | CVE-2026-40112 | h2 - HTTP/2 rapid reset vulnerability [rhtpa-2.2] | 2026-06-08 |
| TC-9002 | New | CVE-2026-40297 | serde_json - Stack overflow on deeply nested input [rhtpa-2.1] | 2026-06-07 |
| TC-9004 | New | CVE-2026-40518 | ring - Timing side-channel in RSA verification [rhtpa-2.2] | 2026-06-04 |

### Status: In Progress

| Issue Key | Status | CVE ID | Summary | Created |
|-----------|--------|--------|---------|---------|
| TC-9003 | In Progress | CVE-2026-40455 | tokio - Race condition in task cancellation [rhtpa-2.2] | 2026-06-05 |

---

## Query 2: Triaged but still New

**JQL**:
```
project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status = New ORDER BY created DESC
```

**Results** (1 issue):

| Issue Key | Status | CVE ID | Summary | Created |
|-----------|--------|--------|---------|---------|
| TC-9010 | New | CVE-2026-39874 | quinn-proto - Panic on malformed QUIC frame [rhtpa-2.2] | 2026-05-28 |

---

## Summary

- **Total untriaged issues**: 4 (3 New, 1 In Progress)
- **Previously triaged but still in New status**: 1
- **Grand total requiring attention**: 5
