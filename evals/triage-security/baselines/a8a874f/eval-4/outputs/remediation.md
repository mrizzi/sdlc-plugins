# Remediation

## Affected Stream: 2.1.x

The 2.2.x stream already ships h2 >= 0.4.8 (the fix) and requires no remediation.

Ecosystem: Cargo -- two tasks are required: upstream backport and downstream propagation.

---

### Task 1: Upstream Backport (2.1.x stream)

- **Repository**: backend
- **Target Branch**: release/0.3.z
- **Action**: Bump h2 to >= 0.4.8 in Cargo.lock / Cargo.toml
- **CVE**: CVE-2026-33501
- **Stream**: 2.1.x

Source: Ecosystem Mappings for the 2.1.x stream (rhtpa-release.0.3.z) specifies Cargo ecosystem maps to repository `backend` on upstream branch `release/0.3.z`.

### Task 2: Downstream Propagation (2.1.x stream)

- **Repository**: rhtpa-release.0.3.z
- **Target Branch**: main
- **Action**: Update artifacts.lock.yaml to pin a backend tag that includes the h2 >= 0.4.8 fix
- **CVE**: CVE-2026-33501
- **Stream**: 2.1.x

Source: Version Streams configuration specifies the Konflux release repo for 2.1.x is rhtpa-release.0.3.z.

---

## Streams Not Requiring Remediation

- **2.2.x**: All versions (2.2.0 through 2.2.4) ship h2 >= 0.4.8. No tasks needed.

## Note

No cross-stream impact notice is generated. The issue is unscoped (no stream suffix in the summary), meaning it covers all streams by definition. Cross-stream impact notices (Case B) only apply to scoped issues where a fix in one stream might affect another.
