# Criterion 3: Deduplication of entries previously distinct due to different qualifiers

## Acceptance Criterion
Duplicate entries that were previously distinct due to different qualifiers are deduplicated in the response.

## Evidence

### Production Code Changes

In `modules/fundamental/src/purl/service/mod.rs`, after mapping PURLs through `without_qualifiers()`, the PR adds:
```rust
.dedup_by(|a, b| a.purl == b.purl)
```

This removes consecutive duplicate PURLs that became identical after qualifier stripping. Note: `dedup_by` only removes consecutive duplicates, which relies on the upstream query ordering to group identical versioned PURLs together. Since the query sorts by the same columns that determine PURL identity (namespace, name, version), consecutive duplicates from different qualifiers will be adjacent.

### Test Evidence

The new `test_recommend_purls_dedup` function in `tests/api/purl_recommend.rs` directly tests this:
- Seeds two PURLs with the same version but different `repository_url` qualifiers:
  - `"pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo1.maven.org&type=jar"`
  - `"pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo2.maven.org&type=jar"`
- Asserts only 1 item is returned: `assert_eq!(body.items.len(), 1);`
- Asserts the result is the deduplicated versioned PURL: `assert_eq!(body.items[0].purl, "pkg:maven/org.apache/commons-lang3@3.12");`

This directly validates that entries that were previously distinct (due to different qualifiers) are now collapsed into a single entry.

All CI checks pass.

## Verdict: PASS

The production code adds `dedup_by` after qualifier removal, and the `test_recommend_purls_dedup` test explicitly verifies that two qualifier-variant PURLs collapse to one.
