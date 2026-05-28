# Review Comment Classification: 30002

## Comment

> The migration should also add an index on `deleted_at` for the sbom table. Queries filtering by `deleted_at IS NULL` will be frequent and a partial index would help. Something like:
>
> ```sql
> CREATE INDEX idx_sbom_not_deleted ON sbom (deleted_at) WHERE deleted_at IS NULL;
> ```

**Author:** reviewer-a
**File:** migration/src/m0042_sbom_soft_delete/mod.rs
**Line:** 14

## Classification: code change request

## Reasoning

The reviewer states "The migration should also add an index" -- this is directive language requesting a concrete code change. The reviewer provides a specific SQL snippet showing exactly what index to add and explains the performance rationale (frequent `deleted_at IS NULL` queries).

While the phrase "Something like" could be interpreted as softening the request to a suggestion, the overall tone is directive and the core ask ("should also add an index") is a clear requirement.

Additionally, this comment is eligible for convention upgrade evaluation. Adding indexes for frequently-queried columns in migrations is a common database convention. The repository's migration structure (migration/src/) and the use of SeaORM suggest established patterns for migration authoring. If the project's CONVENTIONS.md or codebase patterns demonstrate consistent index creation in migrations, this would be upgraded from suggestion to code change request. However, given the directive language ("should"), it is already classified as a code change request without needing the upgrade path.

## Action

Create sub-task to address this feedback.
