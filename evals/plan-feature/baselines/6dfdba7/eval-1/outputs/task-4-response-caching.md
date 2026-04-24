## Repository
trustify-backend

## Description
Add 5-minute HTTP caching to the advisory summary endpoint response. The project uses `tower-http` caching middleware, and the cache configuration should be applied at the route level when registering the advisory summary endpoint. This satisfies the TC-9001 requirement that responses are cached for 5 minutes to ensure low-latency repeated calls from dashboard widgets.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/mod.rs` — Apply cache-control middleware or headers to the `advisory-summary` route with a 300-second max-age
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — Alternatively, set `Cache-Control: max-age=300` response header directly in the handler if the project uses per-handler header injection rather than middleware

## Implementation Notes
- Check how caching is configured for existing endpoints in `modules/fundamental/src/sbom/endpoints/mod.rs` and other endpoint modules. The project uses `tower-http` caching middleware per the conventions doc.
- Two possible patterns:
  1. **Middleware approach**: Wrap the advisory-summary route with a `tower-http::set_header::SetResponseHeaderLayer` that adds `Cache-Control: public, max-age=300`. This is applied in the route registration in `mod.rs`.
  2. **Handler approach**: Return a tuple `([(header::CACHE_CONTROL, "public, max-age=300")], Json(summary))` from the handler function in `advisory_summary.rs`.
- Prefer whichever pattern is already established in the codebase. If existing list endpoints (e.g., `list.rs`) already have caching configured, replicate that pattern.
- The 5-minute TTL (300 seconds) matches the requirement. Use `public` directive since severity counts are not user-specific.
- The `vary` header should not include authorization-specific headers since these counts are SBOM-scoped, not user-scoped.

## Acceptance Criteria
- [ ] Response from `GET /api/v2/sbom/{id}/advisory-summary` includes `Cache-Control` header with `max-age=300`
- [ ] Caching approach is consistent with patterns used by other endpoints in the codebase
- [ ] Cache directive uses `public` since data is not user-specific

## Test Requirements
- [ ] Integration test: verify response headers include `Cache-Control: public, max-age=300` (or equivalent)

## Verification Commands
- `cargo check -p trustify-fundamental` — should compile without errors

## Dependencies
- Depends on: Task 3 — Advisory summary endpoint (route must exist before adding cache configuration)
