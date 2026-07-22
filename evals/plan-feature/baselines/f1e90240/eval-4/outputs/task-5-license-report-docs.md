# Task 5: Document license report endpoint and policy configuration

- **Jira parent**: TC-9004
- **Repository**: trustify-backend
- **Target Branch**: main
- **Priority**: Major
- **Fix Versions**: RHTPA 1.5.0

## Description

Document the new `GET /api/v2/sbom/{id}/license-report` endpoint and the license policy configuration. This covers endpoint usage, response schema, policy file format, and how organizations can customize their compliance rules.

The feature description specifies Doc Impact: New Content.

## Files to Modify/Create

| Action | Path |
|---|---|
| Create | `docs/api/license-report.md` |
| Create | `docs/configuration/license-policy.md` |
| Create | `license-policy.example.json` — example policy configuration file |

## Implementation Notes

- **`docs/api/license-report.md`**: Document the endpoint including:
  - HTTP method and path: `GET /api/v2/sbom/{id}/license-report`
  - Path parameters: `id` (SBOM UUID)
  - Response schema with field descriptions for `LicenseReport`, `LicenseGroup`
  - Example request/response
  - Error responses (404, 500)
  - Use case: compliance officer auditing open-source licenses; CI/CD pipeline gating builds on license compliance

- **`docs/configuration/license-policy.md`**: Document the license policy configuration:
  - File format and location
  - Allow-list and deny-list semantics
  - SPDX license identifier reference
  - How organizations customize their compliance rules
  - Example configurations for common policies (permissive-only, copyleft-allowed, etc.)

- **`license-policy.example.json`**: Provide a sample policy file with comments explaining each field. Example structure:
  ```json
  {
    "allowed": ["MIT", "Apache-2.0", "BSD-2-Clause", "BSD-3-Clause"],
    "denied": ["GPL-3.0-only", "AGPL-3.0-only"],
    "default_compliance": true
  }
  ```

## Acceptance Criteria

- Endpoint documentation covers all request/response fields.
- Policy configuration documentation explains allow/deny semantics.
- Example policy file is valid JSON and parseable by the `LicensePolicy` struct.
- Reference material includes link to SPDX license list.

## Test Requirements

- Validate that `license-policy.example.json` is valid JSON (can be checked in CI with a JSON linter).
