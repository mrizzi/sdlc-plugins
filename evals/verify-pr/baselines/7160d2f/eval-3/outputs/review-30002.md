# Review Comment Classification: 30002

## Comment
**Author:** reviewer-a
**File:** migration/src/m0042_sbom_soft_delete/mod.rs (line 14)
**Text:** The migration should also add an index on `deleted_at` for the sbom table. Queries filtering by `deleted_at IS NULL` will be frequent and a partial index would help. Something like:

```sql
CREATE INDEX idx_sbom_not_deleted ON sbom (deleted_at) WHERE deleted_at IS NULL;
```

## Classification: suggestion

## Reasoning
The reviewer proposes adding a partial index as a performance optimization. While the language uses "should," the feedback is a performance suggestion rather than a correctness requirement -- the code functions correctly without the index. The reviewer provides reasoning ("queries filtering by `deleted_at IS NULL` will be frequent") and a concrete SQL example, but this is an optimization proposal, not a fix for broken behavior. No CONVENTIONS.md exists in the target repository, and there is no demonstrated codebase pattern of consistent index creation in migration files that would warrant upgrading this to a code change request. The suggestion remains classified as a suggestion -- no sub-task is created.
