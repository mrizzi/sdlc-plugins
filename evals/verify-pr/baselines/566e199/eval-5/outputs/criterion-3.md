# Criterion 3: Duplicate entries that were previously distinct due to different qualifiers are deduplicated in the response

## Verdict: PASS

## Analysis

The PR adds deduplication logic in `modules/fundamental/src/purl/service/mod.rs`:

```rust
.dedup_by(|a, b| a.purl == b.purl)
```

This is applied after the `.map()` call that strips qualifiers via `without_qualifiers()`. The `dedup_by` method removes consecutive duplicate entries where the PURL strings match. Since qualifiers have been stripped, PURLs that were previously distinct only due to different qualifiers (e.g., same package/version but different `repository_url`) now have identical PURL strings and are deduplicated.

The test `test_recommend_purls_dedup` in `tests/api/purl_recommend.rs` directly verifies this behavior:
- Seeds two PURLs for the same package version but with different qualifiers:
  - `pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo1.maven.org&type=jar`
  - `pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo2.maven.org&type=jar`
- After requesting recommendations, asserts only 1 item is returned (deduplicated)
- Asserts the returned PURL is `pkg:maven/org.apache/commons-lang3@3.12` (no qualifiers)

Note: `dedup_by` only removes consecutive duplicates. This works correctly here because the query results are ordered, and entries with the same namespace/name/version will be adjacent. The query filtering on `purl::Column::Namespace` and `purl::Column::Name` ensures results are scoped to the same package, and ordering would group same-version entries together.
