# Task 5: Create React Query hook for SBOM comparison

## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Create a React Query hook that wraps the `fetchSbomComparison` API client function. The hook manages loading, error, and success states for the comparison query and is consumed by the comparison page component. It follows the existing hook patterns in `src/hooks/` and supports conditional fetching (only runs when both SBOM IDs are provided).

## Files to Create
- `src/hooks/useSbomComparison.ts` — React Query hook that calls `fetchSbomComparison(leftId, rightId)` and returns typed query state

## Implementation Notes
- Follow the pattern in `src/hooks/useSbomById.ts` for a parameterized query hook:
  ```typescript
  export const useSbomComparison = (leftId: string | undefined, rightId: string | undefined) => {
    return useQuery({
      queryKey: ["sbom-comparison", leftId, rightId],
      queryFn: () => fetchSbomComparison(leftId!, rightId!),
      enabled: !!leftId && !!rightId,
    });
  };
  ```
- The hook should return the standard React Query result object (`data`, `isLoading`, `isError`, `error`).
- The `enabled` option ensures the query only fires when both SBOM IDs are defined, preventing unnecessary API calls on initial page load.
- The query key includes both IDs so React Query caches each unique comparison separately.
- Import `fetchSbomComparison` from `src/api/rest.ts` and `SbomComparison` from `src/api/models.ts`.

## Reuse Candidates
- `src/hooks/useSbomById.ts` — pattern reference for parameterized React Query hook with conditional fetching
- `src/hooks/useSboms.ts` — pattern reference for query key naming and hook structure
- `src/api/rest.ts::fetchSbomComparison` — the API client function created in Task 4

## Acceptance Criteria
- [ ] Hook is exported from `src/hooks/useSbomComparison.ts`
- [ ] Hook accepts `leftId` and `rightId` parameters (both optional)
- [ ] Query only fires when both IDs are provided (`enabled` guard)
- [ ] Query key includes both SBOM IDs for proper cache isolation
- [ ] Return type is properly typed as `UseQueryResult<SbomComparison>`
- [ ] TypeScript compilation passes with no errors

## Test Requirements
- [ ] Hook behavior is verified via the comparison page component tests in Task 6
- [ ] MSW mock handler (Task 8) provides the mock data for hook integration testing

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 4 — Add SBOM comparison TypeScript types and API client function

`[sdlc-workflow] Description digest: sha256-md:e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7`
