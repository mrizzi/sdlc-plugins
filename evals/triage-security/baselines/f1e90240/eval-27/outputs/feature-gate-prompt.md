# Feature-Gated Dependency -- VEX Justification Prompt

## Context

The vulnerable dependency `rustls` (CVE-2026-99002, CVSS 8.1 High) is gated behind the `tls-rustls` feature flag, which is **not** enabled by default. The product ships with the `tls-native` feature enabled by default. All 2.2.x versions (2.2.0 through 2.2.4) include rustls 0.23.4 in Cargo.lock as an optional dependency, but default builds do not compile or link it.

## VEX Justification Prompt

The vulnerable dependency `rustls` is gated behind the `tls-rustls` feature, which is not enabled by default. Recommended VEX justification: **Vulnerable Code not in Execute Path**.

Options:
1. **Skip remediation** -- apply VEX justification and close as not affected
2. **Proceed with remediation** -- create tasks despite the feature gate

Choose (1/2):

## Outcome Details

### If option 1 (Skip remediation):

- **VEX justification**: Vulnerable Code not in Execute Path
- **VEX custom field**: `customfield_12345` set to "Vulnerable Code not in Execute Path"
- **Resolution**: Close TC-8051 as "Not a Bug" with VEX justification
- **Rationale**: The vulnerable dependency `rustls` 0.23.4 is an optional dependency gated behind the non-default `tls-rustls` feature flag. The product ships with `tls-native` (default feature), so the vulnerable code is never compiled into or executed by the default product binary. The `tls-rustls` feature must be explicitly enabled at build time to include rustls.
- **Close comment**: "No supported versions ship rustls in the default configuration. Version impact analysis shows rustls 0.23.4 is present in Cargo.lock for all 2.2.x versions, but it is an optional dependency gated behind the non-default `tls-rustls` feature flag. The default feature set is `[\"tls-native\"]`. VEX justification: Vulnerable Code not in Execute Path."

### If option 2 (Proceed with remediation):

- Create standard remediation tasks (upstream backport + downstream propagation) for the 2.2.x stream without label or priority modifications
- Upstream task: bump rustls to >= 0.23.5 on `release/0.4.z` branch
- Downstream task: update backend reference in rhtpa-release.0.4.z to pick up the fix
