# Task 6: Add SBOM comparison React Query hook

- **Jira parent**: TC-9003
- **Priority**: Critical
- **Fix Versions**: RHTPA 1.5.0
- **Dependencies**: Task 5

## Repository

trustify-ui

## Target Branch

TC-9003

## Description

Create a React Query hook that wraps the `fetchSbomComparison` client function, providing loading/error/data states and automatic caching for the comparison page. The hook should only execute the query when both SBOM IDs are provided (enabled conditionally).

## Files to Create

- `src/hooks/useSbomComparison.ts` -- React Query hook: `useSbomComparison(leftId: string | undefined, rightId: string | undefined)`

## Acceptance Criteria

- [ ] Hook uses `useQuery` from TanStack Query with a unique query key incorporating both SBOM IDs
- [ ] Query is disabled (`enabled: false`) when either `leftId` or `rightId` is undefined or empty
- [ ] Hook returns standard React Query result: `{ data, isLoading, isError, error, refetch }`
- [ ] Query key follows the pattern `["sbom-comparison", leftId, rightId]` for proper cache invalidation
- [ ] Hook is exported as a named export

## Test Requirements

- Unit test: verify the hook does not fire a request when `leftId` is undefined.
- Unit test: verify the hook calls `fetchSbomComparison` with correct parameters when both IDs are provided.

## Implementation Notes

Follow the pattern of existing hooks like `src/hooks/useSbomById.ts`. The hook file structure:

```typescript
import { useQuery } from "@tanstack/react-query";
import { fetchSbomComparison } from "@app/api/rest";

export const useSbomComparison = (leftId: string | undefined, rightId: string | undefined) => {
  return useQuery({
    queryKey: ["sbom-comparison", leftId, rightId],
    queryFn: () => fetchSbomComparison(leftId!, rightId!),
    enabled: !!leftId && !!rightId,
  });
};
```

Use camelCase for the file name per the naming convention for hooks.

## Applicable Conventions

- **API layer** (React Query hooks in src/hooks/): Applies: task creates `src/hooks/useSbomComparison.ts` matching the convention's React Query hooks scope.
- **State management** (React Query / TanStack Query for server state): Applies: task creates hook using `useQuery` matching the convention's state management scope.
