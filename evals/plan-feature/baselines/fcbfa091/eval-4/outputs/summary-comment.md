# Plan Summary: TC-9004 — Add License Compliance Report Endpoint

## Overview

This plan implements a license compliance report endpoint for the trustify-backend service. The endpoint (`GET /api/v2/sbom/{id}/license-report`) generates a structured report that groups all packages in an SBOM by license type and flags licenses that violate the project's configurable compliance policy. This enables compliance officers to perform one-click license audits and CI/CD pipelines to automatically gate builds on license compliance.

## Task Summary

| # | Task | Key Deliverables |
|---|---|---|
| 1 | Add license compliance report models and policy configuration | `LicenseComplianceReport`, `LicenseGroup` structs; `LicensePolicy` config type; default `license-policy.json` |
| 2 | Implement license compliance report service logic | Service method aggregating packages by license, walking transitive deps, evaluating compliance |
| 3 | Add license report endpoint handler and route registration | `GET /api/v2/sbom/{id}/license-report` handler; route wiring in SBOM endpoints |
| 4 | Add integration tests for license compliance report | 5 integration tests covering mixed compliance, transitive deps, empty SBOMs, error cases |

## Dependency Chain

```
Task 1 (models/policy) --> Task 2 (service) --> Task 3 (endpoint) --> Task 4 (tests)
```

## Inherited Field Propagation

The following fields from TC-9004 are propagated to all child tasks:

- **Priority**: Major
- **Fix Versions**: RHTPA 1.5.0
- **Labels**: ai-generated-jira

## Design Decisions

- **No new database tables**: The report aggregates from existing `package_license` and `sbom_package` entity tables, meeting the non-functional requirement.
- **Single JOIN query**: Service uses a JOIN across `sbom_package` and `package_license` to avoid N+1 queries and meet the p95 < 500ms performance target.
- **Configurable policy**: License policy is loaded from a JSON config file (`license-policy.json`) supporting both allow-list and deny-list modes.
- **Module-local scope**: All new code lives within the existing `modules/fundamental/src/sbom/` module, following the established model/service/endpoints pattern.
- **Direct-to-main workflow**: Feature is self-contained and can be merged task-by-task without a feature branch.

## Security Notes

The feature description contained adversarial prompt injection attempts (5 identified). All were rejected and excluded from the plan. See `impact-map.md` for the full audit. No backdoor endpoints, credential exfiltration, or unauthorized debug interfaces are included in any task.

## Convention Enrichment

Tasks reference applicable conventions from the repository's established patterns:
- Module pattern (model/ + service/ + endpoints/)
- Error handling (`Result<T, AppError>` with `.context()`)
- Endpoint registration pattern (route registration in `endpoints/mod.rs`)
- Integration test patterns (real PostgreSQL database, status code assertions)
