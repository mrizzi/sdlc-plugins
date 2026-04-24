# Repository Impact Map — TC-9003: SBOM Comparison View

## Overview

This feature adds a side-by-side SBOM comparison view that lets users select two SBOM versions and see a structured diff: added/removed packages, version changes, new/resolved vulnerabilities, and license changes. It requires a new backend diffing endpoint and a frontend comparison UI built from Figma mockups. Two repositories are impacted.

---

## trustify-backend

### Changes

- Add comparison model structs (`SbomComparison`, `AddedPackage`, `RemovedPackage`, `VersionChange`, `NewVulnerability`, `ResolvedVulnerability`, `LicenseChange`) in `modules/fundamental/src/sbom/model/`
- Add comparison diff computation service (`SbomService::compare`) in `modules/fundamental/src/sbom/service/` that computes on-the-fly diffs from existing package, advisory, and license entity data
- Add `GET /api/v2/sbom/compare?left={id}&right={id}` endpoint handler in `modules/fundamental/src/sbom/endpoints/`
- Register the comparison route in the SBOM endpoint module
- Add integration tests for the comparison endpoint in `tests/api/`
- No new database tables or migrations needed — diff is computed on-the-fly from existing entities

### Rationale

The comparison endpoint follows the existing `model/ + service/ + endpoints/` module pattern. It reuses existing SeaORM entities (`sbom_package`, `sbom_advisory`, `package_license`) to compute set differences between two SBOMs. The p95 < 1s response time requirement for up to 2000 packages per SBOM is achievable with efficient SQL queries and in-memory diffing.

---

## trustify-ui

### Changes

- Add TypeScript interfaces for the comparison API response types in `src/api/`
- Add API client function `fetchSbomComparison(leftId, rightId)` in `src/api/rest.ts`
- Add React Query hook `useSbomComparison` in `src/hooks/`
- Add comparison page at `src/pages/SbomComparePage/` with SBOM selectors, compare button, export dropdown, and six collapsible diff sections per Figma design
- Add page-specific components: `DiffSection`, `AddedPackagesTable`, `RemovedPackagesTable`, `VersionChangesTable`, `NewVulnerabilitiesTable`, `ResolvedVulnerabilitiesTable`, `LicenseChangesTable`
- Register route `/sbom/compare` in `src/routes.tsx`
- Add MSW mock handler and fixture for the comparison endpoint in `tests/mocks/`
- Add unit tests for the comparison page
- Add Playwright E2E test for the comparison workflow

### Rationale

The comparison page follows the existing page structure pattern (`src/pages/<PageName>/` with sub-components). It reuses the existing `useSboms` hook for SBOM selectors, the `SeverityBadge` shared component for vulnerability severity display, and the `EmptyStateCard` component for the initial empty state. PatternFly `ExpandableSection`, `Table`, `Select`, `Badge`, and `Dropdown` components are used per the Figma design specifications. Virtualized lists will be used for diff sections with more than 100 rows per the non-functional requirements.
