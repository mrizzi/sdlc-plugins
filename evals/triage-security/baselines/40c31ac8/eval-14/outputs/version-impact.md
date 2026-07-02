# Step 2 -- Version Impact Analysis: CVE-2026-40215

## Stream Scope

This issue is scoped to **stream 2.2.x** per the `[rhtpa-2.2]` suffix.
Version impact is analyzed for all versions in the 2.2.x stream.

## Version Impact Table

Version Impact for CVE-2026-40215 (openssl-libs < 3.0.7-28.el9_4):

| Version | Tag | openssl-libs version | Affected? | Notes |
|---------|-----|----------------------|-----------|-------|
| 2.2.0 | v0.4.5 | 3.0.7-25.el9_3 | **YES** | < 3.0.7-28.el9_4 |
| 2.2.1 | v0.4.8 | 3.0.7-27.el9_4 | **YES** | < 3.0.7-28.el9_4 |
| 2.2.2 | v0.4.9 | 3.0.7-27.el9_4 | **YES** | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | v0.4.11 | 3.0.7-28.el9_4 | NO | = fix version |
| 2.2.4 | v0.4.12 | 3.0.7-28.el9_4 | NO | = fix version |

**Summary**: Versions 2.2.0, 2.2.1, and 2.2.2 are affected. Versions 2.2.3 and 2.2.4 already ship the fixed openssl-libs.

## Dependency Chain Context (Step 2.3.5)

Dependency chain for openssl-libs (RPM):
- rpms.lock.yaml: present (explicit install)
- SBOM verification: present in BOTH final image SBOM and base image SBOM (base image origin)
- **Disagreement detected** -- see outputs/sbom-verification.md for details
- Origin: **disputed** -- rpms.lock.yaml classifies as explicit install, SBOM classifies as base image

## Cross-Stream Impact

Although this issue is scoped to 2.2.x, the 2.1.x stream is also affected:

| Version | Tag | openssl-libs version | Affected? | Notes |
|---------|-----|----------------------|-----------|-------|
| 2.1.0 | v0.3.8 | 3.0.7-24.el9 | **YES** | < 3.0.7-28.el9_4 |
| 2.1.1 | v0.3.12 | 3.0.7-24.el9 | **YES** | < 3.0.7-28.el9_4 |

Cross-stream impact: openssl-libs (< 3.0.7-28.el9_4) also affects stream 2.1.x.
These versions are tracked by companion issues (see Related links) or may require separate PSIRT triage.

## Proposed Affects Versions Correction (Step 3)

The PSIRT-assigned Affects Version **RHTPA 2.0.0** is incorrect -- there is no 2.0.x stream configured.

Scoped to stream 2.2.x, the correct Affects Versions are:

```
Current:  [RHTPA 2.0.0]
Proposed: [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]
```

This correction requires engineer confirmation before execution.
Versions 2.2.3 and 2.2.4 are excluded because they already ship the fixed openssl-libs 3.0.7-28.el9_4.

## Upstream Fix Status

RPM ecosystem has no upstream branch configured (Upstream Branch column is empty for RPM in Ecosystem Mappings).
The fix is available via the Red Hat errata: RHSA-2026:4021.

## Remediation Recommendation (Step 8)

Since versions 2.2.0 through 2.2.2 are affected and 2.2.3+ already ships the fix, the vulnerability was already remediated in the 2.2.x stream starting with version 2.2.3. The affected versions (2.2.0, 2.2.1, 2.2.2) are older releases.

**Proposed actions** (not executed -- require engineer confirmation):

1. **Correct Affects Versions**: RHTPA 2.0.0 -> [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]
2. **Post Affects Versions correction comment** to TC-8005 documenting the lock file evidence
3. **Note cross-stream impact**: 2.1.x stream (versions 2.1.0, 2.1.1) also ships vulnerable openssl-libs
4. **Add label**: `ai-cve-triaged` to TC-8005
5. **Post summary comment** to TC-8005 with version impact table and triage outcome
