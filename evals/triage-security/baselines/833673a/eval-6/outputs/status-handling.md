# Status-Aware Handling Decisions

Per the triage-security skill's status-aware handling rules, here is the handling decision for each discovered issue based on its current Jira status.

---

## Query 1: Untriaged Issues

### TC-9003 -- CVE-2026-40455 tokio (Status: In Progress)

**Handling**: Warn before proceeding.

This issue is already in `In Progress`. It may be actively worked on. Before triaging, the engineer would be asked:

1. **Proceed with triage anyway** -- e.g., to verify version impact or update Affects Versions
2. **Skip this issue**

If the user chooses to skip, return to the discovery list or end the session.

---

### TC-9001 -- CVE-2026-40112 h2 (Status: New)

**Handling**: Proceed with full triage (default path).

Status is `New`, which is the standard entry point. Full 7-step triage would be executed: data extraction, version impact analysis, Affects Versions correction, duplicate/sibling check, version lifecycle check, already fixed check, and remediation.

---

### TC-9002 -- CVE-2026-40297 serde_json (Status: New)

**Handling**: Proceed with full triage (default path).

Status is `New`, which is the standard entry point. Full 7-step triage would be executed.

---

### TC-9004 -- CVE-2026-40518 ring (Status: New)

**Handling**: Proceed with full triage (default path).

Status is `New`, which is the standard entry point. Full 7-step triage would be executed.

---

## Query 2: Triaged but still New

### TC-9010 -- CVE-2026-39874 quinn-proto (Status: New, Label: ai-cve-triaged)

**Handling**: Proceed with full triage (default path), but note this is a re-triage.

Status is `New` and the issue has the `ai-cve-triaged` label, meaning it was previously triaged but never moved forward. This issue appears in the "Triaged but still New" list specifically to flag it for follow-up. If selected, full triage would proceed to verify whether the original triage outcome is still valid or if conditions have changed.

---

## Summary

| Key | Status | Handling Decision |
|------|--------|-------------------|
| TC-9003 | In Progress | Warn: may be actively worked on. Ask engineer to proceed or skip. |
| TC-9001 | New | Full triage (default path) |
| TC-9002 | New | Full triage (default path) |
| TC-9004 | New | Full triage (default path) |
| TC-9010 | New (previously triaged) | Full triage / re-triage. Flagged as stale -- triaged but never actioned. |
