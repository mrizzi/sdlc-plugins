# Version Impact Analysis — CVE-2026-28940 (serde_json)

## Step 2.3 — Dependency Version Extraction

Fix threshold: **1.0.135** (from Jira description; would be cross-validated with MITRE CVE API and OSV.dev in live triage).

Ecosystem: Cargo. Lock file: `Cargo.lock`. Check command: `git show <tag>:Cargo.lock | grep -A2 'name = "serde_json"'`

### Stream 2.1.x (rhtpa-release.0.3.z)

| Version | Tag | serde_json version | Affected? | Notes |
|---------|-----|--------------------|-----------|-------|
| 2.1.0 | v0.3.8 | 1.0.137 | NO | >= 1.0.135 |
| 2.1.1 | v0.3.12 | 1.0.137 | NO | >= 1.0.135 |

### Stream 2.2.x (rhtpa-release.0.4.z) — issue-scoped stream

| Version | Tag | serde_json version | Affected? | Notes |
|---------|-----|--------------------|-----------|-------|
| 2.2.0 | v0.4.5 | 1.0.138 | NO | >= 1.0.135 |
| 2.2.1 | v0.4.8 | 1.0.138 | NO | >= 1.0.135 |
| 2.2.2 | v0.4.9 | -- | NO | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | v0.4.11 | 1.0.139 | NO | >= 1.0.135 |
| 2.2.4 | v0.4.12 | 1.0.139 | NO | >= 1.0.135 |

## Step 2.4 — Version Impact Table (Aggregated)

Version Impact for CVE-2026-28940 (serde_json < 1.0.135):

| Version | Stream | serde_json | Affected? | Notes |
|---------|--------|------------|-----------|-------|
| 2.1.0 | 2.1.x | 1.0.137 | NO | |
| 2.1.1 | 2.1.x | 1.0.137 | NO | |
| 2.2.0 | 2.2.x | 1.0.138 | NO | |
| 2.2.1 | 2.2.x | 1.0.138 | NO | |
| 2.2.2 | 2.2.x | -- | NO | retag of 2.2.1 |
| 2.2.3 | 2.2.x | 1.0.139 | NO | |
| 2.2.4 | 2.2.x | 1.0.139 | NO | |

**Result: NO supported versions ship a vulnerable version of serde_json.** All versions ship serde_json >= 1.0.137, which is above the fix threshold of 1.0.135.

## Step 2.5 — Upstream Fix Check

Not applicable. No versions are affected, so upstream fix status is moot. For completeness, since all shipped versions already include a version above the fix threshold, no upstream backport or downstream propagation is required.
