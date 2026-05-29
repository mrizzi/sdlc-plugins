# Repository Impact Map — TC-9003: SBOM Comparison View

## trustify-backend

changes:
- Add SBOM comparison diff model structs (SbomComparisonResult, AddedPackage, RemovedPackage, VersionChange, NewVulnerability, ResolvedVulnerability, LicenseChange) in modules/fundamental/src/sbom/model/
- Add SBOM comparison service logic in modules/fundamental/src/sbom/service/ to compute diffs between two SBOMs using existing package, advisory, and license data
- Add GET /api/v2/sbom/compare endpoint in modules/fundamental/src/sbom/endpoints/ accepting left and right SBOM IDs as query parameters
- Register the new comparison route in the SBOM endpoint module
- Add integration tests for the comparison endpoint in tests/api/

## trustify-ui

changes:
- Add TypeScript interfaces for SBOM comparison response types in src/api/models.ts
- Add API client function for the comparison endpoint in src/api/rest.ts
- Add React Query hook for the comparison API call in src/hooks/
- Create SbomComparePage component with header toolbar (SBOM selectors, Compare button, Export dropdown) and collapsible diff sections (Added Packages, Removed Packages, Version Changes, New Vulnerabilities, Resolved Vulnerabilities, License Changes) using PatternFly components
- Add page-specific components: DiffSection, CompareToolbar
- Register /sbom/compare route in src/routes.tsx
- Add checkbox selection and "Compare selected" action to SbomListPage
- Add unit tests with MSW mocks and test fixtures for the comparison page
- Add E2E test for the comparison workflow

---

## Workflow Mode Decision

**Selected mode:** `feature-branch`

**Rationale:** Atomicity indicator #4 (Tightly coupled feature components) is present. The frontend comparison page at `/sbom/compare` depends on the new backend endpoint `GET /api/v2/sbom/compare?left={id1}&right={id2}`, which does not yet exist. Merging the frontend changes to `main` without the backend endpoint would result in a broken comparison page that cannot fetch data. Similarly, merging the backend endpoint alone is safe but the feature is not user-visible until the frontend lands. Coordinated delivery via a feature branch ensures both sides land together.

**Interdependent tasks:**
- Frontend API client/hook tasks depend on backend endpoint task (the frontend calls an endpoint that must exist)
- Frontend comparison page task depends on frontend API types/hook task
- Frontend tests task depends on frontend comparison page task

**Bookend tasks:**
- Task 1: Create feature branch TC-9003 from main (trustify-backend)
- Task 2: Create feature branch TC-9003 from main (trustify-ui)
- Task 8: Merge feature branch TC-9003 to main (trustify-backend)
- Task 9: Merge feature branch TC-9003 to main (trustify-ui)
