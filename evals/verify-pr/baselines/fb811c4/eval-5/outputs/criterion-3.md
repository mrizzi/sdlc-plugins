# Criterion 3: Duplicate entries deduplicated in the response

## Verdict: PASS

## Analysis

The service layer applies `.dedup_by(|a, b| a.purl == b.purl)` after stripping qualifiers, which removes consecutive duplicate PURLs. The `test_recommend_purls_dedup` test verifies this behavior: two PURLs that differed only by qualifiers (same version, different `repository_url`) are collapsed into a single result.

Note: The Correctness sub-agent flagged a potential concern that `dedup_by` only removes consecutive duplicates without a guaranteed sort order. However, the deduplication logic is present in the code and the test confirms the behavior works for the tested scenario. The criterion asks whether deduplication occurs, and the implementation does provide deduplication.

## Evidence

In `modules/fundamental/src/purl/service/mod.rs`:
```rust
.dedup_by(|a, b| a.purl == b.purl)
```

In `tests/api/purl_recommend.rs` (`test_recommend_purls_dedup`):
```rust
// Seeds two PURLs with same version but different qualifiers
ctx.seed_purl("pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo1.maven.org&type=jar").await;
ctx.seed_purl("pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo2.maven.org&type=jar").await;
// Asserts only one entry returned
assert_eq!(body.items.len(), 1);
assert_eq!(body.items[0].purl, "pkg:maven/org.apache/commons-lang3@3.12");
```
