# Review Comment Classification: 30002

**Comment ID:** 30002
**Author:** reviewer-a
**File:** migration/src/m0042_sbom_soft_delete/mod.rs
**Line:** 14
**Classification:** suggestion

## Reasoning

The reviewer uses suggestive language throughout the comment:

- "The migration **should also** add an index" -- the phrase "should also" proposes an addition beyond what was specified, rather than directing a fix to existing code. It suggests an enhancement that would improve performance.
- "Queries filtering by `deleted_at IS NULL` **will be** frequent and a partial index **would help**" -- "would help" is conditional/suggestive, indicating a performance improvement rather than a required correction.
- "Something like:" followed by a SQL example -- the phrase "something like" presents the code as one possible approach, not as a directive.

The reviewer is proposing an optimization (adding a partial index for query performance) that goes beyond the task's requirements. The task description does not mention indexing, and the reviewer frames this as an enhancement rather than a bug fix or required change.

## Convention Upgrade Eligibility

For a suggestion to be upgraded to a code change request, it must match a documented project convention (CONVENTIONS.md) or a demonstrated codebase pattern.

- **CONVENTIONS.md check:** No CONVENTIONS.md content is available in the eval fixtures. The repository structure shows a CONVENTIONS.md file exists at the repo root, but its content was not provided as input. Without access to the actual conventions document, it is impossible to determine whether index creation for soft-delete columns is a documented convention.

- **Codebase pattern check:** The PR diff and fixture data do not include other migration files to compare against. There is no evidence of a consistent pattern of index creation in migrations within the available data.

**Conclusion:** The suggestion does NOT qualify for convention upgrade because:
1. No CONVENTIONS.md content is available to check for a documented convention.
2. No codebase pattern data is available to demonstrate consistent usage.
3. General industry best practices (e.g., "indexes are a database best practice") are explicitly insufficient for upgrade per the Style/Conventions sub-agent rules.

**Action:** No sub-task created. The suggestion remains classified as a suggestion.
