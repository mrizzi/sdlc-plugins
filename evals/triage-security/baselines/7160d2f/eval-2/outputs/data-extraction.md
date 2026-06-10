# Data Extraction: TC-8002

## CVE Identity

- **CVE ID:** CVE-2026-28940
- **Advisory:** GHSA-2026-j9r2-m5vk
- **Jira Key:** TC-8002
- **Status:** New
- **Assignee:** Unassigned

## Vulnerability Details

- **Affected Package:** serde_json
- **Vulnerable Versions:** < 1.0.135
- **Fixed Version:** 1.0.135
- **CVSS Score:** 5.3 (Medium)
- **Due Date:** 2026-07-30

## Vulnerability Description

Versions of serde_json before 1.0.135 are vulnerable to a stack overflow when deserializing deeply nested JSON input. An attacker can craft a JSON payload with thousands of nested arrays or objects that causes unbounded recursion during deserialization, leading to a stack overflow and process crash.

## Attack Vector Summary

- **Type:** Denial of Service (DoS) via stack overflow
- **Trigger:** Crafted deeply nested JSON payload
- **Impact:** Process crash (availability impact)
- **Exploitability:** Remote, requires ability to send JSON input to a deserializing endpoint

## Affected Product Scope

- **Jira Affects Version:** RHTPA 2.2.0
- **Stream Suffix:** [rhtpa-2.2] (scoped to 2.2.x stream)
- **Streams to Evaluate:** All supported streams (2.1.x and 2.2.x)

## Lock File Data (serde_json versions shipped)

| Build Tag | serde_json Version | Vulnerable (< 1.0.135)? |
|-----------|-------------------|--------------------------|
| v0.3.8    | 1.0.137           | No                       |
| v0.3.12   | 1.0.137           | No                       |
| v0.4.5    | 1.0.138           | No                       |
| v0.4.8    | 1.0.138           | No                       |
| v0.4.9    | (retag of v0.4.8) | No (1.0.138)             |
| v0.4.11   | 1.0.139           | No                       |
| v0.4.12   | 1.0.139           | No                       |
