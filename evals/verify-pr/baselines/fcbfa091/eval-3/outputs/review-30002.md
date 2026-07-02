# Review Comment Classification: Comment 30002

## Comment

**Author:** reviewer-a
**File:** migration/src/m0042_sbom_soft_delete/mod.rs (line 14)
**Text:** "The migration should also add an index on `deleted_at` for the sbom table. Queries filtering by `deleted_at IS NULL` will be frequent and a partial index would help. Something like:\n\n```sql\nCREATE INDEX idx_sbom_not_deleted ON sbom (deleted_at) WHERE deleted_at IS NULL;\n```"

## Classification: SUGGESTION

## Reasoning

The reviewer's language uses suggestive, additive phrasing rather than directive correction:

1. **"should also add"** -- the phrase "should also" is a characteristic suggestion marker. It proposes an additional enhancement on top of the current implementation rather than correcting something that is wrong. Compare with comment 30001's "should run" which corrects existing behavior; here "should also" adds new behavior.

2. **"would help"** -- hedging language indicating the reviewer sees this as beneficial but not strictly required. A code change request would use stronger language like "is required", "must", or "needs to".

3. **"Something like:"** -- this phrase explicitly frames the SQL as an example or starting point, not a precise requirement. The reviewer is illustrating the concept rather than prescribing an exact fix.

4. **Performance optimization, not correctness** -- unlike comment 30001 which identifies a correctness bug (inconsistent state), this comment proposes a performance optimization. The code functions correctly without the index; the index improves query performance. This is an enhancement suggestion, not a fix for broken behavior.

### Convention Upgrade Evaluation

Per the Style/Conventions sub-agent's Convention Upgrade check, this suggestion was evaluated for potential upgrade to a code change request:

1. **CONVENTIONS.md check:** The repository's CONVENTIONS.md content was not available for analysis. The Key Conventions listed in the repo structure document do not mention index creation patterns, migration conventions for indexes, or performance-related database conventions.

2. **Codebase pattern check:** The PR diff does not contain evidence of established index creation patterns in migration files. Only one migration file exists in the diff (m0042_sbom_soft_delete/mod.rs) and it does not demonstrate index creation patterns that could serve as a codebase convention.

3. **Performance-related scrutiny:** Applied extra scrutiny per the convention upgrade rules for performance-related suggestions (indexes). No documented performance conventions or retroactive index migration patterns found.

**Upgrade decision: No upgrade.** The suggestion does not match any documented convention in CONVENTIONS.md and no established codebase pattern supports elevation. General database best practices ("indexes improve query performance") are explicitly excluded as upgrade evidence per the Style/Conventions sub-agent rules.

## Action

No sub-task created. The suggestion remains classified as a suggestion -- an optional performance improvement that the PR author may choose to address.
