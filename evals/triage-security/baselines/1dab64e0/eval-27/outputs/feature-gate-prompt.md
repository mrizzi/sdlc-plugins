# Feature-Gated Dependency -- VEX Justification Prompt

## Context

The vulnerable dependency `rustls` (CVE-2026-99002) is gated behind the
`tls-rustls` feature, which is not enabled by default. The product ships
with the `tls-native` feature enabled by default, which uses `native-tls`
instead of `rustls`.

All 2.2.x versions (2.2.0 through 2.2.4) include rustls 0.23.4 in their
Cargo.lock, but the dependency is only compiled and linked when a consumer
explicitly enables the `tls-rustls` feature flag.

## VEX Justification Prompt

The vulnerable dependency `rustls` is gated behind the `tls-rustls`
feature, which is not enabled by default. Recommended VEX justification:
**Vulnerable Code not in Execute Path**.

Options:
1. Skip remediation -- apply VEX justification and close as not affected
2. Proceed with remediation -- create tasks despite the feature gate

Choose (1/2):

## Explanation of Options

### Option 1: Skip remediation (recommended)

If the user selects option 1:
- Apply VEX justification: **Vulnerable Code not in Execute Path**
- Set VEX Justification custom field (`customfield_12345`) to
  "Vulnerable Code not in Execute Path"
- Close the Vulnerability issue TC-8051 with resolution "Not a Bug"
- Post summary comment documenting:
  - The version impact table showing all 2.2.x versions ship rustls 0.23.4
  - The feature-gate evidence from Cargo.toml
  - The VEX justification rationale: rustls is an optional dependency behind
    a non-default feature flag; the default build does not include it
- Add the `ai-cve-triaged` label

### Option 2: Proceed with remediation

If the user selects option 2:
- Create standard remediation tasks (upstream backport + downstream
  propagation) for the 2.2.x stream without label or priority modifications
- The upstream task would bump rustls to >= 0.23.5 on branch `release/0.4.z`
  in the `backend` repository
- The downstream task would update the backend source reference in the
  Konflux release repo `rhtpa-release.0.4.z`
