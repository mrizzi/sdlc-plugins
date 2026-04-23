<!-- SYNTHETIC TEST DATA — mock PR diff for eval testing; simulates `gh pr diff` output for a passing implementation -->

```diff
diff --git a/modules/fundamental/src/package/endpoints/list.rs b/modules/fundamental/src/package/endpoints/list.rs
index 8a3f2d1..c4e5b7a 100644
--- a/modules/fundamental/src/package/endpoints/list.rs
+++ b/modules/fundamental/src/package/endpoints/list.rs
@@ -1,6 +1,7 @@
 use axum::extract::Query;
 use axum::Json;
 use sea_orm::DatabaseConnection;
+use spdx::Expression;

 use crate::package::service::PackageService;
 use common::db::query::Filtering;
@@ -10,10 +11,16 @@ use common::model::paginated::PaginatedResults;
 #[derive(Debug, Deserialize)]
 pub struct PackageListParams {
     pub offset: Option<i64>,
     pub limit: Option<i64>,
+    pub license: Option<String>,
 }

+/// Validates that each license identifier in the comma-separated list is a known SPDX expression.
+fn validate_license_param(license: &str) -> Result<Vec<String>, AppError> {
+    let identifiers: Vec<String> = license.split(',').map(|s| s.trim().to_string()).collect();
+    for id in &identifiers {
+        Expression::parse(id).map_err(|_| {
+            AppError::BadRequest(format!("Invalid SPDX license identifier: {}", id))
+        })?;
+    }
+    Ok(identifiers)
+}
+
 /// Handles GET /api/v2/package with optional license filtering.
 pub async fn list_packages(
     db: DatabaseConnection,
     Query(params): Query<PackageListParams>,
 ) -> Result<Json<PaginatedResults<PackageSummary>>, AppError> {
+    let license_filter = match &params.license {
+        Some(license) => Some(validate_license_param(license)?),
+        None => None,
+    };
+
     let results = PackageService::new(&db)
-        .list(params.offset, params.limit)
+        .list(params.offset, params.limit, license_filter.as_deref())
         .await
         .context("Failed to list packages")?;

diff --git a/modules/fundamental/src/package/service/mod.rs b/modules/fundamental/src/package/service/mod.rs
index 1b2c3d4..e5f6a7b 100644
--- a/modules/fundamental/src/package/service/mod.rs
+++ b/modules/fundamental/src/package/service/mod.rs
@@ -18,12 +18,14 @@ impl PackageService {
     }

     /// Lists packages with optional pagination and license filtering.
-    pub async fn list(&self, offset: Option<i64>, limit: Option<i64>) -> Result<PaginatedResults<PackageSummary>> {
+    pub async fn list(
+        &self,
+        offset: Option<i64>,
+        limit: Option<i64>,
+        license_filter: Option<&[String]>,
+    ) -> Result<PaginatedResults<PackageSummary>> {
         let mut query = Package::find();

+        if let Some(licenses) = license_filter {
+            query = query.filter(
+                Condition::any()
+                    .add(package_license::Column::License.is_in(licenses.iter().cloned()))
+            );
+            query = query.join(JoinType::InnerJoin, package::Relation::PackageLicense.def());
+        }
+
         let total = query.clone().count(&self.db).await?;

         let items = query
diff --git a/tests/api/package.rs b/tests/api/package.rs
new file mode 100644
index 0000000..a1b2c3d
--- /dev/null
+++ b/tests/api/package.rs
@@ -0,0 +1,80 @@
+use crate::common::TestContext;
+use axum::http::StatusCode;
+
+/// Verifies that filtering by a single license returns only matching packages.
+#[test_context(TestContext)]
+#[tokio::test]
+async fn test_list_packages_single_license_filter(ctx: &TestContext) {
+    // Given packages with MIT and Apache-2.0 licenses in the database
+    ctx.seed_package("pkg-a", "MIT").await;
+    ctx.seed_package("pkg-b", "Apache-2.0").await;
+    ctx.seed_package("pkg-c", "MIT").await;
+
+    // When filtering by MIT license
+    let resp = ctx.get("/api/v2/package?license=MIT").await;
+
+    // Then only MIT-licensed packages are returned
+    assert_eq!(resp.status(), StatusCode::OK);
+    let body: PaginatedResults<PackageSummary> = resp.json().await;
+    assert_eq!(body.items.len(), 2);
+    assert!(body.items.iter().all(|p| p.license == "MIT"));
+}
+
+/// Verifies that comma-separated license values return the union of matching packages.
+#[test_context(TestContext)]
+#[tokio::test]
+async fn test_list_packages_multi_license_filter(ctx: &TestContext) {
+    // Given packages with MIT, Apache-2.0, and GPL-3.0 licenses
+    ctx.seed_package("pkg-a", "MIT").await;
+    ctx.seed_package("pkg-b", "Apache-2.0").await;
+    ctx.seed_package("pkg-c", "GPL-3.0-only").await;
+
+    // When filtering by MIT and Apache-2.0
+    let resp = ctx.get("/api/v2/package?license=MIT,Apache-2.0").await;
+
+    // Then packages with either license are returned
+    assert_eq!(resp.status(), StatusCode::OK);
+    let body: PaginatedResults<PackageSummary> = resp.json().await;
+    assert_eq!(body.items.len(), 2);
+    assert!(body.items.iter().all(|p| p.license == "MIT" || p.license == "Apache-2.0"));
+}
+
+/// Verifies that an invalid SPDX license identifier returns 400 Bad Request.
+#[test_context(TestContext)]
+#[tokio::test]
+async fn test_list_packages_invalid_license_returns_400(ctx: &TestContext) {
+    // When requesting with an invalid license identifier
+    let resp = ctx.get("/api/v2/package?license=INVALID-999").await;
+
+    // Then a 400 Bad Request is returned
+    assert_eq!(resp.status(), StatusCode::BAD_REQUEST);
+}
+
+/// Verifies that license filtering integrates correctly with pagination parameters.
+#[test_context(TestContext)]
+#[tokio::test]
+async fn test_list_packages_license_filter_with_pagination(ctx: &TestContext) {
+    // Given 5 MIT-licensed packages
+    for i in 0..5 {
+        ctx.seed_package(&format!("pkg-{}", i), "MIT").await;
+    }
+    ctx.seed_package("pkg-other", "Apache-2.0").await;
+
+    // When filtering by MIT with limit=2 and offset=0
+    let resp = ctx.get("/api/v2/package?license=MIT&limit=2&offset=0").await;
+
+    // Then only 2 items are returned but total reflects all MIT packages
+    assert_eq!(resp.status(), StatusCode::OK);
+    let body: PaginatedResults<PackageSummary> = resp.json().await;
+    assert_eq!(body.items.len(), 2);
+    assert_eq!(body.total, 5);
+}
```
