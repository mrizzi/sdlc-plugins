# Criterion 2: Response PURLs do not contain ? query parameters

**Criterion:** Response PURLs do not contain `?` query parameters (no qualifiers present)

**Result:** PASS

## Reasoning

The PR ensures that no response PURL contains the `?` character (which would indicate qualifier parameters) through both implementation and test verification.

**Implementation:** The service layer in `modules/fundamental/src/purl/service/mod.rs` calls `p.without_qualifiers()` on every PURL before serialization. The `without_qualifiers()` method on the `PackageUrl` builder (from `common/src/purl.rs` per the task's Implementation Notes) constructs a PURL with only the type, namespace, name, and version components -- no qualifier query string.

**Test coverage:** Multiple test functions explicitly assert the absence of `?` in response PURLs:

- `test_recommend_purls_basic` (modified):
  ```rust
  assert!(!body.items[0].purl.contains('?'));
  assert!(!body.items[1].purl.contains('?'));
  ```

- `test_simplified_purl_no_version` (new):
  ```rust
  assert!(!body.items[0].purl.contains('?'));
  ```

- `test_simplified_purl_mixed_types` (new):
  ```rust
  assert!(!body.items[0].purl.contains("vcs_url"));
  ```
  This asserts that a specific qualifier key is absent from the response.

- `test_simplified_purl_ordering_preserved` (new):
  ```rust
  assert!(!body.items[0].purl.contains('?'));
  assert!(!body.items[1].purl.contains('?'));
  ```

The `contains('?')` assertions are a robust negative check -- they verify the absence of any qualifier string regardless of what qualifiers were present in the seeded data. This approach is stronger than checking for specific qualifier keys because it catches any qualifier, including ones not anticipated in the test fixtures.
