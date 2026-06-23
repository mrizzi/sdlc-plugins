# Criterion 3: The count reflects unique advisories only (no duplicates from multiple SBOMs)

## Verdict: FAIL

## Analysis

No deduplication logic exists because no subquery or join is implemented at all. The vulnerability count is hardcoded to 0 for every package in `modules/fundamental/src/package/service/mod.rs`:

```rust
vulnerability_count: 0, // TODO: implement subquery
```

The task requires a correlated subquery that joins through `sbom_package -> sbom_advisory -> advisory` tables using `COUNT(DISTINCT a.id)` to deduplicate advisories that appear across multiple SBOMs. None of this logic is present.

The test `test_vulnerability_count_deduplicates_across_sboms` specifically tests deduplication by seeding a package with 2 unique advisories shared across 3 SBOMs, then asserting `vulnerability_count == 2`. With the hardcoded value of 0, this test would fail, confirming the deduplication logic is entirely absent.

Without any query to count advisories, the concept of deduplication is moot. This criterion fails because the foundational counting mechanism is not implemented.
