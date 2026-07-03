# Criterion 3: Duplicate entries that were previously distinct due to different qualifiers are deduplicated in the response

## Verdict: PASS

## Reasoning

The PR adds deduplication logic in `modules/fundamental/src/purl/service/mod.rs` via the `.dedup_by()` call on the iterator chain:

```rust
.dedup_by(|a, b| a.purl == b.purl)
```

This removes consecutive duplicate entries based on the PURL string value. Since qualifiers have been stripped at this point (via `without_qualifiers()`), PURLs that were previously distinct only because of different qualifiers (e.g., same package version from different repositories) will now have identical string representations and will be collapsed to a single entry.

Additionally, the query has been modified to include `group_by(purl::Column::Id)` in the count query, which handles deduplication at the database level for the total count:

```rust
let total = query.clone()
    .select_only()
    .column(purl::Column::Id)
    .group_by(purl::Column::Id)
    .count(&self.db).await?;
```

The test `test_recommend_purls_dedup` in `tests/api/purl_recommend.rs` directly verifies this behavior:
- Seeds two PURLs for the same package version with different qualifiers: `commons-lang3@3.12?repository_url=https://repo1.maven.org&type=jar` and `commons-lang3@3.12?repository_url=https://repo2.maven.org&type=jar`
- Asserts only one entry is returned: `assert_eq!(body.items.len(), 1);`
- Asserts the returned PURL is the simplified version: `assert_eq!(body.items[0].purl, "pkg:maven/org.apache/commons-lang3@3.12");`

This confirms that entries previously distinct due to different qualifiers are now properly deduplicated.
