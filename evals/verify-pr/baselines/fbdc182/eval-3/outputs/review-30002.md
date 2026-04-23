# Review Comment Classification: 30002

**Comment ID:** 30002
**Author:** reviewer-a
**File:** `migration/src/m0042_sbom_soft_delete/mod.rs` (line 14)
**Classification:** suggestion

## Comment Text

> The migration should also add an index on `deleted_at` for the sbom table. Queries filtering by `deleted_at IS NULL` will be frequent and a partial index would help. Something like:
>
> ```sql
> CREATE INDEX idx_sbom_not_deleted ON sbom (deleted_at) WHERE deleted_at IS NULL;
> ```

## Reasoning

The reviewer proposes adding a partial index on the `deleted_at` column for performance optimization. While the reviewer uses the word "should," the comment proposes an additional enhancement (an index) that was not part of the original task requirements or acceptance criteria. The reviewer frames this as a performance optimization ("would help") rather than identifying a correctness defect.

**Convention check (suggestion upgrade evaluation):** The repository has a CONVENTIONS.md file at its root, but its contents are not available for inspection in this context. The repository structure does not provide evidence of an established convention for adding indexes in migration files. Without documented convention evidence from CONVENTIONS.md or demonstrated codebase patterns (e.g., multiple migrations that consistently add indexes for filter columns), this suggestion cannot be upgraded to a code change request.

**Performance-related scrutiny:** This is a performance-related suggestion (index creation) and received extra scrutiny per the skill definition. However, without access to CONVENTIONS.md contents or the ability to search for `Index::create` patterns in existing migration files, there is insufficient evidence to confirm this is an established project convention.

The classification remains **suggestion**. No sub-task created.

## Action

No sub-task created -- this is a suggestion without confirmed convention backing.
