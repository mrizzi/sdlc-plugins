# Criterion 3: Duplicate entries that were previously distinct due to different qualifiers are deduplicated in the response

## Verdict: PASS (with correctness caveat)

## Reasoning

The PR adds `.dedup_by(|a, b| a.purl == b.purl)` to the iterator chain in `modules/fundamental/src/purl/service/mod.rs`, which removes consecutive duplicate entries based on the PURL string value after qualifier stripping.

The test `test_recommend_purls_dedup` in `tests/api/purl_recommend.rs` directly verifies this:
- Seeds two PURLs with the same version but different qualifiers (`?repository_url=https://repo1.maven.org&type=jar` and `?repository_url=https://repo2.maven.org&type=jar`)
- Asserts that only one entry is returned (`body.items.len() == 1`)
- Verifies the entry is the simplified PURL without qualifiers

This confirms the deduplication behavior is implemented and tested.

**Correctness caveat:** The `dedup_by` method only removes **consecutive** duplicates. If the database returns rows in a non-adjacent order for entries that would produce the same simplified PURL, deduplication would miss them. The query lacks an explicit `ORDER BY` clause, so adjacent ordering of same-version PURLs relies on database behavior (typically insertion order or primary key order, which is usually adequate for this pattern but not guaranteed). This is a fragility concern rather than a functional failure -- in practice, PURLs with the same namespace/name/version but different qualifiers will typically have adjacent IDs. However, a `HashSet`-based dedup or SQL-level `DISTINCT` would be more robust.

Additionally, the `total` count is computed before deduplication (from the raw query), so `total` may overstate the actual number of unique results. The `test_recommend_purls_dedup` test does not assert on `body.total`, so this inconsistency is untested.

## Evidence

- `modules/fundamental/src/purl/service/mod.rs`: `.dedup_by(|a, b| a.purl == b.purl)` in the iterator chain
- `tests/api/purl_recommend.rs`: `test_recommend_purls_dedup` asserts `body.items.len() == 1` when two qualifier-distinct PURLs with the same version are seeded
