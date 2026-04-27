# Repository Impact Map — TC-9002: Improve search experience

## Identified Ambiguities

The following requirements are vague or incomplete and require clarification before implementation:

1. **"Search should be faster"** — no performance baseline or target latency defined. What is the current p95 latency? What is the target? **Assumption pending clarification**: targeting p95 < 500ms for keyword searches, based on industry standards.

2. **"Results should be more relevant"** — no relevance criteria, ranking algorithm, or examples of bad results provided. What constitutes "relevant"? **Assumption pending clarification**: implementing weighted full-text search ranking (title > description > content).

3. **"Add filters"** — no filter dimensions, types, or combination logic specified. Filter by what fields? How do multiple filters combine? **Assumption pending clarification**: adding filters for entity type, severity level, and date range as the most commonly useful dimensions, combining with AND logic.

4. **"Should be fast enough"** (NFR) — non-functional requirement with no quantifiable target. **Assumption pending clarification**: using the same p95 < 500ms target.

5. **"Don't break existing functionality"** (NFR) — backward compatibility scope undefined. Does this mean API response shape must be identical, or just that existing queries continue to work? **Assumption pending clarification**: additive-only API changes, no breaking changes to existing response shapes.

6. **"Better UI"** — this requirement is explicitly excluded from scope. No frontend repository is available in the repository registry, no Figma mockups or design specifications have been provided, and UI improvements cannot be planned without visual design direction. This requirement should be revisited when a frontend repository and design assets are available.

## trustify-backend

### Changes

- Add database indexes on commonly searched fields to improve search query performance in `modules/search/`
- Implement weighted full-text search relevance scoring in `modules/search/src/service/mod.rs` using PostgreSQL `ts_rank` with field weighting
- Add filter query parameters (entity_type, severity, date_from, date_to) to `GET /api/v2/search` endpoint in `modules/search/src/endpoints/mod.rs`
- Add integration tests for improved search behavior in `tests/api/search.rs`
