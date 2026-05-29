<!-- SYNTHETIC TEST DATA — names, URLs, and identifiers are fictional -->

```diff
diff --git a/plugins/sdlc-workflow/skills/verify-pr/style-conventions.md b/plugins/sdlc-workflow/skills/verify-pr/style-conventions.md
index 8a3b4c5..f1e2d3c 100644
--- a/plugins/sdlc-workflow/skills/verify-pr/style-conventions.md
+++ b/plugins/sdlc-workflow/skills/verify-pr/style-conventions.md
@@ -282,6 +282,48 @@ Evidence: per-eval pass rates, overall pass rate, and any failing assertion
 details (assertion text and evidence for each failure).
 
+### Check 6 — Documentation Coverage
+
+Verify that new public symbols introduced in the PR have documentation comments
+using the language's standard doc comment convention.
+
+#### 6a — Identify New Symbols
+
+Scan the PR diff for newly added function, method, struct, class, interface,
+enum, and type definitions. A symbol is "new" if its definition line appears
+in the diff with a `+` prefix and has no corresponding `-` line (not a rename
+or modification of an existing symbol).
+
+If no new symbols are found, skip to the Verdict and record N/A.
+
+#### 6b — Check Documentation Comments
+
+For each new symbol identified in 6a, check whether a documentation comment
+immediately precedes the definition. Use the language's standard convention:
+
+- **Rust:** `///` or `//!` doc comments
+- **TypeScript/Java:** `/** ... */` JSDoc/Javadoc blocks
+- **Python:** `"""..."""` docstrings immediately inside the function/class body
+- **Go:** `//` comment immediately preceding the symbol declaration
+- **Markdown:** not applicable — skip Markdown files
+
+Record each symbol's documentation status (documented or undocumented).
+
+#### 6c — Produce Verdict
+
+- **PASS** — all new symbols have documentation comments
+- **WARN** — at least one new symbol lacks a documentation comment
+- **N/A** — no new symbols introduced in the PR
+
+Evidence: list of undocumented symbols with file path and line number.
+
 ## Output Format
 
-Produce exactly five rows:
+Produce exactly six rows:
 
 ```
 | Check | Verdict | Details |
@@ -291,4 +333,5 @@ Produce exactly five rows:
 | Test Documentation       | <PASS|WARN|N/A> | <one-line summary>              |
 | Eval Quality             | <PASS|WARN|N/A> | <one-line summary with pass rate> |
+| Documentation Coverage   | <PASS|WARN|N/A> | <one-line summary>              |
 ```
diff --git a/plugins/sdlc-workflow/skills/verify-pr/SKILL.md b/plugins/sdlc-workflow/skills/verify-pr/SKILL.md
index 2c4d5e6..7f8a9b0 100644
--- a/plugins/sdlc-workflow/skills/verify-pr/SKILL.md
+++ b/plugins/sdlc-workflow/skills/verify-pr/SKILL.md
@@ -354,6 +354,7 @@ Add a new mapping row:
 | Style/Conventions | Repetitive Test Detection | Test Quality *(combined)* |
 | Style/Conventions | Test Documentation        | Test Quality *(combined)* |
 | Style/Conventions | Eval Quality              | Test Quality *(combined)* |
+| Style/Conventions | Documentation Coverage    | Style Quality *(new)*     |
 ```
```
