# Plan Summary — TC-9002: Improve search experience

## Tasks Created

| # | Summary | Repository |
|---|---|---|
| Task 1 | Add search filtering parameters to the search endpoint | trustify-backend |
| Task 2 | Improve search relevance scoring in SearchService | trustify-backend |
| Task 3 | Optimize search performance with database indexes | trustify-backend |

## Repositories Affected

- **trustify-backend** — search module (`modules/search/`), common query helpers (`common/src/db/query.rs`), entity definitions (`entity/src/`), migration (`migration/src/`), integration tests (`tests/api/search.rs`)

## Architecture Summary

The plan decomposes the "Improve search experience" feature into three independent backend tasks targeting the `trustify-backend` Rust service:

1. **Filtering** (Task 1) — Extends the search endpoint and SearchService to accept filter parameters (entity type, search qualifiers), enabling users to narrow search results. Builds on existing query builder helpers in `common/src/db/query.rs`.

2. **Relevance** (Task 2) — Implements full-text search ranking in the SearchService to score and order results by match quality. Adds a `sort` parameter to the search endpoint and includes relevance scores in the response.

3. **Performance** (Task 3) — Adds a database migration for GIN indexes on full-text search columns and optimizes SearchService query patterns to ensure index utilization.

Each task can be merged independently (direct-to-main workflow). No cross-task atomicity constraints were identified.

## Workflow Mode

**direct-to-main** — No atomicity indicators. Tasks are independent improvements that do not break `main` when merged individually.

## Inherited Field Values

- **Priority**: Normal — inherited from TC-9002 and propagated to all created tasks. The Feature's priority is set (not "Undefined"), so it is included in `additional_fields` on each task.
- **fixVersions**: RHTPA 1.6.0 — inherited from TC-9002 and propagated to all created tasks. The Feature has a non-empty fixVersions array, and the `fixVersion scope` defaults to "both" (no `### Jira Field Defaults` section found in CLAUDE.md), so fixVersions are propagated to tasks.

## Ambiguities Flagged

Five ambiguities were identified and documented in the impact map and individual task descriptions. Each task includes an "Ambiguity note" stating the assumption made and that it is pending clarification from the feature owner.

## Excluded Requirements

- **Better UI** — excluded from scope. No frontend repository is available and no design mockups were provided. This requirement cannot be decomposed into actionable tasks without a frontend repo and Figma designs.

## Additional Fields (Task Creation)

Each task is created with the following `additional_fields`:

```json
{
  "labels": ["ai-generated-jira"],
  "priority": {"name": "Normal"},
  "fixVersions": [{"name": "RHTPA 1.6.0"}]
}
```
