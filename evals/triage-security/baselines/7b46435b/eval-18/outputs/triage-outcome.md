# Triage Outcome: TC-8001 Re-Run Produces No New Mutations

## Context

TC-8001 (CVE-2026-31812, quinn-proto panic on large stream counts, scoped to stream rhtpa-2.2) was fully triaged in a prior run on 2026-07-01. This document explains why the second invocation of `/sdlc-workflow:triage-security` on the same issue produces zero new Jira mutations.

## Why No New Mutations

The triage-security skill is designed to be idempotent across re-runs. Each step checks for the presence of its expected output before performing mutations. When a prior run has already completed all steps, the re-run walks through the same step sequence but finds every artifact already in place, resulting in no new writes to Jira.

### Step-by-Step Re-Run Trace

| Step | Name | Re-Run Behavior | Mutation? |
|------|------|-----------------|-----------|
| 0 | Validate Configuration | Reads CLAUDE.md, extracts Security Configuration. Pure read. | No |
| 0.3 | Matrix Staleness Check | Reads security-matrix.md timestamps. Pure read. | No |
| 0.5 | Jira Access | Initializes MCP or REST API connection. Pure setup. | No |
| 0.7 | Assign and Transition | Issue is already In Progress (past Assigned). Assignment may re-assert current user but status transition is skipped. | No (or idempotent assignment) |
| 1 | Data Extraction | Fetches issue fields and remote links. Pure read. Extracts same CVE data as before. | No |
| 1.5 | External CVE Enrichment | Queries MITRE and OSV.dev APIs. Pure read. | No |
| 1.7 | Embargo Check | CVSS 7.5 triggers the gate, but no embargo policy URL is configured in the mock CLAUDE.md, so this step is skipped. | No |
| 2 | Version Impact Analysis | Reads security-matrix.md and lock file data. Produces same version impact table as before. Pure read. | No |
| 3 | Affects Versions Correction | Current Affects Versions (RHTPA 2.2.0, RHTPA 2.2.1) already match the version impact table for the scoped stream 2.2.x. No correction needed. | No |
| 4 | Duplicate/Sibling/Overlap Check | Searches for sibling CVEs, cross-CVE overlap, and preemptive tasks. Read-only queries. Any Related links that would be created already exist (idempotent link check). | No |
| 5 | Version Lifecycle Check | Fetches product lifecycle page. Pure read. Affected versions are still supported. | No |
| 6 | Already Fixed Check | Checks resolved siblings. No resolved siblings with full coverage detected. Pure read. | No |
| 7 | Concurrent Triage Detection | Searches for in-progress triages on same component. Pure read. | No |
| 8 | Remediation (Case A) | Existing Depend links to TC-8100 and TC-8101 are detected in the issue's issuelinks array. The skill recognizes that remediation tasks already exist for the scoped stream. Task creation is skipped entirely. | No |
| Post-Triage: ai-cve-triaged label | Label already present in the issue's Labels field. Adding it again would be a no-op. Skipped. | No |
| Post-Triage: Summary comment | A post-triage summary comment already exists (posted 2026-07-01T10:01:00Z). Re-posting would produce a duplicate. Skipped. | No |
| Post-Triage: Description digest | A description digest comment already exists (posted 2026-07-01T10:00:00Z). The description has not changed, so the digest would be identical. Skipped. | No |

### Total mutations on re-run: **0**

## Idempotency Mechanisms

The skill achieves idempotency through these mechanisms:

1. **Label presence check**: The `ai-cve-triaged` label acts as a triage-complete marker. Its presence signals that the full triage workflow completed previously.

2. **Status-aware transitions**: Step 0.7 only transitions when the issue is in New status. An issue already in In Progress or later statuses skips the transition.

3. **Link existence checks**: Before creating any Jira link (Depend, Related, Blocks), the skill inspects the issue's existing `issuelinks` array. If a link of the same type to the same target already exists, creation is skipped with a log message.

4. **Affects Versions comparison**: Step 3 compares the current Affects Versions against the version impact table. When they already match, no correction is proposed.

5. **Remediation task detection**: Step 8 checks for existing Depend-linked remediation tasks before creating new ones. If tasks for the scoped stream already exist, creation is skipped entirely.

6. **Comment deduplication**: The description digest and post-triage summary comments are recognized by their structured markers (e.g., `[sdlc-workflow] Description digest:` prefix). Existing comments prevent duplicate posting.

## Conclusion

The second triage run on TC-8001 is a pure verification pass. It re-derives the same version impact analysis, confirms all triage artifacts are present and correct, and exits without modifying the issue. This behavior is by design -- the skill's idempotency guarantees ensure that re-running triage on an already-triaged issue is safe and produces no side effects.
