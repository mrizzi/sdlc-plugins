## Repository
trustify-ui

## Target Branch
main

## Description
Register the SBOM comparison page route in the application router. Add a `/sbom/compare` route pointing to the new `SbomComparePage` component with lazy loading, consistent with existing route patterns.

## Files to Modify
- `src/routes.tsx` — Add route definition for `/sbom/compare` with lazy-loaded `SbomComparePage`

## Implementation Notes
Add the comparison route to `src/routes.tsx` following the existing pattern of lazy-loaded page components using React Router v6.

```typescript
const SbomComparePage = React.lazy(() => import("./pages/SbomComparePage/SbomComparePage"));
```

Add the route entry. Place the `/sbom/compare` route before any `/sbom/:id` route to avoid the `:id` segment matching "compare" as a parameter.

Per Key Conventions (Routing): React Router v6 with lazy-loaded page components. Applies: task modifies `src/routes.tsx` matching the convention's routing scope.

## Acceptance Criteria
- [ ] `/sbom/compare` route is registered in `src/routes.tsx`
- [ ] Route lazy-loads `SbomComparePage` component
- [ ] Route is placed before dynamic `/sbom/:id` routes to avoid conflicts
- [ ] Navigation to `/sbom/compare` renders the comparison page
- [ ] Navigation to `/sbom/compare?left=id1&right=id2` pre-populates selectors

## Test Requirements
- [ ] Verify route renders SbomComparePage when navigating to `/sbom/compare`
- [ ] Verify route does not interfere with existing `/sbom/:id` routes

## Dependencies
- Depends on: Task 7 — SBOM comparison page component

[sdlc-workflow] Description digest: sha256-md:65b981708eb9374b6401f889081044adb04fc06a5016b0985dc2cae338a4ea5f
