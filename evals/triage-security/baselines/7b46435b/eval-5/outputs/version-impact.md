# Step 2 -- Version Impact Analysis

## Version Impact for CVE-2026-40215 (openssl-libs < 3.0.7-28.el9_4)

### Scoped stream: 2.2.x (rhtpa-release.0.4.z)

| Version | Tag | openssl-libs | Affected? | Notes |
|---------|-----|-------------|-----------|-------|
| 2.2.0 | v0.4.5 | 3.0.7-25.el9_3 | YES | |
| 2.2.1 | v0.4.8 | 3.0.7-27.el9_4 | YES | |
| 2.2.2 | v0.4.9 | -- | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | v0.4.11 | 3.0.7-28.el9_4 | NO | ships fixed version |
| 2.2.4 | v0.4.12 | 3.0.7-28.el9_4 | NO | ships fixed version |

### Cross-stream reference: 2.1.x (rhtpa-release.0.3.z)

| Version | Tag | openssl-libs | Affected? | Notes |
|---------|-----|-------------|-----------|-------|
| 2.1.0 | v0.3.8 | 3.0.7-24.el9 | YES | |
| 2.1.1 | v0.3.12 | 3.0.7-24.el9 | YES | |

All 2.1.x versions are affected. This is cross-stream impact (Case B) and
will be noted in remediation for companion issue coordination.

## Dependency Chain (Step 2.3.5)

```
Dependency chain for openssl-libs (RPM):
  rpms.lock.yaml: present --> explicit install
  SBOM verification: skipped -- cosign not available in this environment.
    Using rpms.lock.yaml classification only.
  Origin: explicit install (openssl-libs specified in rpms.lock.yaml)

Remediation: update the package version in rpms.lock.yaml (and rpms.in.yaml
if present) to >= 3.0.7-28.el9_4.
```

Since openssl-libs is found in `rpms.lock.yaml` at each inspected tag, it is
classified as an **explicit install** -- not inherited from a base image.
The remediation path is to update the package spec directly in the Konflux
release repo's RPM lock file.

SBOM verification via cosign was not performed because cosign is not available
in this environment. The rpms.lock.yaml classification stands as the sole
source of origin determination.

## Upstream Fix Status

The RPM ecosystem mapping for the 2.2.x stream has no Upstream Branch configured
(column value is `--`). Upstream fix status check is not applicable for RPM
system packages -- the fix comes from the RPM repository (Red Hat errata), not
from a source code branch.

The advisory RHSA-2026:4021 confirms the fix is available as openssl-libs-3.0.7-28.el9_4.
