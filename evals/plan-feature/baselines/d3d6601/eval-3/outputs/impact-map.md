# Repository Impact Map — TC-9003: SBOM Comparison View

## Workflow Mode

**Mode:** `feature-branch`

**Rationale:** This feature exhibits atomicity indicator #4 (Tightly coupled feature components). The frontend comparison page requires the new backend `GET /api/v2/sbom/compare` endpoint, which does not yet exist. Neither side functions independently — merging the backend endpoint alone adds unused code, and merging the frontend alone would call a nonexistent API. Both must land together.

**Interdependent tasks:** All frontend tasks (API types, hook, comparison page, route registration) depend on the backend comparison endpoint task.

---

## Impact Map

```
trustify-backend:
  changes:
    - Add SbomComparison response model with diff section structs (added_packages, removed_packages, version_changes, new_vulnerabilities, resolved_vulnerabilities, license_changes)
    - Add SbomComparisonService with diff computation logic that compares two SBOMs by fetching their packages and advisories
    - Add GET /api/v2/sbom/compare?left={id1}&right={id2} endpoint returning SbomComparison
    - Add integration tests for the comparison endpoint

trustify-ui:
  changes:
    - Add TypeScript interfaces for the comparison API response shape
    - Add API client function fetchSbomComparison(leftId, rightId) in rest.ts
    - Add React Query hook useSbomComparison for the comparison endpoint
    - Add SbomComparePage with header toolbar (SBOM selectors, Compare button, Export dropdown) and collapsible diff sections per Figma design
    - Add route /sbom/compare to routes.tsx with URL query param support (left, right)
    - Add unit tests for the comparison page and E2E test for the comparison workflow
```

## Task Summary

| # | Repository | Summary | Target Branch |
|---|---|---|---|
| 1 | trustify-backend | Create feature branch TC-9003 from main | main |
| 2 | trustify-backend | Add SBOM comparison response model types | TC-9003 |
| 3 | trustify-backend | Add SBOM comparison service with diff logic | TC-9003 |
| 4 | trustify-backend | Add GET /api/v2/sbom/compare endpoint and integration tests | TC-9003 |
| 5 | trustify-ui | Add SBOM comparison API types and client function | TC-9003 |
| 6 | trustify-ui | Add useSbomComparison React Query hook | TC-9003 |
| 7 | trustify-ui | Add SBOM comparison page UI with diff sections | TC-9003 |
| 8 | trustify-ui | Add comparison route and E2E tests | TC-9003 |
| 9 | trustify-backend | Merge feature branch TC-9003 to main | main |
