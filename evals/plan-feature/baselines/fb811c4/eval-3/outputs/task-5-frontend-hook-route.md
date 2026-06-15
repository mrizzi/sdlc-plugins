# Task 5 — Add SBOM comparison hook and route

## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Create a React Query hook for the SBOM comparison data and register the `/sbom/compare` route in the application router. The hook wraps `fetchSbomComparison()` with proper query key management and enabled/disabled state (the query should only run when both SBOM IDs are provided). The route is lazy-loaded following the existing routing pattern.

## Files to Modify
- `src/routes.tsx` — add `/sbom/compare` route with lazy-loaded page component

## Files to Create
- `src/hooks/useSbomComparison.ts` — React Query hook for SBOM comparison

## Implementation Notes
**React Query hook** in `src/hooks/useSbomComparison.ts`:

```typescript
import { useQuery } from "@tanstack/react-query";
import { fetchSbomComparison } from "../api/rest";

export const useSbomComparison = (leftId: string | undefined, rightId: string | undefined) =>
  useQuery({
    queryKey: ["sbom-comparison", leftId, rightId],
    queryFn: () => fetchSbomComparison(leftId!, rightId!),
    enabled: !!leftId && !!rightId,
  });
```

Follow the existing hook pattern in `src/hooks/useSboms.ts` and `src/hooks/useSbomById.ts`.

**Route registration** in `src/routes.tsx`:
- Add a lazy import for SbomComparePage
- Register path `/sbom/compare` before any `/sbom/:id` route to avoid path conflicts
- Follow the existing React Router v6 lazy-loading pattern

Per CONVENTIONS.md §State Management: React Query (TanStack Query) for server state; no Redux.
Applies: task creates `src/hooks/useSbomComparison.ts` matching the convention's state management scope.

Per CONVENTIONS.md §Routing: React Router v6 with lazy-loaded page components.
Applies: task modifies `src/routes.tsx` matching the convention's routing scope.

## Acceptance Criteria
- [ ] `useSbomComparison` hook calls `fetchSbomComparison` only when both IDs are provided
- [ ] Hook uses a descriptive query key `["sbom-comparison", leftId, rightId]`
- [ ] Route `/sbom/compare` is registered and lazy-loads the comparison page
- [ ] Route is placed before any parameterized `/sbom/:id` route

## Test Requirements
- [ ] Unit test: hook does not fetch when leftId is undefined
- [ ] Unit test: hook does not fetch when rightId is undefined
- [ ] Unit test: hook fetches and returns data when both IDs are provided (using MSW mock)

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003
- Depends on: Task 4 — Add SBOM comparison API types and client function

[sdlc-workflow] Description digest: sha256-md:0f5c082bd31ce6fdb22d02ec99b693de543a7a646f0858005c29146d36d20ce4
