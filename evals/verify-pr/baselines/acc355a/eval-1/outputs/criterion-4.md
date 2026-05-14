## Criterion 4: Filter integrates with existing pagination -- filtered results are paginated correctly

### Verdict: PASS

### Evidence

**Service layer (`service/mod.rs`):**
- The license filter is applied to the query *before* pagination. The implementation adds the WHERE clause and JOIN first, then the existing pagination logic applies:
  - `let total = query.clone().count(&self.db).await?;` counts only filtered results
  - The subsequent `query` with offset/limit retrieves the correct page of filtered results
- The `total` count reflects the filtered set, not the unfiltered set, which is essential for correct pagination metadata.

**Endpoint layer (`list.rs`):**
- The `PackageListParams` struct retains `offset: Option<i64>` and `limit: Option<i64>` alongside the new `license: Option<String>`. All three parameters are independently extracted from the query string and passed through.

**Test evidence (`tests/api/package.rs`):**
- `test_list_packages_license_filter_with_pagination` seeds 5 MIT packages and 1 Apache-2.0 package, requests `?license=MIT&limit=2&offset=0`, and asserts:
  - Response status is 200 OK
  - `body.items.len() == 2` (respects the limit parameter)
  - `body.total == 5` (total count reflects all MIT packages, not just the page)

This confirms the filter composes correctly with pagination: the total reflects the filtered count and the page size is respected.
