# Status-Aware Handling Decisions

For each issue surfaced in discovery mode, the following status-aware handling applies per the triage-security skill protocol.

---

## Untriaged Issues (Query 1)

### TC-9001 — Status: New
- **Handling:** Proceed with full triage (default path).
- **Action:** Ready for selection. Running `/triage-security TC-9001` will execute the complete 8-step triage workflow starting from Step 0.

### TC-9002 — Status: New
- **Handling:** Proceed with full triage (default path).
- **Action:** Ready for selection. Running `/triage-security TC-9002` will execute the complete 8-step triage workflow starting from Step 0.

### TC-9003 — Status: In Progress
- **Handling:** Warning required. This issue is already in `In Progress` status. It may be actively worked on.
- **Action:** If selected, the engineer will be prompted:
  > "This issue is already in `In Progress`. It may be actively worked on."
  > 1. Proceed with triage anyway (e.g., to verify version impact or update Affects Versions)
  > 2. Skip this issue
- **Note:** The engineer must explicitly choose before triage proceeds. If skipped, return to the discovery list.

### TC-9004 — Status: New
- **Handling:** Proceed with full triage (default path).
- **Action:** Ready for selection. Running `/triage-security TC-9004` will execute the complete 8-step triage workflow starting from Step 0.

---

## Triaged but still New (Query 2)

### TC-9010 — Status: New
- **Handling:** Proceed with full triage (default path). Status is New so no warning is required.
- **Action:** This issue was previously triaged (`ai-cve-triaged` label present) but never moved beyond New status. It may need follow-up or re-triage to determine why it stalled. Running `/triage-security TC-9010` will re-execute the triage workflow, which may update version impact analysis or remediation tasks.

---

## Ready for QA Candidates (Query 3)

### TC-9020 — Status: Modified
- **Handling:** No triage warning (Modified is not a warning-triggering status for selection).
- **Action:** All linked remediation tasks are complete (TC-9021 Done, TC-9022 Closed). Consider transitioning to ON_QA. If the engineer selects this issue for triage, the full workflow runs; however, the primary recommended action is the ON_QA transition since remediation is complete.

### TC-9023 — Status: In Progress
- **Handling:** Warning required. This issue is already in `In Progress` status.
- **Action:** Excluded from Ready for QA list because TC-9025 is still In Progress. If selected for triage, the engineer will be warned that the issue is actively being worked on and asked to choose between proceeding with triage or skipping.

### TC-9026 — Status: Modified
- **Handling:** No triage warning (Modified is not a warning-triggering status for selection).
- **Action:** Excluded from Ready for QA list because it has no linked Tasks with link type "Depend". There is no remediation work to verify. This may indicate remediation tasks were never created, or were linked with a different link type. The engineer should investigate whether remediation tasks need to be created.
