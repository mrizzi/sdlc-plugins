# Security Matrix — {stream} Stream

<!-- Canonical template for security matrix files. Copy this file to the path
     specified in your Security Configuration's Version Streams table
     (e.g., docs/security-matrix-2.2.x.md) and replace placeholders with
     concrete values. The triage-security skill validates existing matrices
     against this structure. -->

## Version Stream

<!-- Identifies which product version stream this matrix covers. -->

This Konflux release repo covers the **{stream}** product version stream.

## Supportability Matrix

<!-- One row per product version built from this release stream.
     trustify and trustify-ui columns contain the tag or commit hash
     pinned in the Konflux build. -->

| RHTPA Version | Build | Build Date | trustify | trustify-ui | Notes |
|---|---|---|---|---|---|
| {version} | {build} | {build-date} | `{trustify-ref}` | `{trustify-ui-ref}` | |

### Source Pinning Method

<!-- How each source repository's commit or tag is pinned in the Konflux
     release repo. Common methods: git submodule, artifacts.lock.yaml,
     or tag reference in a build config file. -->

- **trustify**: {trustify-pinning-method}
- **trustify-ui**: {trustify-ui-pinning-method}

## Ecosystem Mappings

<!-- Maps each dependency ecosystem to its lock file and inspection command.
     Used by triage-security to check whether a specific package version
     is present in a given product build. -->

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|---|---|---|---|---|
| {ecosystem} | {repository} | `{lock-file}` | `{check-command}` | `{upstream-branch}` |

## Forward Pointer

<!-- Points to the next version stream's matrix, or "None" for the latest
     development stream. Helps navigation across streams. -->

{forward-pointer}
