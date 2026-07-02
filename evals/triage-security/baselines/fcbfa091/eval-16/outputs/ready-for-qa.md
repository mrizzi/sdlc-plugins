# Ready for QA Filtering Analysis

## Query

```
project = TC AND issuetype = 10024 AND labels IN (ai-cve-triaged) AND status NOT IN (Closed, Verified, 'ON_QA') ORDER BY created DESC
```

This query finds triaged Vulnerability issues (`ai-cve-triaged` label present) that are not yet in a terminal or QA status. The results are then filtered by checking each issue's `issuelinks` for linked Tasks with link type "Depend".

## Filtering Criteria

An issue qualifies as "Ready for QA" only when:

1. **ALL** linked remediation Tasks (link type "Depend") have status Done or Closed.
2. At least one Depend-type linked Task exists (issues with no Depend links are excluded because there is no remediation to verify).

## Candidates Evaluated

### TC-9020 — CVE-2026-38901 hyper - HTTP request smuggling [rhtpa-2.2]

- **Status**: Modified
- **Linked remediation Tasks (Depend)**:
  - TC-9021 (Task) — **Done**
  - TC-9022 (Task) — **Closed**
- **Assessment**: All 2 linked remediation Tasks are in a completed state (Done or Closed).
- **Result**: **INCLUDED** — Ready for QA. Consider transitioning to ON_QA.

### TC-9023 — CVE-2026-39102 rustls - Certificate validation bypass [rhtpa-2.1]

- **Status**: In Progress
- **Linked remediation Tasks (Depend)**:
  - TC-9024 (Task) — **Done**
  - TC-9025 (Task) — **In Progress**
- **Assessment**: TC-9025 is still In Progress. Not all linked remediation Tasks are completed.
- **Result**: **EXCLUDED** — Remediation is still in progress. TC-9025 must reach Done or Closed before this issue qualifies.

### TC-9026 — CVE-2026-39330 openssl - Buffer overflow in X.509 parsing [rhtpa-2.2]

- **Status**: Modified
- **Linked remediation Tasks (Depend)**: None
- **Assessment**: No Depend-type issue links found. Without linked remediation Tasks, there is no remediation work to verify.
- **Result**: **EXCLUDED** — No Depend links. This issue may need remediation tasks created before it can proceed to QA.

## Summary

| Issue | CVE | Status | Depend Links | All Complete? | Ready for QA? |
|-------|-----|--------|--------------|---------------|---------------|
| TC-9020 | CVE-2026-38901 | Modified | TC-9021 (Done), TC-9022 (Closed) | Yes | Yes |
| TC-9023 | CVE-2026-39102 | In Progress | TC-9024 (Done), TC-9025 (In Progress) | No | No |
| TC-9026 | CVE-2026-39330 | Modified | (none) | N/A | No |

## Recommended Action

**TC-9020**: Transition to ON_QA. All remediation tasks are complete and the fix is ready for QA verification.
