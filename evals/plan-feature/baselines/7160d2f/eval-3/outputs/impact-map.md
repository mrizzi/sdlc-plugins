# Repository Impact Map — TC-9003: SBOM Comparison View

## trustify-backend

changes:
  - Add SbomComparison response model with diff categories (added_packages, removed_packages, version_changes, new_vulnerabilities, resolved_vulnerabilities, license_changes)
  - Add comparison service logic in SbomService to compute structured diff between two SBOMs using existing package, advisory, and license data
  - Add GET /api/v2/sbom/compare endpoint with left and right query parameters
  - Add integration tests for the comparison endpoint covering normal diff, empty diff, and large SBOM scenarios

## trustify-ui

changes:
  - Add TypeScript interfaces for the comparison API response shape in api/models.ts
  - Add API client function for the comparison endpoint in api/rest.ts
  - Add React Query hook for the comparison query
  - Add SbomComparePage with SBOM selectors, compare button, and diff section layout using PatternFly components
  - Add route definition for /sbom/compare
  - Add selection UI (checkboxes + "Compare selected" button) to the existing SbomListPage
  - Add unit tests for the comparison page components
  - Add E2E test for the comparison workflow

## Workflow Mode

**Selected mode:** `feature-branch`

**Rationale:** Atomicity indicator #4 (Tightly coupled feature components) is present. The frontend comparison page requires the new `GET /api/v2/sbom/compare` backend endpoint to function. Merging the frontend without the backend would result in a broken comparison page that calls a non-existent endpoint. Merging the backend alone is harmless but the feature is not usable without the frontend. Both sides must land together for the feature to be complete.

**Interdependent tasks:** All frontend tasks depend on the backend comparison endpoint task. The comparison page cannot render meaningful data without the backend diff service.
