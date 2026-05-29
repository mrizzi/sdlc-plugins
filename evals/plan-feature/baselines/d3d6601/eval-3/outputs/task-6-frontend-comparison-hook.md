## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add a React Query hook `useSbomComparison` that wraps the `fetchSbomComparison` API client function, providing loading state, error handling, and caching for the comparison page. The hook should only execute the query when both SBOM IDs are provided.

## Files to Create
- `src/hooks/useSbomComparison.ts` — React Query hook for the SBOM comparison endpoint

## Implementation Notes
- Follow the existing hook pattern in `src/hooks/useSboms.ts` and `src/hooks/useSbomById.ts` — use `useQuery` from React Query (TanStack Query) with a query key that includes both SBOM IDs.
- The hook should accept `leftId: string | undefined` and `rightId: string | undefined` as parameters.
- Use the `enabled` option to only fire the query when both `leftId` and `rightId` are defined and non-empty: `enabled: !!leftId && !!rightId`.
- Query key: `["sbom-comparison", leftId, rightId]` — this ensures the cache is keyed by the specific comparison pair.
- Return the standard React Query result object (`data`, `isLoading`, `isError`, `error`).

## Reuse Candidates
- `src/hooks/useSboms.ts` — follow the same `useQuery` pattern, query key structure, and export style
- `src/hooks/useSbomById.ts` — reference for hooks that accept an ID parameter with `enabled` conditional
- `src/api/rest.ts::fetchSbomComparison` — the API function to call inside the query function

## Acceptance Criteria
- [ ] `useSbomComparison(leftId, rightId)` hook is exported from `src/hooks/useSbomComparison.ts`
- [ ] Hook returns React Query result with `data` typed as `SbomComparison`
- [ ] Query only executes when both `leftId` and `rightId` are provided (non-empty)
- [ ] Query key includes both SBOM IDs for correct cache invalidation

## Test Requirements
- [ ] Unit test: verify hook does not fire query when `leftId` is undefined
- [ ] Unit test: verify hook does not fire query when `rightId` is undefined
- [ ] Unit test: verify hook fires query and returns data when both IDs are provided (using MSW mock)

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 5 — Add SBOM comparison API types and client function

[sdlc-workflow] Description digest: sha256:43853bd51c97071e6e4fd702a05dbb995edd0270a5bc843a8355be8a42c3ae95
