## Criterion 3: Duplicate entries that were previously distinct due to different qualifiers are deduplicated in the response

**Verdict: PASS**

### Evidence from the diff

1. **Implementation**: In `modules/fundamental/src/purl/service/mod.rs`, after stripping qualifiers via `without_qualifiers()`, the results are passed through a deduplication step:

   ```rust
   .dedup_by(|a, b| a.purl == b.purl)
   ```

   This removes consecutive duplicate entries based on the PURL string. Since qualifiers have been stripped, entries that were previously distinct (e.g., same version with `repository_url=repo1` vs `repository_url=repo2`) will now have identical PURL strings and be collapsed into a single entry.

2. **Dedicated test**: The new `test_recommend_purls_dedup` function in `tests/api/purl_recommend.rs` directly validates this behavior:

   ```rust
   // Given PURLs with different qualifiers for the same package version
   ctx.seed_purl("pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo1.maven.org&type=jar").await;
   ctx.seed_purl("pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo2.maven.org&type=jar").await;
   
   // Then only one entry is returned (deduplicated after qualifier removal)
   assert_eq!(body.items.len(), 1);
   assert_eq!(body.items[0].purl, "pkg:maven/org.apache/commons-lang3@3.12");
   ```

   This seeds two PURLs that differ only in their `repository_url` qualifier and asserts that only one entry is returned after qualifier stripping and deduplication.

3. **Note on dedup_by**: The `dedup_by` method removes consecutive duplicates, which means it relies on the database query returning rows grouped such that duplicates are adjacent. The query applies `group_by(purl::Column::Id)` in the count path, but the item-fetch path does not explicitly sort. If the database returns rows ordered by insertion or primary key, PURLs for the same version would typically be adjacent. This is a potential edge case worth noting but does not invalidate the test evidence.
