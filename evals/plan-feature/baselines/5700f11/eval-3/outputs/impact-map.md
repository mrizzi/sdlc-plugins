# Repository Impact Map — TC-9003: SBOM Comparison View

## Overview

This feature adds a side-by-side SBOM comparison view, requiring a new backend diffing endpoint and a frontend comparison UI. Two repositories are impacted: `trustify-backend` (new comparison service and endpoint) and `trustify-ui` (new comparison page, API client, hook, and route).

---

## trustify-backend

### New Files

- `modules/fundamental/src/sbom/model/comparison.rs` — Structs for the SBOM comparison response: `SbomComparison`, `AddedPackage`, `RemovedPackage`, `VersionChange`, `NewVulnerability`, `ResolvedVulnerability`, `LicenseChange`
- `modules/fundamental/src/sbom/service/compare.rs` — `SbomService::compare()` method that computes the structured diff between two SBOMs by querying package, advisory, and license data
- `modules/fundamental/src/sbom/endpoints/compare.rs` — `GET /api/v2/sbom/compare?left={id}&right={id}` endpoint handler
- `tests/api/sbom_compare.rs` — Integration tests for the comparison endpoint

### Modified Files

- `modules/fundamental/src/sbom/model/mod.rs` — Add `pub mod comparison;` to expose the new comparison model
- `modules/fundamental/src/sbom/service/mod.rs` — Add `pub mod compare;` to expose the comparison service
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Register the `/compare` route alongside existing SBOM routes
- `server/src/main.rs` — No changes expected (routes are registered via module endpoint registration)

### Rationale

The comparison endpoint computes an on-the-fly diff using existing SBOM, package, advisory, and license entity data. No new database tables or migrations are needed. The diff logic lives in the service layer following the existing `model/ + service/ + endpoints/` module pattern.

---

## trustify-ui

### New Files

- `src/api/comparisons.ts` — TypeScript interfaces for the comparison API response (`SbomComparison`, section item types)
- `src/hooks/useSbomComparison.ts` — React Query hook that calls `GET /api/v2/sbom/compare?left={id}&right={id}`
- `src/pages/SbomComparePage/SbomComparePage.tsx` — Main comparison page component with SBOM selectors, compare button, and diff sections
- `src/pages/SbomComparePage/SbomComparePage.test.tsx` — Unit tests for the comparison page
- `src/pages/SbomComparePage/components/DiffSection.tsx` — Reusable collapsible diff section using PatternFly `ExpandableSection` with count `Badge`
- `src/pages/SbomComparePage/components/AddedPackagesTable.tsx` — Table for added packages
- `src/pages/SbomComparePage/components/RemovedPackagesTable.tsx` — Table for removed packages
- `src/pages/SbomComparePage/components/VersionChangesTable.tsx` — Table for version changes
- `src/pages/SbomComparePage/components/NewVulnerabilitiesTable.tsx` — Table for new vulnerabilities (with critical row highlighting)
- `src/pages/SbomComparePage/components/ResolvedVulnerabilitiesTable.tsx` — Table for resolved vulnerabilities
- `src/pages/SbomComparePage/components/LicenseChangesTable.tsx` — Table for license changes
- `tests/mocks/fixtures/sbom-comparison.json` — Mock comparison response fixture
- `tests/e2e/sbom-compare.spec.ts` — Playwright E2E test for the comparison flow

### Modified Files

- `src/api/rest.ts` — Add `fetchSbomComparison(leftId, rightId)` API client function
- `src/routes.tsx` — Add route `/sbom/compare` pointing to `SbomComparePage`
- `tests/mocks/handlers.ts` — Add MSW handler for `GET /api/v2/sbom/compare`

### Rationale

The comparison page follows the existing page structure pattern (`src/pages/<PageName>/` with sub-components). It reuses the existing `useSboms` hook for SBOM selectors, the `SeverityBadge` shared component for vulnerability severity display, and the `EmptyStateCard` component for the initial empty state. PatternFly `ExpandableSection`, `Table`, `Select`, `Badge`, and `Dropdown` components are used per the Figma design specifications.
