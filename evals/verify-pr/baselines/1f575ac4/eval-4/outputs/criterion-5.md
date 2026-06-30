# Criterion 5: Response serialization includes the new field in JSON output

## Criterion Text
Response serialization includes the new field in JSON output

## Verdict: PASS

## Reasoning

The `vulnerability_count` field is added to the `PackageSummary` struct in `modules/fundamental/src/package/model/summary.rs`. Based on the repository conventions (Axum + SeaORM, with Serde serialization), struct fields are serialized into JSON responses by default when the struct derives `Serialize`.

The endpoint in `modules/fundamental/src/package/endpoints/list.rs` returns `Json<PaginatedResults<PackageSummary>>`, which means all public fields of `PackageSummary` are included in the JSON response. The diff shows the endpoint continues to call `PackageService::list()` and return the result as JSON:

```rust
     let results = PackageService::new(&db)
-        .list(params.offset, params.limit)
+        .list(params.offset, params.limit)  // vulnerability_count now included in response
         .await
         .context("Failed to list packages")?;
```

The comment confirms the intent that `vulnerability_count` is now part of the response. Since the field is a public `i64` on a serializable struct that is wrapped in `Json<>` for the response, it will be included in the JSON output automatically.

The integration tests further confirm this by deserializing the response into `PaginatedResults<PackageSummary>` and accessing `pkg.vulnerability_count`, which would fail if the field were not present in the JSON.

## Evidence
- File: `modules/fundamental/src/package/model/summary.rs` -- field added to struct
- File: `modules/fundamental/src/package/endpoints/list.rs` -- returns `Json<PaginatedResults<PackageSummary>>`
- File: `tests/api/package_vuln_count.rs` -- tests deserialize the response and access `vulnerability_count`
