# Repository Impact Map — TC-9003: SBOM Comparison View

## trustify-backend

changes:
  - Add SBOM comparison diff model structs (SbomComparisonResult with added_packages, removed_packages, version_changes, new_vulnerabilities, resolved_vulnerabilities, license_changes) in modules/fundamental/src/sbom/model/
  - Add SBOM comparison service method to compute structured diff between two SBOMs on-the-fly from existing package, advisory, and license data (no new database tables)
  - Add GET /api/v2/sbom/compare endpoint with left and right query parameters returning the structured diff response
  - Add integration tests for the comparison endpoint covering normal diff, empty diff, invalid SBOM IDs, and performance with large SBOMs

## trustify-ui

changes:
  - Add TypeScript interfaces for the SBOM comparison API response shape in src/api/models.ts
  - Add API client function fetchSbomComparison() in src/api/rest.ts to call GET /api/v2/sbom/compare
  - Add React Query hook useSbomComparison in src/hooks/ for the comparison endpoint
  - Add SbomComparePage component with header toolbar (SBOM selectors, Compare button, Export dropdown) and six collapsible diff sections per Figma design
  - Add diff section sub-components using PatternFly ExpandableSection, Badge, and composable Table
  - Add route definition for /sbom/compare with URL query parameter support for left/right SBOM IDs
  - Update SbomListPage to support checkbox selection and "Compare selected" navigation action
  - Add MSW mock handlers and fixtures for the comparison endpoint
  - Add unit tests for comparison page and E2E test for the comparison workflow

## Workflow Mode

**Selected mode:** `feature-branch`

**Rationale:** Atomicity indicator #4 (tightly coupled feature components) applies. The frontend comparison page requires the new backend `GET /api/v2/sbom/compare` endpoint, which does not yet exist. Merging only the frontend would produce a non-functional page calling a missing endpoint; merging only the backend provides no user-facing value. Both sides must land together for the feature to function.

**Interdependent tasks:** All backend implementation tasks (model, service, endpoint) and frontend implementation tasks (API layer, comparison page, routing) are interdependent. The frontend API client, hook, and page depend on the backend endpoint existing and returning the expected response shape. The merge-branch bookend depends on all intermediate tasks.
