## Criterion 2: Response PURLs do not contain `?` query parameters (no qualifiers present)

**Verdict: PASS**

### Analysis

The service layer change in `modules/fundamental/src/purl/service/mod.rs` calls `p.without_qualifiers()` on every PURL before serialization. The `without_qualifiers()` method (from `common/src/purl.rs` per the task's Implementation Notes) constructs a PURL without any qualifier key-value pairs, which means no `?` character will appear in the serialized string.

The qualifier join that previously fetched qualifier data from the database was also removed:

```diff
-            .join(JoinType::LeftJoin, purl::Relation::PurlQualifier.def());
```

This means qualifier data is not even fetched from the database, eliminating any possibility of qualifiers leaking into the response.

### Test Evidence

Multiple tests explicitly assert the absence of `?` in response PURLs:

In `tests/api/purl_recommend.rs`, `test_recommend_purls_basic`:
```rust
assert!(!body.items[0].purl.contains('?'));
assert!(!body.items[1].purl.contains('?'));
```

In `tests/api/purl_simplify.rs`, `test_simplified_purl_no_version`:
```rust
assert!(!body.items[0].purl.contains('?'));
```

In `tests/api/purl_simplify.rs`, `test_simplified_purl_mixed_types`:
```rust
assert!(!body.items[0].purl.contains("vcs_url"));
```

In `tests/api/purl_simplify.rs`, `test_simplified_purl_ordering_preserved`:
```rust
assert!(!body.items[0].purl.contains('?'));
assert!(!body.items[1].purl.contains('?'));
```

The combination of the service-layer qualifier stripping and the comprehensive test assertions on absence of `?` satisfies this criterion.
