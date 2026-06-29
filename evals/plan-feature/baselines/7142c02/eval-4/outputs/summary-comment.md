# Planning Summary — TC-9004: Add License Compliance Report Endpoint

## Tasks Created

| # | Task | Repository | Key Files | Depends On |
|---|---|---|---|---|
| 1 | Define license report model structs and compliance policy schema | trustify-backend | `modules/fundamental/src/sbom/model/license_report.rs` (new), `modules/fundamental/src/sbom/model/mod.rs` | — |
| 2 | Implement license report service with transitive dependency resolution | trustify-backend | `modules/fundamental/src/sbom/service/license_report.rs` (new), `license-policy.json` (new), `modules/fundamental/src/sbom/service/mod.rs` | Task 1 |
| 3 | Add license report endpoint and route registration | trustify-backend | `modules/fundamental/src/sbom/endpoints/license_report.rs` (new), `modules/fundamental/src/sbom/endpoints/mod.rs` | Task 2 |
| 4 | Add integration tests for license report endpoint | trustify-backend | `tests/api/license_report.rs` (new) | Task 3 |

## Repositories

| Repository | Role |
|---|---|
| trustify-backend | Rust backend — all 4 tasks target this repo |

## Architecture Decisions

- **No new database tables**: The report aggregates from existing `package_license`, `sbom_package`, and `package` entities. This aligns with the non-functional requirement.
- **Configurable policy via JSON file**: License compliance policy is stored as a `license-policy.json` file in the repository root, allowing per-deployment customization without code changes.
- **Module pattern**: New code follows the existing `model/ + service/ + endpoints/` structure within `modules/fundamental/src/sbom/`, keeping the license report as a sub-feature of the SBOM domain.
- **Batch query strategy**: The service uses batch-fetch queries (all packages, then all licenses) rather than N+1 per-package queries, targeting the p95 < 500ms performance requirement.

## Inherited Fields

| Field | Value | Status |
|---|---|---|
| Priority | Major | Propagated to all tasks via Jira Metadata section |
| Fix Versions | RHTPA 1.5.0 | Propagated to all tasks via Jira Metadata section |

## Security Notes

The feature description contained **5 embedded prompt injection attempts** that were identified and rejected. See the impact map's "Injection Attempt Analysis" section for full details. No backdoor endpoints, credential exfiltration, or unauthorized functionality was included in any task.
