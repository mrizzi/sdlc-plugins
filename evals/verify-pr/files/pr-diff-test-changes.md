<!-- SYNTHETIC TEST DATA — mock PR diff for eval testing; simulates `gh pr diff` output for a PR with both additive and reductive test changes -->

```diff
diff --git a/modules/fundamental/src/purl/endpoints/recommend.rs b/modules/fundamental/src/purl/endpoints/recommend.rs
index 2a4f8c1..b7d3e9f 100644
--- a/modules/fundamental/src/purl/endpoints/recommend.rs
+++ b/modules/fundamental/src/purl/endpoints/recommend.rs
@@ -1,6 +1,5 @@
 use axum::extract::Query;
 use axum::Json;
-use sea_orm::JoinType;
 use sea_orm::DatabaseConnection;
 
 use crate::purl::service::PurlService;
@@ -22,7 +21,7 @@ pub async fn recommend_purls(
     db: DatabaseConnection,
     Query(params): Query<RecommendParams>,
 ) -> Result<Json<PaginatedResults<PurlSummary>>, AppError> {
-    let results = PurlService::new(&db)
+    let results = PurlService::new(&db)
         .recommend(&params.purl, params.offset, params.limit)
         .await
         .context("Failed to get PURL recommendations")?;
diff --git a/modules/fundamental/src/purl/service/mod.rs b/modules/fundamental/src/purl/service/mod.rs
index 3c5d1e2..a8f4b7c 100644
--- a/modules/fundamental/src/purl/service/mod.rs
+++ b/modules/fundamental/src/purl/service/mod.rs
@@ -42,18 +42,15 @@ impl PurlService {
         offset: Option<i64>,
         limit: Option<i64>,
     ) -> Result<PaginatedResults<PurlSummary>> {
-        let mut query = Purl::find()
+        let mut query = Purl::find()
             .filter(purl::Column::Namespace.eq(&base_purl.namespace))
-            .filter(purl::Column::Name.eq(&base_purl.name))
-            .join(JoinType::LeftJoin, purl::Relation::PurlQualifier.def());
+            .filter(purl::Column::Name.eq(&base_purl.name));
 
-        let total = query.clone().count(&self.db).await?;
+        let total = query.clone()
+            .select_only()
+            .column(purl::Column::Id)
+            .group_by(purl::Column::Id)
+            .count(&self.db).await?;
 
         let items = query
             .offset(offset.unwrap_or(0) as u64)
@@ -61,11 +58,12 @@ impl PurlService {
             .all(&self.db)
             .await?
             .into_iter()
-            .map(|p| PurlSummary {
-                purl: p.to_string(),
+            .map(|p| {
+                let simplified = p.without_qualifiers();
+                PurlSummary {
+                    purl: simplified.to_string(),
+                }
             })
+            .dedup_by(|a, b| a.purl == b.purl)
             .collect();
 
         Ok(PaginatedResults { items, total })
diff --git a/tests/api/purl_recommend.rs b/tests/api/purl_recommend.rs
index 5e6a7b8..c9d1f2e 100644
--- a/tests/api/purl_recommend.rs
+++ b/tests/api/purl_recommend.rs
@@ -4,14 +4,14 @@ use common::model::paginated::PaginatedResults;
 use common::purl::PurlSummary;
 
-/// Verifies that basic PURL recommendations return fully qualified PURLs.
+/// Verifies that basic PURL recommendations return versioned PURLs without qualifiers.
 #[test_context(TestContext)]
 #[tokio::test]
 async fn test_recommend_purls_basic(ctx: &TestContext) {
     // Given a package with known PURLs in the database
-    ctx.seed_purl("pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo1.maven.org&type=jar").await;
-    ctx.seed_purl("pkg:maven/org.apache/commons-lang3@3.11?repository_url=https://repo1.maven.org&type=jar").await;
+    ctx.seed_purl("pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo1.maven.org&type=jar").await;
+    ctx.seed_purl("pkg:maven/org.apache/commons-lang3@3.11?repository_url=https://repo1.maven.org&type=jar").await;
 
     // When requesting recommendations for the base PURL
     let resp = ctx.get("/api/v2/purl/recommend?purl=pkg:maven/org.apache/commons-lang3").await;
 
-    // Then recommendations are returned with fully qualified PURLs
+    // Then recommendations are returned with versioned PURLs without qualifiers
     assert_eq!(resp.status(), StatusCode::OK);
     let body: PaginatedResults<PurlSummary> = resp.json().await;
     assert_eq!(body.items.len(), 2);
-    assert_eq!(
-        body.items[0].purl,
-        "pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo1.maven.org&type=jar"
-    );
+    assert_eq!(body.items[0].purl, "pkg:maven/org.apache/commons-lang3@3.12");
+    assert!(!body.items[0].purl.contains('?'));
+    assert!(!body.items[1].purl.contains('?'));
 }
 
-/// Verifies that PURL recommendations include qualifier details when present.
-#[test_context(TestContext)]
-#[tokio::test]
-async fn test_recommend_purls_with_qualifiers(ctx: &TestContext) {
-    // Given PURLs with different qualifiers for the same package version
-    ctx.seed_purl("pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo1.maven.org&type=jar").await;
-    ctx.seed_purl("pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo2.maven.org&type=jar").await;
-
-    // When requesting recommendations
-    let resp = ctx.get("/api/v2/purl/recommend?purl=pkg:maven/org.apache/commons-lang3").await;
-
-    // Then both qualifier variants are returned as separate entries
-    assert_eq!(resp.status(), StatusCode::OK);
-    let body: PaginatedResults<PurlSummary> = resp.json().await;
-    assert_eq!(body.items.len(), 2);
-    assert!(body.items[0].purl.contains("repository_url="));
-    assert!(body.items[1].purl.contains("repository_url="));
-    assert_ne!(body.items[0].purl, body.items[1].purl);
-}
+/// Verifies that removing qualifiers deduplicates entries that were previously distinct.
+#[test_context(TestContext)]
+#[tokio::test]
+async fn test_recommend_purls_dedup(ctx: &TestContext) {
+    // Given PURLs with different qualifiers for the same package version
+    ctx.seed_purl("pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo1.maven.org&type=jar").await;
+    ctx.seed_purl("pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo2.maven.org&type=jar").await;
+
+    // When requesting recommendations (qualifiers stripped, dedup applied)
+    let resp = ctx.get("/api/v2/purl/recommend?purl=pkg:maven/org.apache/commons-lang3").await;
+
+    // Then only one entry is returned (deduplicated after qualifier removal)
+    assert_eq!(resp.status(), StatusCode::OK);
+    let body: PaginatedResults<PurlSummary> = resp.json().await;
+    assert_eq!(body.items.len(), 1);
+    assert_eq!(body.items[0].purl, "pkg:maven/org.apache/commons-lang3@3.12");
+}
 
 /// Verifies that recommendations for an unknown PURL return an empty list.
 #[test_context(TestContext)]
diff --git a/tests/api/purl_simplify.rs b/tests/api/purl_simplify.rs
new file mode 100644
index 0000000..d4e5f6a
--- /dev/null
+++ b/tests/api/purl_simplify.rs
@@ -0,0 +1,62 @@
+use crate::common::TestContext;
+use axum::http::StatusCode;
+use common::model::paginated::PaginatedResults;
+use common::purl::PurlSummary;
+
+/// Verifies that PURLs with only namespace and name (no version) are returned correctly.
+#[test_context(TestContext)]
+#[tokio::test]
+async fn test_simplified_purl_no_version(ctx: &TestContext) {
+    // Given a PURL without a version qualifier
+    ctx.seed_purl("pkg:maven/org.apache/commons-io").await;
+
+    // When requesting recommendations
+    let resp = ctx.get("/api/v2/purl/recommend?purl=pkg:maven/org.apache/commons-io").await;
+
+    // Then the PURL is returned without qualifiers
+    assert_eq!(resp.status(), StatusCode::OK);
+    let body: PaginatedResults<PurlSummary> = resp.json().await;
+    assert_eq!(body.items.len(), 1);
+    assert_eq!(body.items[0].purl, "pkg:maven/org.apache/commons-io");
+    assert!(!body.items[0].purl.contains('?'));
+}
+
+/// Verifies that multiple PURL types are all returned without qualifiers.
+#[test_context(TestContext)]
+#[tokio::test]
+async fn test_simplified_purl_mixed_types(ctx: &TestContext) {
+    // Given PURLs of different types with qualifiers
+    ctx.seed_purl("pkg:npm/%40angular/core@16.0.0?vcs_url=https://github.com/angular/angular").await;
+    ctx.seed_purl("pkg:pypi/requests@2.31.0?repository_url=https://pypi.org/simple").await;
+
+    // When requesting recommendations for npm scope
+    let resp = ctx.get("/api/v2/purl/recommend?purl=pkg:npm/%40angular/core").await;
+
+    // Then qualifiers are stripped from the response
+    assert_eq!(resp.status(), StatusCode::OK);
+    let body: PaginatedResults<PurlSummary> = resp.json().await;
+    assert_eq!(body.items.len(), 1);
+    assert_eq!(body.items[0].purl, "pkg:npm/%40angular/core@16.0.0");
+    assert!(!body.items[0].purl.contains("vcs_url"));
+}
+
+/// Verifies that response ordering is preserved after qualifier removal and dedup.
+#[test_context(TestContext)]
+#[tokio::test]
+async fn test_simplified_purl_ordering_preserved(ctx: &TestContext) {
+    // Given multiple versions of the same package with qualifiers
+    ctx.seed_purl("pkg:maven/org.apache/commons-lang3@3.10?type=jar").await;
+    ctx.seed_purl("pkg:maven/org.apache/commons-lang3@3.11?type=jar").await;
+    ctx.seed_purl("pkg:maven/org.apache/commons-lang3@3.12?type=jar").await;
+
+    // When requesting recommendations with limit
+    let resp = ctx.get("/api/v2/purl/recommend?purl=pkg:maven/org.apache/commons-lang3&limit=2").await;
+
+    // Then results are ordered and paginated correctly without qualifiers
+    assert_eq!(resp.status(), StatusCode::OK);
+    let body: PaginatedResults<PurlSummary> = resp.json().await;
+    assert_eq!(body.items.len(), 2);
+    assert!(!body.items[0].purl.contains('?'));
+    assert!(!body.items[1].purl.contains('?'));
+    assert_eq!(body.total, 3);
+}
```
