# Repository Impact Map — TC-9002: Improve Search Experience

## Workflow Mode: `direct-to-main`

**Rationale:** No atomicity indicators were identified. The search improvements (performance optimization, relevance tuning, and filter support) can each be delivered independently to `main` without leaving the codebase in a broken state. Each task enhances an existing, working search module — no coordinated schema migrations, no breaking API changes, and no cross-cutting refactors that require all-or-nothing delivery.

---

```
trustify-backend:
  changes:
    - Add database indexes and optimize search query execution in the search module to reduce query latency
    - Implement full-text search ranking and relevance scoring in SearchService for more meaningful result ordering
    - Add filter parameters (entity type, severity, date range, license) to the search endpoint and integrate with the shared query builder
    - Add integration tests for search performance, relevance ranking, and filtering behavior
```
