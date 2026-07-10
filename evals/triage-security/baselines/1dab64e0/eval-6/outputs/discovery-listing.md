# Discovery Mode — Vulnerability Issue Listing

## Configuration Used

| Parameter | Value |
|-----------|-------|
| Project key | TC |
| Vulnerability issue type ID | 10024 |
| Jira version prefix | RHTPA |
| Component label pattern | pscomponent: |
| VEX Justification custom field | customfield_12345 |

---

## Query 1: Untriaged Issues

**JQL:**
```
project = TC AND issuetype = 10024 AND labels NOT IN (ai-cve-triaged) ORDER BY status ASC, created DESC
```

**Results: 4 issues**

### Status: New (3 issues)

1. **TC-9001** — New — CVE-2026-40112 — h2 - HTTP/2 rapid reset vulnerability [rhtpa-2.2] — Created: 2026-06-08
2. **TC-9002** — New — CVE-2026-40297 — serde_json - Stack overflow on deeply nested input [rhtpa-2.1] — Created: 2026-06-07
3. **TC-9004** — New — CVE-2026-40518 — ring - Timing side-channel in RSA verification [rhtpa-2.2] — Created: 2026-06-04

### Status: In Progress (1 issue)

4. **TC-9003** — In Progress — CVE-2026-40455 — tokio - Race condition in task cancellation [rhtpa-2.2] — Created: 2026-06-05

---

## Query 2: Triaged but still New

**JQL:**
```
project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status = New ORDER BY created DESC
```

**Results: 1 issue**

### Status: New (1 issue)

1. **TC-9010** — New — CVE-2026-39874 — quinn-proto - Panic on malformed QUIC frame [rhtpa-2.2] — Created: 2026-05-28

This issue was previously triaged (has `ai-cve-triaged` label) but remains in New status. It may need follow-up or re-triage.

---

## Query 3: Ready for QA Candidates

**JQL:**
```
project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status NOT IN (Closed, Verified, 'ON_QA') ORDER BY created DESC
```

**Results: 3 issues evaluated, 1 ready for QA**

### Ready for QA (1 issue)

| Issue | Status | CVE | Summary | Created | Remediation Tasks |
|-------|--------|-----|---------|---------|-------------------|
| TC-9020 | Modified | CVE-2026-38901 | hyper - HTTP request smuggling [rhtpa-2.2] | 2026-05-15 | TC-9021 (Done), TC-9022 (Closed) |

All linked remediation Tasks (Depend links) are completed. Consider transitioning TC-9020 to ON_QA.

### Excluded from Ready for QA (2 issues)

| Issue | Status | CVE | Summary | Exclusion Reason |
|-------|--------|-----|---------|------------------|
| TC-9023 | In Progress | CVE-2026-39102 | rustls - Certificate validation bypass [rhtpa-2.1] | Remediation in progress: TC-9025 still In Progress (TC-9024 Done) |
| TC-9026 | Modified | CVE-2026-39330 | openssl - Buffer overflow in X.509 parsing [rhtpa-2.2] | No linked Tasks with type "Depend" — no remediation to verify |
