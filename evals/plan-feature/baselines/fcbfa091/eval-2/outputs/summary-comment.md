# Plan Summary: TC-9002 -- Improve Search Experience

## Overview

Planned **3 implementation tasks** for feature TC-9002 targeting the **trustify-backend** repository. The feature requests improvements to search performance, result relevance, and filtering capabilities.

## Inherited Fields

- **Priority:** Normal (inherited from TC-9002)
- **Fix Versions:** RHTPA 1.6.0 (inherited from TC-9002)
- **Labels:** ai-generated-jira (propagated to all tasks)

All three fields have been propagated to every task's `additional_fields`.

## Task Summary

| # | Task | Key Changes | Dependencies |
|---|---|---|---|
| 1 | Search performance indexes | New migration with GIN indexes; optimize SearchService queries | None |
| 2 | Search relevance ranking | ts_rank scoring; sort query parameter on search endpoint | Task 1 |
| 3 | Search filters | Type, date range, severity filter parameters on search endpoint | Task 1 |

## Scope Decisions

- **Better UI (non-MVP):** Excluded. Cannot be planned without design mockups or a frontend repository. The trustify-backend repository contains only the REST API; UI changes require a frontend feature specification.
- **Documentation task:** Not generated. The feature description contains no "Documentation Considerations" section.
- **Testing tasks:** Not generated. No testing readiness template was provided.

## Ambiguities Flagged

The feature description is intentionally vague in several areas. The following ambiguities were identified and documented in the impact map and individual task descriptions:

1. **No quantitative performance targets** -- "faster" and "fast enough" are not measurable. Assumed: index scans over sequential scans as the performance criterion.
2. **Undefined relevance criteria** -- "more relevant" has no definition. Assumed: PostgreSQL ts_rank text-match scoring.
3. **Unspecified filter set** -- "some kind of filtering" names no attributes. Assumed: entity type, date range, and severity filters based on the existing data model.
4. **No regression test criteria** -- "don't break existing functionality" is unverifiable without a baseline. Assumed: existing `tests/api/search.rs` integration tests as regression baseline.
5. **No search scope definition** -- unclear which entities and fields are in scope. Assumed: current SearchService scope (SBOM, advisory, package entities).

All assumptions are labeled as "pending clarification" in the task descriptions and impact map.

## Convention Enrichment

Conventions from the repository were applied per the convention-applicability-rules:
- Module pattern (model/ + service/ + endpoints/) -- applied to all tasks modifying `modules/search/`
- Error handling (`Result<T, AppError>` with `.context()`) -- applied to all tasks
- Response types (`PaginatedResults<T>`) -- applied to Tasks 2 and 3
- Query helpers (`common/src/db/query.rs`) -- applied to all tasks
- Testing patterns (integration tests in `tests/api/`) -- applied to test requirements in all tasks

## Dependency Graph

```
Task 1 (indexes) --> Task 2 (relevance)
Task 1 (indexes) --> Task 3 (filters)
```

Tasks 2 and 3 are independent of each other and can be executed in parallel after Task 1 completes.
