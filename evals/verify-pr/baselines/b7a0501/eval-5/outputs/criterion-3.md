# Criterion 3: Duplicate entries are deduplicated after qualifier removal

## Acceptance Criterion
Duplicate entries that were previously distinct due to different qualifiers are deduplicated in the response.

## Verdict: PASS

## Reasoning

### Production Code

In `modules/fundamental/src/purl/service/mod.rs`, after stripping qualifiers via `without_qualifiers()`, a deduplication step is applied:

```rust
.dedup_by(|a, b| a.purl == b.purl)
```

This ensures that PURLs which were previously distinct only because of different qualifiers (e.g., different `repository_url` values) are collapsed into a single entry.

### Test Evidence

The new `test_recommend_purls_dedup` function in `tests/api/purl_recommend.rs` directly verifies this behavior:

- Seeds two PURLs for the same package/version but with different qualifiers (`repo1.maven.org` vs `repo2.maven.org`)
- Asserts that only one item is returned after qualifier removal and deduplication:
```rust
assert_eq!(body.items.len(), 1);
assert_eq!(body.items[0].purl, "pkg:maven/org.apache/commons-lang3@3.12");
```

This replaces the old `test_recommend_purls_with_qualifiers` which asserted that both qualifier variants were returned as separate entries -- the inverse of the new behavior.
