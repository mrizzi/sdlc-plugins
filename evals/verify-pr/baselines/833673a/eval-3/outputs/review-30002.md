## Review Comment Classification: 30002

**Comment ID:** 30002
**Author:** reviewer-a
**File:** migration/src/m0042_sbom_soft_delete/mod.rs, line 14
**Classification:** suggestion

### Comment Text

> The migration should also add an index on `deleted_at` for the sbom table. Queries filtering by `deleted_at IS NULL` will be frequent and a partial index would help. Something like:
>
> ```sql
> CREATE INDEX idx_sbom_not_deleted ON sbom (deleted_at) WHERE deleted_at IS NULL;
> ```

### Classification Reasoning

The reviewer proposes adding a partial index on `deleted_at` as a performance optimization. While this is reasonable advice for a soft-delete pattern, the language is suggestive rather than imperative -- "should also add" and "would help" indicate a recommendation rather than a required fix.

**Convention upgrade evaluation:**
- No CONVENTIONS.md is available in the repository to document an indexing convention for migrations.
- The PR diff contains only one migration file, so no codebase pattern of adding indexes to migration files can be demonstrated from the available context.
- Without documented conventions or countable codebase patterns, this suggestion cannot be upgraded to a code change request per the convention upgrade rules.
- General database best practices (indexes on frequently filtered columns) are not sufficient grounds for an upgrade -- the evidence must cite a concrete CONVENTIONS.md section or a counted codebase pattern.

### Action

No sub-task created. The suggestion remains optional -- the reviewer may choose to follow up if they feel strongly about the index.
