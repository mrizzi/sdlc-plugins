# Feature-Gate VEX Justification Prompt

## Context

The vulnerable dependency `rustls` (CVE-2026-99002, CVSS 8.1 High) is present in the Cargo.lock at version 0.23.4 (below fix threshold 0.23.5) for all 2.2.x versions. However, it is an optional dependency gated behind a non-default feature flag.

- **Library**: rustls
- **Declared as**: `optional = true` in `[dependencies]`
- **Feature flag**: `tls-rustls`
- **Default features**: `["tls-native"]` (does NOT include `tls-rustls`)
- **Product ships with**: `tls-native` (native-tls) enabled by default

## Prompt Presented to User

The vulnerable dependency `rustls` is gated behind the `tls-rustls` feature, which is not enabled by default. Recommended VEX justification: **Vulnerable Code not in Execute Path**.

Options:
1. Skip remediation -- apply VEX justification and close as not affected
2. Proceed with remediation -- create tasks despite the feature gate

Choose (1/2):

## Outcome Paths

### Option 1: Skip remediation (VEX justification)

- VEX Justification: **Vulnerable Code not in Execute Path**
- Rationale: The rustls crate is declared as an optional dependency (`optional = true`) and is only compiled when the `tls-rustls` feature is explicitly enabled. The default feature set (`["tls-native"]`) does not include `tls-rustls`. The product as shipped uses native-tls as its TLS backend, so the vulnerable rustls code is not compiled into the binary and is not in the execute path.
- Action: Close as Not a Bug with VEX justification field (`customfield_12345`) set to "Vulnerable Code not in Execute Path".

### Option 2: Proceed with remediation

- Create standard remediation tasks for all affected 2.2.x versions without label or priority modifications.
- Two tasks per stream (source dependency ecosystem -- Cargo):
  - Upstream backport task: bump rustls to >= 0.23.5 in backend Cargo.toml on release/0.4.z
  - Downstream propagation subtask: update backend source reference in rhtpa-release.0.4.z
