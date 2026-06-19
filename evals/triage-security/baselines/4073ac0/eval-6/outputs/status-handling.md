# Status-Aware Handling Decisions

Based on the discovery listing, the following status-aware handling applies to each issue per the triage-security skill's rules.

---

## Untriaged Issues (Query 1)

### TC-9001 — CVE-2026-40112 (h2 - HTTP/2 rapid reset vulnerability)
- **Status:** New
- **Handling:** Proceed with full triage (Steps 1-7). This is the default path for New issues. No warnings required.

### TC-9002 — CVE-2026-40297 (serde_json - Stack overflow on deeply nested input)
- **Status:** New
- **Handling:** Proceed with full triage (Steps 1-7). This is the default path for New issues. No warnings required.

### TC-9003 — CVE-2026-40455 (tokio - Race condition in task cancellation)
- **Status:** In Progress
- **Handling:** **Warning** — This issue is already in `In Progress`. It may be actively worked on. Before triaging, the engineer must be asked whether to:
  1. Proceed with triage anyway (e.g., to verify version impact or update Affects Versions)
  2. Skip this issue
- If the engineer chooses to skip, return to the discovery list or end the session.

### TC-9004 — CVE-2026-40518 (ring - Timing side-channel in RSA verification)
- **Status:** New
- **Handling:** Proceed with full triage (Steps 1-7). This is the default path for New issues. No warnings required.

---

## Triaged but still New (Query 2)

### TC-9010 — CVE-2026-39874 (quinn-proto - Panic on malformed QUIC frame)
- **Status:** New (but labeled `ai-cve-triaged`)
- **Handling:** This issue was previously triaged but has not progressed beyond New status. It may need follow-up or re-triage. If the engineer selects this issue, proceed with full triage (Steps 1-7) as its status is New. The existing `ai-cve-triaged` label indicates prior triage was completed but no action was taken — the engineer should review whether the original triage outcome still applies or if circumstances have changed.

---

## Summary Table

| Key | Status | Action |
|-----|--------|--------|
| TC-9001 | New | Ready for full triage |
| TC-9002 | New | Ready for full triage |
| TC-9003 | In Progress | **Requires warning** — ask engineer before proceeding |
| TC-9004 | New | Ready for full triage |
| TC-9010 | New (stale) | Ready for re-triage / follow-up |
