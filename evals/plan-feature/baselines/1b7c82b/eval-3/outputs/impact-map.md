# Impact Map: TC-9003 SBOM Comparison View

## Feature Summary

Add a side-by-side SBOM comparison view with a backend diffing endpoint (`GET /api/v2/sbom/compare`) and a frontend comparison UI. Users select two SBOM versions and see structured diffs: added/removed packages, version changes, new/resolved vulnerabilities, and license changes.

## Impacted Repositories

### trustify-backend

| Area | Files / Paths | Nature of Change |
|---|---|---|
| Comparison model | `modules/fundamental/src/sbom/model/` | New structs: `SbomComparison`, `PackageDiff`, `VersionChange`, `VulnerabilityDiff`, `LicenseChange` |
| Comparison service | `modules/fundamental/src/sbom/service/` | New `compare` method on `SbomService` that loads two SBOMs, computes package/advisory/license diffs |
| Comparison endpoint | `modules/fundamental/src/sbom/endpoints/` | New `compare.rs` handler for `GET /api/v2/sbom/compare?left={id1}&right={id2}` |
| Endpoint registration | `modules/fundamental/src/sbom/endpoints/mod.rs` | Register the new compare route |
| Integration tests | `tests/api/` | New `sbom_compare.rs` test file covering comparison scenarios |

### trustify-ui

| Area | Files / Paths | Nature of Change |
|---|---|---|
| API types | `src/api/models.ts` | New TypeScript interfaces for comparison response |
| API client | `src/api/rest.ts` | New `fetchSbomComparison()` function |
| React Query hook | `src/hooks/` | New `useSbomComparison.ts` hook |
| Comparison page | `src/pages/SbomComparisonPage/` | New page with SBOM selectors, diff sections, empty/loading states |
| Route registration | `src/routes.tsx` | Add `/sbom/compare` route |
| MSW mocks | `tests/mocks/` | New comparison handler and fixture data |

## Task Dependency Graph

```
Task 1: Backend comparison model & service
  |
  v
Task 2: Backend comparison endpoint & tests
  |
  v
Task 3: Frontend API layer & hook  -->  Task 4: Frontend comparison page UI
```

## Out of Scope (Non-MVP)

- Export diff as JSON or CSV (deferred to follow-up)
