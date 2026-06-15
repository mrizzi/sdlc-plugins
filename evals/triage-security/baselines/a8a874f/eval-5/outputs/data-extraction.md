# Data Extraction (Step 1)

Parsed CVE data from vulnerability issue TC-8005:

- **CVE ID**: CVE-2026-40215
- **Package**: openssl-libs -- this is a system-level RPM package, NOT a source dependency
- **Affected range**: versions before 3.0.7-28.el9_4
- **Fixed version**: 3.0.7-28.el9_4
- **CVSS**: 7.1 (High)
- **Ecosystem**: **RPM** (NOT Cargo) -- detected from the library name openssl-libs being a system RPM package. The Ecosystem Mappings in security-matrix.md shows RPM ecosystem with rpms.lock.yaml as the lock file.
- **Lock file**: rpms.lock.yaml
- **Stream scope**: [rhtpa-2.2] -> 2.2.x stream
- **PSIRT Affects Versions**: RHTPA 2.0.0
