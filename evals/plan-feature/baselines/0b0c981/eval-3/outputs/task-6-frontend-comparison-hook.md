## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add a React Query hook `useSbomComparison` that wraps the `compareSboms` API client function, providing loading state, error handling, and caching for the SBOM comparison data. The hook is only enabled when both SBOM IDs are provided.

## Files to Create
- `src/hooks/useSbomComparison.ts` — React Query hook wrapping `compareSboms` with conditional enabling based on both IDs being present

## Implementation Notes
Follow the existing React Query hook pattern in `src/hooks/`:
- Mirror the structure of `src/hooks/useSboms.ts` and `src/hooks/useSbomById.ts` for the hook function signature and `useQuery` configuration.
- The hook should accept `leftId: string | undefined` and `rightId: string | undefined` parameters.
- Use the `enabled` option to prevent the query from firing until both `leftId` and `rightId` are defined: `enabled: !!leftId && !!rightId`.
- Query key should be `["sbom-comparison", leftId, rightId]` to ensure proper caching and refetching.
- Import `compareSboms` from `src/api/rest.ts` and `SbomComparisonResult` from `src/api/models.ts`.
- Return type is `UseQueryResult<SbomComparisonResult>`.

## Reuse Candidates
- `src/hooks/useSbomById.ts` — existing hook showing the pattern for a single-resource query with a parameter-based query key
- `src/hooks/useSboms.ts` — existing hook showing the `useQuery` pattern for SBOM data

## Acceptance Criteria
- [ ] `useSbomComparison(leftId, rightId)` hook exists in `src/hooks/useSbomComparison.ts`
- [ ] Hook uses React Query's `useQuery` with conditional `enabled` flag
- [ ] Hook does not fire when either ID is undefined
- [ ] Hook returns `UseQueryResult<SbomComparisonResult>` with loading, error, and data states

## Test Requirements
- [ ] Unit test: verify hook does not fire the API call when one or both IDs are undefined
- [ ] Unit test: verify hook returns comparison data when both IDs are provided (using MSW mock handler)

## Dependencies
- Depends on: Task 2 — Create feature branch TC-9003 from main (trustify-ui)
- Depends on: Task 5 — Add SBOM comparison API types and client function

[sdlc-workflow] Description digest: sha256:4a583821e5583237e402308a474143f2b9aefb5b326fb17c63c24ad8ac9cb4ed
