# Repository Impact Map

## trustify-backend

### Changes
- Create reversible database migration: define `advisory_status_enum` PostgreSQL enum type with values (New, Analyzing, Fixed, Rejected), add `status` enum column to `advisory` table, backfill from `status_id` foreign key join, drop `status_id` FK column, drop `advisory_status` lookup table
- Update SeaORM entity definitions: define `AdvisoryStatusEnum` Rust enum with `DeriveActiveEnum`, update `advisory` entity to use `status` enum field, remove `advisory_status` entity and module declaration
- Update advisory service layer and endpoints: remove `advisory_status` join from all advisory queries in `AdvisoryService`, update `AdvisorySummary` and `AdvisoryDetails` models to source status from enum field, update list and get endpoint handlers to filter by enum values directly
- Update advisory ingestion pipeline: replace lookup table insert and FK reference with direct `advisory_status_enum` value assignment during advisory ingestion
- Update integration tests: modify test data seeding and assertions in advisory endpoint tests for enum-based status column
- Update internal architecture documentation to reflect schema change from lookup table to enum column

### Workflow Mode Decision

**Selected mode:** `feature-branch`

**Rationale:** Multiple atomicity indicators are present:

1. **Coordinated schema migration** -- The migration adds the `status` enum column and drops the `status_id` FK column and `advisory_status` table. The code changes in the service layer, ingestion pipeline, and entity definitions depend on the enum column existing and the lookup table being absent. Merging the migration without the code changes would break all advisory queries (they still join the now-dropped `advisory_status` table). Merging the code changes without the migration would reference a `status` column that does not exist.

2. **Tightly coupled feature components** -- The entity definition update (`AdvisoryStatusEnum`), service layer update (query changes), and ingestion pipeline update (enum value writes) are interdependent: the entity defines the enum type that both the service and ingestion code consume. Partial delivery would fail compilation.

**Interdependent tasks:**
- Task 2 (migration) + Task 3 (entities) + Task 4 (service/endpoints) + Task 5 (ingestion) -- these four tasks form a tight dependency chain where none can function independently on `main`.

The `workflow:feature-branch` label will be applied to the feature issue TC-9005.

### Excluded Requirements
None -- all requirements from the feature description can be decomposed into actionable tasks within the trustify-backend repository.

### Additional Fields for Task Creation

All created tasks include the following `additional_fields`:

```json
{
  "labels": ["ai-generated-jira"],
  "priority": {"name": "High"},
  "fixVersions": [{"name": "RHTPA 2.0.0"}]
}
```

- **Priority**: inherited from Feature TC-9005 (High)
- **Fix Versions**: inherited from Feature TC-9005 (RHTPA 2.0.0); `fixVersion scope` not configured in CLAUDE.md Jira Field Defaults, defaulting to `"both"` (propagate to tasks)
- **Labels**: `ai-generated-jira` applied to all tasks; `workflow:feature-branch` applied to the Feature issue TC-9005
