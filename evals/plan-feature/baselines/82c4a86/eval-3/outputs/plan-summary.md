# Plan Summary — TC-9003: SBOM Comparison View

## Overview

This plan decomposes TC-9003 into 5 implementation tasks across 2 repositories (trustify-backend, trustify-ui). Backend tasks are sequenced first, followed by frontend tasks that depend on the backend API contract.

## Tasks Created

| # | Title | Repository | Dependencies |
|---|---|---|---|
| 1 | Add SBOM comparison model and diff service | trustify-backend | None |
| 2 | Add SBOM comparison REST endpoint | trustify-backend | Task 1 |
| 3 | Add comparison API client and React Query hook | trustify-ui | Task 2 |
| 4 | Add SBOM comparison page with diff sections | trustify-ui | Task 3 |
| 5 | Add "Compare selected" action to SBOM list page | trustify-ui | Task 4 |

## Dependency Chain

```
Task 1 (backend model+service)
  └─► Task 2 (backend endpoint)
        └─► Task 3 (frontend API client + hook)
              └─► Task 4 (frontend comparison page)
                    └─► Task 5 (frontend list page integration)
```

## Repositories Affected

- **trustify-backend** (Tasks 1-2): New comparison model, service, and endpoint
- **trustify-ui** (Tasks 3-5): New API client, comparison page, and list page selection

## Architecture Summary

- **Backend**: A new `SbomService::compare` method computes diffs on-the-fly from existing SBOM, package, advisory, and license data. No new database tables. Exposed via `GET /api/v2/sbom/compare?left={id1}&right={id2}`.
- **Frontend**: TypeScript interfaces and React Query hook wrap the comparison endpoint. A new page at `/sbom/compare` renders the Figma-specified UI with PatternFly components (Select dropdowns, ExpandableSection, composable Table, Badge, EmptyState). The SBOM list page gains checkbox selection and a "Compare selected" action.

## Cross-Repo API Contract

The frontend (Tasks 3-4) depends on the backend endpoint (Task 2) returning this JSON shape:

```json
{
  "added_packages": [{ "name": "...", "version": "...", "license": "...", "advisory_count": 0 }],
  "removed_packages": [{ "name": "...", "version": "...", "license": "...", "advisory_count": 0 }],
  "version_changes": [{ "name": "...", "left_version": "...", "right_version": "...", "direction": "upgrade" }],
  "new_vulnerabilities": [{ "advisory_id": "...", "severity": "critical", "title": "...", "affected_package": "..." }],
  "resolved_vulnerabilities": [{ "advisory_id": "...", "severity": "...", "title": "...", "previously_affected_package": "..." }],
  "license_changes": [{ "name": "...", "left_license": "...", "right_license": "..." }]
}
```

## Non-MVP Items (Not Planned)

- Export diff as JSON or CSV — marked as non-MVP in the feature. The Export dropdown UI is included (per Figma) but the actual export logic is deferred.
