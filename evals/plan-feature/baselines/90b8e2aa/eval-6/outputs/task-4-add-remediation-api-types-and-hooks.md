## Repository
trustify-ui

## Target Branch
main

## Description
Add TypeScript interfaces for the remediation API response types, Axios client functions for fetching remediation data, and React Query hooks for the remediation summary and by-product endpoints. This establishes the data layer that the remediation dashboard page will consume.

## Files to Modify
- `src/api/models.ts` — add `RemediationSummary` interface (severity, status, count), `ProductRemediation` interface (product, total, open, inProgress, resolved), and `RemediationByProductResponse` interface (items, total)
- `src/api/rest.ts` — add `fetchRemediationSummary()` and `fetchRemediationByProduct()` functions using the Axios client

## Files to Create
- `src/hooks/useRemediationSummary.ts` — React Query hook wrapping `fetchRemediationSummary()` with appropriate query key and stale time
- `src/hooks/useRemediationByProduct.ts` — React Query hook wrapping `fetchRemediationByProduct()` with query key, pagination params, and filter params

## Implementation Notes
- Per CONVENTIONS.md §API layer: Axios client in `src/api/client.ts`; typed API functions in `src/api/rest.ts`; React Query hooks in `src/hooks/`. Follow this three-layer pattern. See `src/api/rest.ts::fetchAdvisories()` and `src/hooks/useAdvisories.ts` for reference.
  Applies: task modifies `src/api/rest.ts` matching the convention's TypeScript API file scope.
- Per CONVENTIONS.md §Naming: use camelCase for hooks and utility functions, PascalCase for interface names.
  Applies: task creates `src/hooks/useRemediationSummary.ts` matching the convention's TypeScript file scope.
- Per CONVENTIONS.md §State management: use React Query (TanStack Query) for server state, no Redux. Hooks should use `useQuery` with typed generics.
  Applies: task creates `src/hooks/useRemediationSummary.ts` matching the convention's TypeScript hook file scope.

**Backend API contracts:**
- `GET /api/v2/remediation/summary` — response shape: `{ items: RemediationSummary[] }` where `RemediationSummary = { severity: string, status: string, count: number }` (see `modules/remediation/src/endpoints/summary.rs` in trustify-backend)
- `GET /api/v2/remediation/by-product?offset={offset}&limit={limit}` — response shape: `{ items: ProductRemediation[], total: number }` where `ProductRemediation = { product: string, total: number, open: number, in_progress: number, resolved: number }` (see `modules/remediation/src/endpoints/by_product.rs` in trustify-backend)

Verify these contracts against the backend repo during implementation using the implement-task cross-repo API verification step.

## Reuse Candidates
- `src/api/rest.ts::fetchAdvisories` — existing API client function pattern with Axios; reference for structuring remediation fetch functions
- `src/api/rest.ts::fetchSboms` — existing API client function with pagination parameters; reference for the by-product fetch function
- `src/hooks/useAdvisories.ts` — React Query hook pattern with query key and options; reference for remediation hooks
- `src/hooks/useSboms.ts` — React Query hook with pagination support; reference for by-product hook with offset/limit params
- `src/api/models.ts` — existing TypeScript interfaces for API types; extend with remediation interfaces

## Acceptance Criteria
- [ ] `RemediationSummary` and `ProductRemediation` TypeScript interfaces are defined in `models.ts`
- [ ] `fetchRemediationSummary()` calls `GET /api/v2/remediation/summary` and returns typed data
- [ ] `fetchRemediationByProduct()` calls `GET /api/v2/remediation/by-product` with pagination params and returns typed data
- [ ] `useRemediationSummary` hook provides loading, error, and data states
- [ ] `useRemediationByProduct` hook supports pagination parameters and filter parameters

## Test Requirements
- [ ] Unit test for `fetchRemediationSummary()` verifying correct API path and response parsing
- [ ] Unit test for `fetchRemediationByProduct()` verifying correct API path, query params, and response parsing
- [ ] Unit test for `useRemediationSummary` hook verifying React Query integration
- [ ] Unit test for `useRemediationByProduct` hook verifying pagination parameter handling

## Dependencies
- None (frontend can be developed with mocked backend responses; backend endpoints from Tasks 1-2 must be deployed before integration testing)
