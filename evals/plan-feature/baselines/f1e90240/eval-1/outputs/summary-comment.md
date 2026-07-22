# Planning Summary: TC-9001 -- Add advisory severity aggregation endpoint

## Task Breakdown

8 tasks were created for feature TC-9001:

- **5 implementation tasks** (Tasks 1-5): model, service, endpoint, cache invalidation, integration tests
- **1 documentation task** (Task 6): REST API reference update
- **2 testing tasks** (Tasks 7-8): smoke tests, performance benchmarks

## Inherited Field Propagation

### Priority

- **Feature value**: Major
- **Action**: Propagated to all 8 tasks
- **Rationale**: Priority is "Major" (not "Undefined"), so it is inherited by all child tasks per the field inheritance rules.

### Fix Versions

- **Feature value**: RHTPA 1.5.0
- **Action**: Propagated to all 8 tasks
- **Rationale**: Fix Versions is non-empty ("RHTPA 1.5.0") and there is no `fixVersion` scope override in the project configuration, so the default scope of "both" applies -- the fix version is propagated to all tasks (both implementation and non-implementation).

## Dependency Structure

All task dependencies form a valid DAG (directed acyclic graph) with no circular dependencies:

- Task 1 has no dependencies (root)
- Task 2 depends on Task 1
- Task 3 depends on Task 2
- Task 4 depends on Task 3
- Task 5 depends on Tasks 3 and 4
- Task 6 (documentation) depends on Task 3
- Task 7 (smoke tests) depends on Tasks 1, 2, 3, 4, 5
- Task 8 (performance benchmarks) depends on Tasks 1, 2, 3, 4, 5

Testing tasks (7, 8) depend on all implementation tasks but not on the documentation task or on each other.

## Convention Enrichment

Conventions from the repository's Key Conventions section were applied to tasks based on file-type scope matching:

- **Module pattern** (`model/ + service/ + endpoints/`): Applied to Tasks 1, 2, 3 (create/modify files within these directories)
- **Error handling** (`Result<T, AppError>` with `.context()`): Applied to Tasks 2, 3 (service and endpoint code)
- **Endpoint registration** (routes in `endpoints/mod.rs`): Applied to Task 3
- **Caching** (`tower-http` middleware): Applied to Tasks 3, 4
- **Testing** (integration tests in `tests/api/`): Applied to Task 5
- **Query helpers** (filtering/pagination via `common/src/db/query.rs`): Applied to Task 2

Conventions for response types (`PaginatedResults<T>`) were not applied because the advisory-summary endpoint returns a single aggregated object, not a paginated list.
