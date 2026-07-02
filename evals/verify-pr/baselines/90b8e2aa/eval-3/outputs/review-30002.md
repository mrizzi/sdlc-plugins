# Review Comment Classification: 30002

## Comment

> The migration should also add an index on `deleted_at` for the sbom table. Queries filtering by `deleted_at IS NULL` will be frequent and a partial index would help. Something like:
>
> ```sql
> CREATE INDEX idx_sbom_not_deleted ON sbom (deleted_at) WHERE deleted_at IS NULL;
> ```

**Author:** reviewer-a
**File:** `migration/src/m0042_sbom_soft_delete/mod.rs`, line 14
**Review ID:** 20001

## Initial Classification: suggestion

The reviewer uses the phrases "should also add" and "would help", which is suggestive language rather than imperative. The reviewer proposes a performance improvement (adding a partial index) and provides a code example, but the phrasing frames it as a recommendation rather than a mandatory requirement. The word "also" implies this is an additional idea beyond what is strictly required. "Would help" is conditional and advisory, not directive. Under the standard classification rules, this is a **suggestion**.

## Convention Upgrade Eligibility Assessment

Convention upgrade was evaluated to determine whether this suggestion should be promoted to a code change request.

### CONVENTIONS.md Check

The repository structure shows a `CONVENTIONS.md` file at the root of `trustify-backend/`. However, the contents of this file are not available for inspection. Without being able to verify that CONVENTIONS.md documents a specific convention requiring indexes on frequently-filtered columns in migrations, there is no confirmed documented convention to cite.

### Codebase Pattern Check

The repository contains migration files under `migration/src/`. While adding indexes for columns used in WHERE clauses is a common database best practice, no established codebase pattern was verified in the existing migrations (only `m0001_initial/` is visible in the repository structure). A single initial migration is insufficient evidence of an established project-specific convention for index creation.

### Upgrade Decision

The suggestion is **not upgraded** because:
1. No documented convention in CONVENTIONS.md was confirmed to require index creation for filtered columns in migrations
2. The existing migration history (only `m0001_initial/` visible) does not provide sufficient evidence of an established codebase pattern for index creation alongside column additions
3. While the suggestion is technically sound (the `list` endpoint filters by `deleted_at IS NULL`), a sound suggestion without convention backing remains a suggestion per the classification rules

The reviewer's recommendation is valid from a performance perspective, but without a documented convention or established codebase pattern to cite, it does not qualify for convention upgrade.

## Final Classification: suggestion

## Action

No sub-task created. Suggestions without convention backing are informational feedback that do not require tracked work. The PR author may choose to implement this improvement at their discretion.
