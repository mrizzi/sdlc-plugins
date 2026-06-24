## Repository
trustify-ui

## Target Branch
main

## Description
Create a React Query hook `useSbomComparison` that wraps the `compareSboms` API client function. The hook accepts two SBOM IDs, calls the comparison endpoint, and returns the query result with loading/error/data states. The query is disabled when either SBOM ID is missing.

## Files to Create
- `src/hooks/useSbomComparison.ts` — React Query hook for SBOM comparison

## Implementation Notes
Follow the existing hook pattern in `src/hooks/useSboms.ts` and `src/hooks/useSbomById.ts`. Use `useQuery` from TanStack Query with a descriptive query key.

```typescript
import { useQuery } from "@tanstack/react-query";
import { compareSboms } from "../api/rest";
import { SbomComparisonResult } from "../api/models";

export const useSbomComparison = (leftId: string | undefined, rightId: string | undefined) => {
  return useQuery<SbomComparisonResult>({
    queryKey: ["sbom-comparison", leftId, rightId],
    queryFn: () => compareSboms(leftId!, rightId!),
    enabled: !!leftId && !!rightId,
  });
};
```

The `enabled` flag ensures the query only fires when both IDs are present, supporting the use case where the page loads without query params (empty state).

Per Key Conventions (State management): React Query (TanStack Query) for server state; hooks in `src/hooks/`. Applies: task creates `src/hooks/useSbomComparison.ts` matching the convention's hooks directory scope.

Per Key Conventions (Naming): camelCase for hooks. Applies: task creates `src/hooks/useSbomComparison.ts` matching the convention's naming scope.

## Acceptance Criteria
- [ ] `useSbomComparison` hook is exported from `src/hooks/useSbomComparison.ts`
- [ ] Hook accepts two optional SBOM ID strings
- [ ] Query is disabled when either ID is undefined
- [ ] Query key includes both SBOM IDs for proper cache separation
- [ ] TypeScript compiles without errors

## Test Requirements
- [ ] Verify hook returns loading state initially when IDs are provided
- [ ] Verify hook does not fire query when either ID is missing

## Dependencies
- Depends on: Task 5 — Frontend API types and client function

[sdlc-workflow] Description digest: sha256-md:73c8f921232ebe4c7fdd7a722f75d50ea144d0ab1e19d7f2995ee333a2becf5e
