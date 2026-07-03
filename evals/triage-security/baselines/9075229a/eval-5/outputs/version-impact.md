# Step 2 -- Version Impact Analysis: CVE-2026-40215

## 2.1 -- Supportability Matrix

Loaded from mock security-matrix.md. Last-Updated: 2026-06-28T10:00:00Z (5 days ago -- within the 14-day freshness threshold, no staleness warning).

Two streams loaded:
- **2.1.x** from rhtpa-release.0.3.z (versions 2.1.0, 2.1.1)
- **2.2.x** from rhtpa-release.0.4.z (versions 2.2.0, 2.2.1, 2.2.2, 2.2.3, 2.2.4)

## 2.3 -- Dependency Version Extraction (rpms.lock.yaml)

Ecosystem: RPM. Lock file: `rpms.lock.yaml`. Vulnerable library: openssl-libs.
Fix threshold: 3.0.7-28.el9_4 (from Jira description).

Version Impact for CVE-2026-40215 (openssl-libs, versions before 3.0.7-28.el9_4):

| Version | Stream | Tag | openssl-libs version | Affected? | Notes |
|---------|--------|-----|----------------------|-----------|-------|
| 2.1.0 | 2.1.x | `v0.3.8` | 3.0.7-24.el9 | YES | |
| 2.1.1 | 2.1.x | `v0.3.12` | 3.0.7-24.el9 | YES | |
| 2.2.0 | 2.2.x | `v0.4.5` | 3.0.7-25.el9_3 | YES | |
| 2.2.1 | 2.2.x | `v0.4.8` | 3.0.7-27.el9_4 | YES | |
| 2.2.2 | 2.2.x | `v0.4.9` | -- | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 2.2.x | `v0.4.11` | 3.0.7-28.el9_4 | NO | ships fixed version |
| 2.2.4 | 2.2.x | `v0.4.12` | 3.0.7-28.el9_4 | NO | ships fixed version |

## 2.3.5 -- Dependency Chain Context

Dependency chain for openssl-libs (RPM):

```
rpms.lock.yaml: PRESENT --> explicit install
SBOM verification: skipped -- cosign not available. Using rpms.lock.yaml classification only.
Origin: explicit install (openssl-libs specified in rpms.lock.yaml)

Remediation: update the package spec in rpms.in.yaml / rpms.lock.yaml
to >= 3.0.7-28.el9_4.
```

The package openssl-libs is present in rpms.lock.yaml at each pinned commit,
indicating it is an explicitly installed package (not inherited from the base
image). SBOM comparison via cosign was not performed because cosign is not
available in this environment. The rpms.lock.yaml classification alone is used.

## 2.4 -- Version Impact Summary

**Stream 2.2.x (issue scope):**
- Affected: 2.2.0, 2.2.1, 2.2.2 (retag)
- Not affected: 2.2.3, 2.2.4

**Stream 2.1.x (cross-stream):**
- Affected: 2.1.0, 2.1.1

## 2.5 -- Upstream Fix Check

RPM ecosystem has no Upstream Branch configured in the Ecosystem Mappings table.
Upstream fix check is not applicable for system packages -- the fix is applied
directly in the Konflux release repo by updating rpms.lock.yaml / rpms.in.yaml.
