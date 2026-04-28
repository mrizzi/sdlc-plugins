# Task 4 — Add Query Performance Logging to SearchService

## Repository
trustify-backend

## Description
Add structured performance logging to the `SearchService` to measure search query latency and enable ongoing performance monitoring. The feature's non-functional requirement "should be fast enough" is unquantified, so instrumentation is needed to establish a baseline, validate that the full-text search improvements (Tasks 1-2) achieve acceptable latency, and detect regressions. This logging provides the measurement data that the team needs to define and enforce concrete latency targets.

## Files to Modify
- `modules/search/src/service/mod.rs` — add timing instrumentation around search query execution; log query duration, result count, and filter parameters at INFO level for successful queries and WARN level for slow queries (above a configurable threshold)

## Implementation Notes
- Inspect the current `SearchService` implementation in `modules/search/src/service/mod.rs` to identify the query execution call sites that need instrumentation
- Use `std::time::Instant` to measure query duration: capture `Instant::now()` before the query and `.elapsed()` after
- Use the `tracing` crate for structured logging (consistent with Axum ecosystem):
  - `tracing::info!(duration_ms = elapsed.as_millis(), result_count = count, query = %search_term, "search query completed")`
  - `tracing::warn!(duration_ms = elapsed.as_millis(), query = %search_term, "slow search query")` for queries exceeding a threshold (default 500ms)
- Define the slow-query threshold as a constant that can be overridden via environment variable (e.g., `SEARCH_SLOW_QUERY_THRESHOLD_MS`)
- Follow the existing error handling pattern with `Result<T, AppError>` and `.context()` wrapping
- Per constraints doc section 2: commit must reference TC-9002 in footer, use Conventional Commits format
- Per constraints doc section 5: keep changes scoped to the search service module

## Reuse Candidates
- `common/src/error.rs` — `AppError` for error handling consistency
- `modules/search/src/service/mod.rs` — existing SearchService structure to extend with logging

## Acceptance Criteria
- [ ] Every search query logs its execution duration in milliseconds
- [ ] Successful queries log at INFO level with duration, result count, and query term
- [ ] Queries exceeding the slow-query threshold log at WARN level
- [ ] The slow-query threshold is configurable via environment variable
- [ ] Logging does not materially affect search query latency (no blocking I/O in the logging path)

## Test Requirements
- [ ] Unit test: verify that search queries complete successfully with logging enabled (no panics or errors from instrumentation)
- [ ] Integration test: verify search endpoint returns correct results with performance logging active (logging must not alter response content)

## Verification Commands
- `cargo test -p search` — search module tests pass
- `RUST_LOG=search=info cargo test --test search` — run search integration tests with logging visible to confirm log output format
