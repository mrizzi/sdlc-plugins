# Step 1 — Data Extraction: TC-8040

## Extracted CVE Data

| Field | Value |
|-------|-------|
| **CVE ID** | CVE-2026-31812 |
| **Affected component** | `pscomponent:org/rhtpa-server` |
| **Product version (PSIRT-claimed)** | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| **Affects Versions (Jira field)** | RHTPA 2.0.0 |
| **Vulnerable library** | quinn-proto |
| **Affected version range** | versions before 0.11.14 (< 0.11.14) |
| **Fixed version** | 0.11.14 |
| **CVSS** | 7.5 (High) |
| **Due date** | 2026-07-15 |
| **Upstream fix PR** | [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) |
| **Advisory URL** | [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) |
| **CVE record URL** | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) |
| **Existing comments** | None |

## Stream Scope Resolution

The issue summary contains the suffix `[rhtpa-2.2]`, which maps to the **2.2.x** version stream (Konflux release repo `rhtpa-release.0.4.z`). This issue is **stream-scoped** to the 2.2.x stream.

## Ecosystem Detection

The vulnerable library is **quinn-proto**. Based on the eval instruction, ecosystem detection resolves to **Go modules**.

### Ecosystem Mappings available in security-matrix.md

The Ecosystem Mappings tables in the configured `security-matrix.md` files list the following ecosystems:

**Stream 2.2.x (rhtpa-release.0.4.z):**

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|-----------|------------|-----------|---------------|-----------------|
| Cargo | backend | `Cargo.lock` | `git show <tag>:Cargo.lock` | `release/0.4.z` |
| RPM | -- | `rpms.lock.yaml` | `git show <tag>:rpms.lock.yaml` | -- |

**Stream 2.1.x (rhtpa-release.0.3.z):**

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|-----------|------------|-----------|---------------|-----------------|
| Cargo | backend | `Cargo.lock` | `git show <tag>:Cargo.lock` | `release/0.3.z` |
| RPM | -- | `rpms.lock.yaml` | `git show <tag>:rpms.lock.yaml` | -- |

### Result

The detected ecosystem **Go modules** is **not listed** in either stream's Ecosystem Mappings table. The supported ecosystems are Cargo and RPM only.

**Automated triage cannot proceed for this ecosystem.**

## Deployment Context Lookup

The affected repository identified from the component label `pscomponent:org/rhtpa-server` was looked up in the Source Repositories table. The repository `rhtpa-backend` is the configured source repository. Deployment context defaults to `upstream` (no Deployment Context column present in the Source Repositories table).

## Step 0 Configuration Summary

| Config Field | Value |
|---|---|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Component label pattern | `pscomponent:` |
| VEX Justification custom field | customfield_12345 |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| Version Streams | 2.1.x (rhtpa-release.0.3.z), 2.2.x (rhtpa-release.0.4.z) |
| Source Repositories | rhtpa-backend (https://github.com/rhtpa/rhtpa-backend) |
