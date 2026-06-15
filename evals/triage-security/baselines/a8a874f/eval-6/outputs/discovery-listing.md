# Discovery Mode — Issue Listing

## Project Configuration (from Security Configuration)

- Project: TC
- Vulnerability issue type ID: 10024

---

## Query 1: Untriaged Issues

**JQL**: `project = TC AND issuetype = 10024 AND labels NOT IN (ai-cve-triaged) ORDER BY status ASC, created DESC`

**Results** (4 issues):

| Key | Status | CVE ID | Summary | Created |
|-----|--------|--------|---------|---------|
| TC-9001 | New | CVE-2026-40112 | h2 - HTTP/2 rapid reset vulnerability [rhtpa-2.2] | 2026-06-08 |
| TC-9002 | New | CVE-2026-40297 | serde_json - Stack overflow on deeply nested input [rhtpa-2.1] | 2026-06-07 |
| TC-9003 | In Progress | CVE-2026-40455 | tokio - Race condition in task cancellation [rhtpa-2.2] | 2026-06-05 |
| TC-9004 | New | CVE-2026-40518 | ring - Timing side-channel in RSA verification [rhtpa-2.2] | 2026-06-04 |

---

## Query 2: Triaged but still New

**JQL**: `project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status = New ORDER BY created DESC`

**Results** (1 issue):

| Key | Status | CVE ID | Summary | Created |
|-----|--------|--------|---------|---------|
| TC-9010 | New | CVE-2026-39874 | quinn-proto - Panic on malformed QUIC frame [rhtpa-2.2] | 2026-05-28 |
