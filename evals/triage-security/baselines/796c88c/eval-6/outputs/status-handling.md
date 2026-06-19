# Status-Aware Handling Decisions

## From Query 1: Untriaged Issues

### TC-9001 - CVE-2026-40112 (h2 - HTTP/2 rapid reset vulnerability)
- **Status**: New
- **Decision**: Present for full triage. This issue is untriaged (no `ai-cve-triaged` label) and in New status, so it is eligible for complete CVE triage analysis including version-aware impact assessment, VEX justification, and disposition recommendation.

### TC-9002 - CVE-2026-40297 (serde_json - Stack overflow on deeply nested input)
- **Status**: New
- **Decision**: Present for full triage. This issue is untriaged (no `ai-cve-triaged` label) and in New status, so it is eligible for complete CVE triage analysis including version-aware impact assessment, VEX justification, and disposition recommendation.

### TC-9003 - CVE-2026-40455 (tokio - Race condition in task cancellation)
- **Status**: In Progress
- **Decision**: Warning -- active work in progress. This issue is currently In Progress, meaning someone is already working on it. It should NOT be presented for full triage. Instead, a warning should be raised that this issue has active work underway, and automated triage actions (label changes, status transitions, comment posting) should be skipped to avoid conflicting with the ongoing human effort.

### TC-9004 - CVE-2026-40518 (ring - Timing side-channel in RSA verification)
- **Status**: New
- **Decision**: Present for full triage. This issue is untriaged (no `ai-cve-triaged` label) and in New status, so it is eligible for complete CVE triage analysis including version-aware impact assessment, VEX justification, and disposition recommendation.

## From Query 2: Triaged but still New

### TC-9010 - CVE-2026-39874 (quinn-proto - Panic on malformed QUIC frame)
- **Status**: New (previously triaged)
- **Decision**: This issue was previously triaged (has `ai-cve-triaged` label) but remains in New status, indicating that prior triage did not result in a status change. It should be flagged for re-review -- the previous triage may need to be revisited, or the issue may require manual attention to determine why it was not moved out of New status after triage.

## Summary of Handling

| Issue Key | CVE ID | Status | Handling Decision |
|-----------|--------|--------|-------------------|
| TC-9001 | CVE-2026-40112 | New | Full triage |
| TC-9002 | CVE-2026-40297 | New | Full triage |
| TC-9003 | CVE-2026-40455 | In Progress | Warning: active work, skip triage |
| TC-9004 | CVE-2026-40518 | New | Full triage |
| TC-9010 | CVE-2026-39874 | New (triaged) | Re-review: still in New after prior triage |
