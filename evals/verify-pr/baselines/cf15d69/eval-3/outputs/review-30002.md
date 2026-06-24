# Review Comment Classification: 30002

## Comment

**Author:** reviewer-a
**File:** `migration/src/m0042_sbom_soft_delete/mod.rs`, line 14
**Body:** "The migration should also add an index on `deleted_at` for the sbom table. Queries filtering by `deleted_at IS NULL` will be frequent and a partial index would help. Something like:
```sql
CREATE INDEX idx_sbom_not_deleted ON sbom (deleted_at) WHERE deleted_at IS NULL;
```"

## Classification: Suggestion

## Reasoning

The reviewer's language uses suggestive, advisory phrasing rather than imperative directives. Key indicators:

1. **"should also"** -- the word "also" signals this is an addition beyond the core requirements, not a correction of an existing defect. "Should also" is a weaker directive than "must" or "needs to".
2. **"would help"** -- this is conditional/advisory language indicating a performance optimization that would be beneficial, not a requirement. It frames the index as helpful rather than mandatory.
3. **"Something like:"** -- this phrase explicitly frames the provided SQL as an illustrative example of a possible approach, not a prescribed fix.

The comment proposes a performance optimization (adding a partial index) rather than identifying a correctness defect. The code functions correctly without the index -- queries will return correct results, just potentially slower at scale.

### Convention Upgrade Eligibility Assessment

To determine whether this suggestion should be upgraded to a code change request, the following checks apply:

1. **CONVENTIONS.md check:** The repository has a CONVENTIONS.md file (noted in repo-backend.md). However, the repository structure document does not include the CONVENTIONS.md contents, so no documented convention about index creation for migration files can be confirmed. Without access to the actual CONVENTIONS.md content, there is no documented convention to cite as backing evidence for an upgrade.

2. **Codebase pattern check:** The PR diff contains only one migration file (`m0042_sbom_soft_delete/mod.rs`), and the repository structure shows only one other migration (`m0001_initial/`). There is insufficient evidence in the available data to establish a consistent codebase pattern of adding indexes in migration files. A counted pattern match (e.g., "17 migrations use Index::create for FK columns") cannot be substantiated from the available inputs.

3. **Performance-related scrutiny:** While indexes are a database best practice, the upgrade decision requires project-specific evidence (a documented convention or a demonstrated codebase pattern), not general industry knowledge. "Indexes are a database best practice" is general knowledge and does not qualify as project-specific convention evidence per the upgrade rules.

**Conclusion:** No upgrade. The suggestion remains classified as **suggestion** because (a) no CONVENTIONS.md convention could be confirmed to back it, (b) no counted codebase pattern of index creation in migrations is available from the inputs, and (c) general database best practices do not qualify as project-specific convention evidence.

## Action

No sub-task created.
