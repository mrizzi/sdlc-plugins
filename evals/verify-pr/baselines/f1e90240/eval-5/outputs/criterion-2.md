# Criterion 2: Response PURLs do not contain `?` query parameters

## Criterion Text
Response PURLs do not contain `?` query parameters (no qualifiers present)

## Verdict: PASS

## Reasoning

The PR satisfies this criterion through both the implementation logic and explicit test assertions.

### Implementation Guarantee (`modules/fundamental/src/purl/service/mod.rs`)

The service layer calls `p.without_qualifiers()` on each PURL model before serialization. According to the task's Implementation Notes, the `PackageUrl` builder in `common/src/purl.rs` supports the `without_qualifiers()` method, which constructs a PURL without any qualifier key-value pairs. Since qualifiers are the portion of a PURL that follows the `?` character, stripping them guarantees no `?` appears in the output string.

Additionally, the qualifier join was removed from the query:

```rust
// Before (removed):
.join(JoinType::LeftJoin, purl::Relation::PurlQualifier.def());

// After: no join at all
```

This means qualifier data is not even fetched from the database, providing a second layer of assurance that qualifiers cannot leak into the response.

### Test Assertions (`tests/api/purl_recommend.rs`)

The updated `test_recommend_purls_basic` test explicitly asserts the absence of `?` in response PURLs:

```rust
assert!(!body.items[0].purl.contains('?'));
assert!(!body.items[1].purl.contains('?'));
```

These assertions directly verify the criterion: response PURLs do not contain `?` query parameters.

### Additional Test Coverage (`tests/api/purl_simplify.rs`)

The new test file reinforces this criterion across multiple scenarios:

- `test_simplified_purl_no_version`: `assert!(!body.items[0].purl.contains('?'));`
- `test_simplified_purl_mixed_types`: `assert!(!body.items[0].purl.contains("vcs_url"));` (checks that specific qualifier keys are absent)
- `test_simplified_purl_ordering_preserved`: `assert!(!body.items[0].purl.contains('?'));` and `assert!(!body.items[1].purl.contains('?'));`

Every test that inspects response PURLs includes an explicit assertion that qualifiers (indicated by `?`) are absent. This provides comprehensive coverage of the criterion.
