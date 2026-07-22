# Field Propagation Summary: TC-9003

## Inherited Fields

The following fields from feature TC-9003 have been propagated to all child tasks:

| Field | Value | Scope | Tasks Applied |
|---|---|---|---|
| Priority | Critical | All tasks | Tasks 1-9 |
| Fix Versions | RHTPA 1.5.0 | Both repositories (default scope) | Tasks 1-9 |

## Propagation Details

- **Priority: Critical** -- Propagated to all 9 child tasks. Every task header includes `Priority: Critical`.
- **Fix Versions: RHTPA 1.5.0** -- Propagated to all 9 child tasks with default scope "both", meaning it applies to tasks targeting both `trustify-backend` (Tasks 2-4) and `trustify-ui` (Tasks 5-8), as well as cross-repo bookend tasks (Tasks 1, 9).

## Task Summary

| Task | Slug | Repository | Target Branch |
|---|---|---|---|
| 1 | create-feature-branch | trustify-backend, trustify-ui | main |
| 2 | comparison-model | trustify-backend | TC-9003 |
| 3 | comparison-service | trustify-backend | TC-9003 |
| 4 | comparison-endpoint | trustify-backend | TC-9003 |
| 5 | comparison-api-client | trustify-ui | TC-9003 |
| 6 | comparison-hook | trustify-ui | TC-9003 |
| 7 | comparison-page | trustify-ui | TC-9003 |
| 8 | comparison-route-tests | trustify-ui | TC-9003 |
| 9 | merge-feature-branch | trustify-backend, trustify-ui | main |

## Workflow Mode

Feature-branch mode selected. The SBOM comparison feature requires tightly coupled backend and frontend changes -- the new `/sbom/compare` UI page cannot function without the new `GET /api/v2/sbom/compare` backend endpoint. A feature branch (`TC-9003`) isolates all intermediate work. Bookend tasks (1 and 9) target `main`; intermediate tasks (2-8) target `TC-9003`.

## Cross-Repository Dependency

Task 5 (trustify-ui) explicitly depends on Task 4 (trustify-backend), establishing the cross-repo dependency chain. Backend tasks (2-4) have lower task numbers than frontend tasks (5-8) to enforce build order.
