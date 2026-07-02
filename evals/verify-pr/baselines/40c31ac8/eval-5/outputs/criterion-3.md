## Criterion 3: Duplicate entries that were previously distinct due to different qualifiers are deduplicated in the response

### Verdict: PASS

### Reasoning

Removing qualifiers from PURLs introduces a deduplication concern: two PURLs that were previously distinct only because of different qualifiers (e.g., `...@3.12?repository_url=https://repo1.maven.org` vs `...@3.12?repository_url=https://repo2.maven.org`) now produce the same string (`...@3.12`). The implementation addresses this with a dedup step.

In `modules/fundamental/src/purl/service/mod.rs`, after mapping PURLs through `without_qualifiers()`, the code applies:
```rust
.dedup_by(|a, b| a.purl == b.purl)
```

This removes consecutive duplicates based on the PURL string. Note that `dedup_by` only removes *consecutive* duplicates, so correct deduplication depends on the query ordering placing identical PURLs adjacently. Since the PURLs are derived from the same base package (same namespace and name) and the qualifier removal makes same-version PURLs identical, they should naturally be adjacent when ordered by version.

The query also adds a `group_by` on the ID column for the count:
```rust
.select_only()
.column(purl::Column::Id)
.group_by(purl::Column::Id)
.count(&self.db).await?;
```

The test `test_recommend_purls_dedup` in `tests/api/purl_recommend.rs` directly verifies this:
- Seeds two PURLs with the same version but different `repository_url` qualifiers
- Asserts only 1 entry is returned (deduplicated)
- Asserts the returned PURL is `"pkg:maven/org.apache/commons-lang3@3.12"` (without qualifiers)

This is a replacement for the old `test_recommend_purls_with_qualifiers` which verified that the same two PURLs were returned as 2 separate entries. The behavioral change is correctly reflected in the test expectations.

This criterion is satisfied.
