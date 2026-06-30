# Repository Impact Map — TC-9003: SBOM Comparison View

## trustify-backend

changes:
  - Add `SbomComparisonResult` response model with diff categories (added/removed packages, version changes, new/resolved vulnerabilities, license changes)
  - Add `SbomService::compare` method to compute on-the-fly diff between two SBOMs using existing package, advisory, and license data
  - Add `GET /api/v2/sbom/compare?left={id1}&right={id2}` endpoint handler with query parameter validation
  - Register the comparison route in the SBOM endpoint module
  - Add integration tests for the comparison endpoint covering normal diffs, identical SBOMs, and invalid SBOM IDs

## trustify-ui

changes:
  - Add TypeScript interfaces for the comparison API response shape to the models file
  - Add `fetchSbomComparison()` API client function to rest.ts
  - Add `useSbomComparison` React Query hook for the comparison endpoint
  - Create `SbomComparisonPage` with SBOM selector dropdowns, diff sections (ExpandableSection + Badge + Table for each category), empty state, and loading state
  - Add `/sbom/compare` route to the route definitions
  - Add "Compare selected" action to the SBOM list page for selecting two SBOMs and navigating to the comparison view
  - Add MSW mock handler and fixture data for the comparison endpoint
  - Add unit tests for the comparison page component
  - Add Playwright E2E test for the comparison workflow

## Workflow Mode Decision

**Selected mode:** `feature-branch`

**Rationale:** Atomicity indicator #4 (Tightly coupled feature components) is present. The frontend comparison page at `/sbom/compare` depends on the new backend endpoint `GET /api/v2/sbom/compare` which does not yet exist. Merging the frontend without the backend would result in a broken comparison page that calls a non-existent endpoint. Merging the backend alone is safe but delivers no user value. Both sides must land together for the feature to function.

**Interdependent tasks:** All frontend tasks depend on the backend comparison endpoint task. The backend endpoint must exist before the frontend can successfully call it.

The `workflow:feature-branch` label will be applied to the feature issue TC-9003.
