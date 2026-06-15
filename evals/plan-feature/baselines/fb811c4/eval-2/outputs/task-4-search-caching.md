## Repository
trustify-backend

## Target Branch
main

## Description
Add application-level query result caching for repeated search queries to reduce database load and improve response times for frequently executed searches. This further addresses the "search should be faster" requirement.

Assumption (pending clarification): The feature says search should be "fast enough" without specifying latency targets or whether caching is the desired approach. This task assumes that caching repeated identical queries is an appropriate optimization. Cache TTL is set to a conservative default (60 seconds) since no data freshness requirements are specified.

## Files to Modify
- `modules/search/src/service/mod.rs` — Add an in-memory LRU cache layer around search queries, keyed by query string + filter parameters
- `modules/search/src/lib.rs` — Configure cache settings (capacity, TTL) as module-level configuration

## Implementation Notes
In `modules/search/src/service/mod.rs`:
- Add an LRU cache (e.g., using `lru` or `moka` crate) to `SearchService` that caches serialized search results keyed by (query_string, filters, pagination) tuple
- Cache lookup should happen before database query execution
- Cache entries should have a configurable TTL (default: 60 seconds)
- Cache should be invalidated or bypassed when data ingestion occurs (the ingestor in `modules/ingestor/src/service/mod.rs` could trigger cache invalidation, but cross-module coupling should be minimized — TTL-based expiry is simpler)

Assumption (pending clarification): Without knowing the data update frequency, the TTL is set conservatively. If data changes frequently (e.g., continuous SBOM ingestion via `modules/ingestor/`), a shorter TTL or event-based invalidation may be needed.

In `modules/search/src/lib.rs`:
- Expose cache configuration (max_capacity, ttl_seconds) that can be set during module initialization

The existing `tower-http` caching middleware (mentioned in repo conventions) handles HTTP-level caching. This task adds application-level caching within the service layer, which operates at a different level and complements HTTP caching.

Per CONVENTIONS.md §Error handling: Cache miss fallback to database must maintain `Result<T, AppError>` with `.context()` wrapping.
Applies: task modifies `modules/search/src/service/mod.rs` matching the error handling convention.

Per CONVENTIONS.md §Caching: Complements existing `tower-http` caching middleware with application-level caching.
Applies: task modifies search service caching behavior.

## Acceptance Criteria
- [ ] Repeated identical search queries within TTL are served from cache without database query
- [ ] Cache key includes query string, filter parameters, and pagination to avoid returning wrong results
- [ ] Cache has a configurable TTL (default 60 seconds) (note: TTL value assumed, pending clarification on acceptable data staleness)
- [ ] Cache has a bounded capacity to prevent unbounded memory growth
- [ ] Cache misses fall through to normal database query transparently
- [ ] Search correctness is not affected by caching — same results for same inputs

## Test Requirements
- [ ] Unit test: identical query within TTL returns cached result
- [ ] Unit test: different query parameters produce different cache keys (no false cache hits)
- [ ] Unit test: cache entry expires after TTL
- [ ] Integration test: search response time improves for repeated queries

## Dependencies
- Depends on: Task 2 — search-relevance-ranking (cache should store relevance-ranked results, not unranked ones)

[sdlc-workflow] Description digest: sha256-md:7b846c7cb6706f6a039d32f5eb8d935961cba1d34b96767962ffb7a7278adcc8
