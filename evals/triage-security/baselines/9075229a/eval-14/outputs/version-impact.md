# Step 2 -- Version Impact Analysis

## Stream Scope

Issue TC-8005 is scoped to stream **2.2.x** (suffix `[rhtpa-2.2]`).
Only versions in the 2.2.x stream are analyzed.

## Supportability Matrix Source

Matrix loaded from stream 2.2.x: `rhtpa-release.0.4.z`
Last-Updated: 2026-06-28T10:00:00Z (5 days ago -- within 14-day freshness threshold)

## Version Impact Table

Version Impact for CVE-2026-40215 (openssl-libs versions before 3.0.7-28.el9_4):

| Version | openssl-libs | Affected? | Notes |
|---------|-------------|-----------|-------|
| 2.2.0 | 3.0.7-25.el9_3 | YES | |
| 2.2.1 | 3.0.7-27.el9_4 | YES | |
| 2.2.2 | 3.0.7-27.el9_4 | YES | retag of 2.2.1 (backend same as v0.4.8) |
| 2.2.3 | 3.0.7-28.el9_4 | NO | at fixed version |
| 2.2.4 | 3.0.7-28.el9_4 | NO | at fixed version |

## Cross-Stream Observation

The 2.1.x stream (outside the scope of this issue) also ships vulnerable versions of
openssl-libs:

| Version | openssl-libs | Affected? | Notes |
|---------|-------------|-----------|-------|
| 2.1.0 | 3.0.7-24.el9 | YES | (out of scope -- different stream) |
| 2.1.1 | 3.0.7-24.el9 | YES | (out of scope -- different stream) |

This cross-stream impact would be reported in Step 8 (Case B) if applicable.

## Dependency Chain Context (Step 2.3.5)

Dependency chain for openssl-libs (RPM):
  rpms.lock.yaml: present -- explicit install
  SBOM verification: present in both final and base image SBOMs -- base image
    (DISAGREES with lock file classification -- see sbom-verification.md)
  Origin: DISPUTED -- rpms.lock.yaml says explicit install, SBOM says base image
  Remediation path depends on resolution of classification disagreement.

## Upstream Fix Status

RPM ecosystem has no Upstream Branch configured in the Ecosystem Mappings table
(Upstream Branch column is empty: `--`). Upstream fix check is not applicable for
system packages -- the fix comes from the RPM vendor (Red Hat errata).

Advisory with fix: https://access.redhat.com/errata/RHSA-2026:4021
