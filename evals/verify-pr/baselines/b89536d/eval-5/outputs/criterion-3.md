# Criterion 3: Duplicate entries that were previously distinct due to different qualifiers are deduplicated in the response

## Verdict: PASS

## Reasoning

The PR implements deduplication in the service layer and verifies it with a dedicated test:

1. **Service layer deduplication**: In `modules/fundamental/src/purl/service/mod.rs`, after stripping qualifiers, the code applies `.dedup_by(|a, b| a.purl == b.purl)` to the results iterator:
   ```rust
   .map(|p| {
       let simplified = p.without_qualifiers();
       PurlSummary {
           purl: simplified.to_string(),
       }
   })
   .dedup_by(|a, b| a.purl == b.purl)
   .collect();
   ```
   This removes consecutive duplicate entries that became identical after qualifier removal.

2. **Dedicated deduplication test**: The new `test_recommend_purls_dedup` function in `tests/api/purl_recommend.rs` explicitly tests this scenario:
   - Seeds two PURLs that differ only in their qualifiers: `commons-lang3@3.12?repository_url=https://repo1.maven.org` and `commons-lang3@3.12?repository_url=https://repo2.maven.org`
   - Asserts that only one entry is returned after qualifier removal and dedup: `assert_eq!(body.items.len(), 1)`
   - Verifies the returned PURL is the simplified version: `assert_eq!(body.items[0].purl, "pkg:maven/org.apache/commons-lang3@3.12")`

This directly addresses the criterion. The deduplication logic and its test coverage are both present in the PR.
