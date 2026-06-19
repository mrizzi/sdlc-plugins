## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Create a React Query hook that wraps the `compareSboms` API client function. This hook manages the server state for the comparison result, handling loading, error, and success states. It will be consumed by the ComparisonPage component to fetch and display the SBOM diff.

## Files to Create
- `src/hooks/useSbomComparison.ts` — React Query hook: `useSbomComparison(leftId: string | undefined, rightId: string | undefined)` returning query result with `SbomComparison` data

## Implementation Notes
Follow the existing hook patterns in `src/hooks/useSboms.ts` and `src/hooks/useSbomById.ts`.

```typescript
import { useQuery } from "@tanstack/react-query";
import { compareSboms } from "@app/api/rest";
import { SbomComparison } from "@app/api/models";

export const useSbomComparison = (leftId: string | undefined, rightId: string | undefined) => {
  return useQuery<SbomComparison>({
    queryKey: ["sbom-comparison", leftId, rightId],
    queryFn: () => compareSboms(leftId!, rightId!),
    enabled: !!leftId && !!rightId,
  });
};
```

Key behaviors:
- The query is disabled (`enabled: false`) until both `leftId` and `rightId` are provided. This supports the page's initial empty state before the user selects two SBOMs.
- Query key includes both IDs for proper caching: changing either ID triggers a refetch.
- No stale time configuration needed beyond defaults; comparison results are not expected to change frequently.

## Reuse Candidates
- `src/hooks/useSboms.ts` — Pattern for React Query hook with `useQuery`
- `src/hooks/useSbomById.ts` — Pattern for conditional query execution with `enabled`

## Acceptance Criteria
- [ ] Hook is defined and exported from `src/hooks/useSbomComparison.ts`
- [ ] Query is disabled when either `leftId` or `rightId` is undefined
- [ ] Query key includes both SBOM IDs
- [ ] Returns standard React Query result object (data, isLoading, isError, error)
- [ ] TypeScript compilation passes

## Test Requirements
- [ ] Hook returns loading state when query is enabled
- [ ] Hook does not fire when either ID is undefined

## Dependencies
- Depends on: Task 6 — Frontend API types and client functions
