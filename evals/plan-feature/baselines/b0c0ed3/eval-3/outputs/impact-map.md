# Repository Impact Map — TC-9003: SBOM Comparison View

## trustify-backend

```
trustify-backend:
  changes:
    - Add SbomComparisonResult model with diff category structs (added_packages, removed_packages, version_changes, new_vulnerabilities, resolved_vulnerabilities, license_changes)
    - Add comparison service method to SbomService that computes a structured diff between two SBOMs by querying existing package, advisory, and license data
    - Add GET /api/v2/sbom/compare endpoint that accepts left and right SBOM ID query params and returns the structured diff
    - Add integration tests for the comparison endpoint covering: valid comparison, missing SBOM IDs, identical SBOMs, large SBOM diffs
```

## trustify-ui

```
trustify-ui:
  changes:
    - Add TypeScript interfaces for the comparison API response shape (SbomComparisonResult and its nested types)
    - Add API client function fetchSbomComparison() in rest.ts to call GET /api/v2/sbom/compare
    - Add React Query hook useSbomComparison for the comparison endpoint
    - Add SbomComparePage with header toolbar (two SBOM Select dropdowns, Compare button, Export dropdown) and six collapsible diff sections using PatternFly ExpandableSection, Badge, and Table components
    - Add route definition for /sbom/compare in routes.tsx
    - Add checkbox selection and "Compare selected" button to SbomListPage for navigating to comparison
    - Add unit tests for SbomComparePage using MSW mocks and React Testing Library
```
