## Repository
trustify-backend

## Description
Add query timing instrumentation to the search endpoint to measure and log search latency. Since the feature description specifies no quantitative performance targets ("should be faster," "fast enough"), this task adds the observability foundation needed to measure current performance, validate that the full-text search changes (Tasks 1-2) have improved latency, and establish baselines for future optimization.

**Ambiguity note:** The feature requirements "Search should be faster" and "Should be fast enough" provide no measurable performance targets. Without concrete latency goals, this task focuses on instrumentation so that performance can be measured, baselined, and iterated on. The product owner should define target latencies (e.g., p95 < 200ms) so that acceptance criteria can be made concrete in a follow-up (assumption pending clarification).

## Files to Modify
- `modules/search/src/service/mod.rs` — add timing instrumentation around search query execution, logging query duration
- `modules/search/src/endpoints/mod.rs` — optionally expose query timing in response headers (e.g., `X-Query-Time-Ms`) for client-side observability

## Implementation Notes
- Add timing instrumentation in `SearchService` (in `modules/search/src/service/mod.rs`) around the database query execution. Use `std::time::Instant` to measure elapsed time:
  ```
  let start = Instant::now();
  // ... execute search query ...
  let elapsed = start.elapsed();
  ```
- Log the query duration using the project's logging framework (likely `tracing` given the Rust/Axum stack). Log at `info` or `debug` level with structured fields:
  - `search_query`: the user's search term (redacted/truncated if needed)
  - `result_count`: number of results returned
  - `query_duration_ms`: elapsed time in milliseconds
  - `filters_applied`: which filters were active (entity_type, severity)
- Optionally add a response header `X-Query-Time-Ms` in the endpoint handler (`modules/search/src/endpoints/mod.rs`) so that API consumers can observe search latency without parsing logs.
- Per Key Conventions: the project uses Axum for HTTP. Use Axum's response header mechanisms to add custom headers.
- Per Key Conventions: all handlers return `Result<T, AppError>`. The instrumentation must not change the error handling behavior — timing should wrap the existing logic, not alter control flow.
- The `tower-http` caching middleware (noted in Key Conventions) may affect observed latency for repeated queries. The instrumentation should measure the actual database query time, not the cached response time, to give accurate performance data.

## Reuse Candidates
- `common/src/db/query.rs` — the query builder helpers are the code being timed; understanding their structure helps place instrumentation correctly
- `modules/search/src/service/mod.rs::SearchService` — the existing service implementation where timing instrumentation will be added

## Acceptance Criteria
- [ ] Search query execution time is logged with each search request
- [ ] Log entries include structured fields: query term, result count, duration in milliseconds, and active filters
- [ ] A `X-Query-Time-Ms` response header is returned with the search endpoint response
- [ ] Instrumentation does not alter the search response body or status codes
- [ ] Instrumentation does not introduce measurable overhead (< 1ms additional latency)

## Test Requirements
- [ ] Integration test in `tests/api/search.rs`: verify that the `X-Query-Time-Ms` header is present in search responses and contains a numeric value
- [ ] Integration test: verify that the header value is a reasonable positive number (> 0)
- [ ] Manual verification: confirm search query logs appear in application log output with the expected structured fields

## Dependencies
- Depends on: Task 2 — Enhance search relevance ranking (instrumentation should measure the final search implementation, not an intermediate state)
