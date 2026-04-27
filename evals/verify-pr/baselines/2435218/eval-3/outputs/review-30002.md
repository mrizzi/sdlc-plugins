# Review Comment Classification: 30002

**Comment ID:** 30002
**Reviewer:** reviewer-a
**File:** migration/src/m0042_sbom_soft_delete/mod.rs
**Line:** 14
**Classification:** code change request

## Comment Text

> The migration should also add an index on `deleted_at` for the sbom table. Queries filtering by `deleted_at IS NULL` will be frequent and a partial index would help. Something like:
>
> ```sql
> CREATE INDEX idx_sbom_not_deleted ON sbom (deleted_at) WHERE deleted_at IS NULL;
> ```

## Classification Reasoning

This is a **code change request**. The reviewer uses directive language ("The migration should also add an index") requesting a concrete code modification to the migration file. While the suggestion relates to performance optimization, the reviewer frames it as a requirement ("should also add"), not as an optional consideration. The reviewer identifies that queries filtering by `deleted_at IS NULL` will be frequent (the list endpoint added in this PR always applies this filter by default), making the index a correctness concern for production query performance rather than a speculative optimization.

### Convention check

No Serena instance is available for the trustify-backend repository (per the Repository Registry in CLAUDE.md). The repository structure shows a `CONVENTIONS.md` file at the root, but it could not be inspected because the repository is not available locally. The migration directory shows only `m0001_initial` as a prior migration, providing insufficient evidence to determine whether index creation is an established codebase convention.

Despite the lack of convention evidence, the comment is classified as a code change request based on the directive language and the direct performance implication for the query pattern introduced in this PR.

## Action

Sub-task created to address this feedback. The fix requires adding a partial index on `deleted_at` to the migration.
