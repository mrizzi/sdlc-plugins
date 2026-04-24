# Criterion 2: Response PURLs do not contain `?` query parameters

## Criterion
Response PURLs do not contain `?` query parameters (no qualifiers present).

## Result: PASS

## Detailed Reasoning

The PR addresses this criterion at two levels: implementation and test verification.

### Implementation Level

In `modules/fundamental/src/purl/service/mod.rs`, the `without_qualifiers()` method is called on every PURL before it is converted to a string for the response. The `without_qualifiers()` method (referenced in the task's Implementation Notes as part of the `PackageUrl` builder in `common/src/purl.rs`) strips all qualifier key-value pairs from the PURL, which are the components that appear after the `?` character in a PURL string.

Additionally, the `JoinType::LeftJoin` on `purl::Relation::PurlQualifier` has been removed from the query, so qualifier data is not even fetched from the database. This provides a defense-in-depth approach: even if `without_qualifiers()` were somehow bypassed, no qualifier data would be available to serialize.

### Test Verification Level

The updated `test_recommend_purls_basic` test explicitly asserts the absence of `?` in response PURLs:

```rust
assert!(!body.items[0].purl.contains('?'));
assert!(!body.items[1].purl.contains('?'));
```

These assertions directly verify the criterion's requirement. If any qualifier leaked through, the `?` character would be present and the test would fail.

The new `test_recommend_purls_dedup` test also asserts a specific PURL value without qualifiers:
```rust
assert_eq!(body.items[0].purl, "pkg:maven/org.apache/commons-lang3@3.12");
```

And in `tests/api/purl_simplify.rs`, every test includes assertions verifying the absence of qualifiers:
- `test_simplified_purl_no_version`: `assert!(!body.items[0].purl.contains('?'));`
- `test_simplified_purl_mixed_types`: `assert!(!body.items[0].purl.contains("vcs_url"));`
- `test_simplified_purl_ordering_preserved`: `assert!(!body.items[0].purl.contains('?'));` and `assert!(!body.items[1].purl.contains('?'));`

The criterion is satisfied both by the implementation (qualifier stripping) and comprehensive test assertions.
