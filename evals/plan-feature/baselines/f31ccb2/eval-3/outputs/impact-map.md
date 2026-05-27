# Repository Impact Map — TC-9003: SBOM Comparison View

## trustify-backend

changes:
  - Add comparison response model structs (SbomComparisonResult with added_packages, removed_packages, version_changes, new_vulnerabilities, resolved_vulnerabilities, license_changes)
  - Add comparison diffing logic in SbomService to compute structured diff between two SBOMs
  - Add GET /api/v2/sbom/compare endpoint with left and right query parameters
  - Register comparison endpoint route in SBOM endpoint module
  - Add integration tests for the comparison endpoint

## trustify-ui

changes:
  - Add TypeScript interfaces for the comparison API response in models.ts
  - Add API client function for the comparison endpoint in rest.ts
  - Add React Query hook for the comparison endpoint
  - Create SbomComparePage with header toolbar (SBOM selectors, Compare button, Export dropdown)
  - Create diff section components (Added Packages, Removed Packages, Version Changes, New Vulnerabilities, Resolved Vulnerabilities, License Changes) using PatternFly ExpandableSection and Table
  - Add empty state and loading state for the comparison page
  - Register /sbom/compare route in routes.tsx
  - Add unit tests and MSW mock handlers for the comparison page

---

## Workflow Mode

**Selected mode:** `feature-branch` (branch name: `TC-9003`)

**Rationale:** Atomicity indicator #4 (tightly coupled feature components) is present. The frontend comparison page at `/sbom/compare` requires the new backend `GET /api/v2/sbom/compare` endpoint to function. Neither side delivers value independently — merging the frontend without the backend would render a broken page, and merging the backend without the frontend would create an unused endpoint. All tasks must land together via a feature branch.

**Interdependent tasks:**
- The backend comparison endpoint task and the frontend comparison page task are tightly coupled — the frontend calls the backend endpoint and cannot render meaningful content without it.
- The frontend API client/hook task depends on the backend model task for the response shape contract.
