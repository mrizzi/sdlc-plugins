# Repository Impact Map — TC-9002: Improve search experience

## Ambiguities Identified

The feature description TC-9002 contains significant ambiguities that must be resolved before implementation can proceed with full confidence. The following ambiguities are flagged for clarification with the product owner:

### Ambiguity 1: "Search should be faster" — No performance targets defined
The requirement states search is "currently too slow" and should be "fast enough," but provides no measurable targets. There are no latency benchmarks (e.g., p95 < 200ms), no baseline measurements of current performance, and no definition of what "fast enough" means.

**Assumption (pending clarification):** We assume the goal is to add database indexing on commonly searched fields and optimize the existing query patterns in `modules/search/src/service/mod.rs`. We target a meaningful improvement (e.g., sub-500ms for typical queries) but cannot validate against a specific SLA without defined targets.

### Ambiguity 2: "Results should be more relevant" — No relevance criteria defined
The requirement says users complain about "irrelevant results" but does not define what relevance means. There is no ranking algorithm specified, no indication of which entity types (SBOMs, advisories, packages) should be prioritized, and no user research data on what "relevant" means in context.

**Assumption (pending clarification):** We assume relevance can be improved by implementing weighted full-text search scoring (e.g., exact matches ranked higher than partial matches, title matches ranked higher than description matches) and by searching across all three entity types (SBOMs, advisories, packages) with type-aware ranking.

### Ambiguity 3: "Add filters" — No filter specifications
The requirement says "some kind of filtering capability" but does not specify which fields should be filterable, what filter types are needed (dropdown, date range, text, multi-select), or how filters interact with full-text search.

**Assumption (pending clarification):** Based on the existing entity models in the repository, we assume the following filters are reasonable for an MVP:
- Entity type filter (SBOM, Advisory, Package)
- Severity filter (for advisories, based on the `severity` field in `AdvisorySummary`)
- Date range filter (for creation/modification dates)

### Ambiguity 4: "Better UI" — Non-MVP, no design mockups, no frontend repository
The "Better UI" requirement is marked as non-MVP. Additionally, there are no Figma mockups linked to this feature, no frontend repository is listed in the Repository Registry, and the only target repository is `trustify-backend` (a Rust backend service). **This requirement is excluded from scope entirely** — it cannot be planned without design mockups and a frontend repository.

### Ambiguity 5: Non-functional requirements are vague
"Should be fast enough" and "Don't break existing functionality" are not measurable criteria. There are no specific NFRs for memory usage, concurrent query limits, or degradation tolerance.

**Assumption (pending clarification):** We assume standard engineering practices apply — no regressions in existing test suite, search queries should not degrade database performance for other operations, and the existing connection pool limiter in `common/src/db/limiter.rs` should be respected.

---

## Impact Map

```
trustify-backend:
  changes:
    - Add database indexes on commonly searched text fields to improve query performance
    - Add a database migration for full-text search indexes (tsvector columns and GIN indexes)
    - Extend SearchService to support weighted full-text search ranking across SBOMs, advisories, and packages
    - Add filter parameters (entity type, severity, date range) to the search endpoint
    - Update the search endpoint to accept filter query parameters and pass them to the service layer
    - Add integration tests for search performance improvements, relevance ranking, and filtering
```

---

## Workflow Mode Decision

**Selected mode:** `direct-to-main`

**Rationale:** No atomicity indicators are present:
1. No coordinated schema migrations — the search index migration is self-contained and does not break existing functionality (additive only).
2. No breaking API changes — the search endpoint changes are backward-compatible (new optional query parameters).
3. No cross-cutting refactors — changes are confined to the search module and a new migration.
4. No tightly coupled cross-repo components — only the backend repository is affected, and there is no frontend repository in scope.

Each task can be merged independently to `main` without leaving the codebase in a broken state.
