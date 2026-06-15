# Criterion 2: Check 6 verifies each new symbol has a documentation comment using the language's convention

## Verdict: PASS

## Reasoning

The diff adds section "6b -- Check Documentation Comments" to style-conventions.md. This section instructs checking whether a documentation comment immediately precedes each new symbol definition, with language-specific conventions listed:

- Rust: `///` or `//!` doc comments
- TypeScript/Java: `/** ... */` JSDoc/Javadoc blocks
- Python: `"""..."""` docstrings immediately inside the function/class body
- Go: `//` comment immediately preceding the symbol declaration
- Markdown: not applicable -- skip Markdown files

## Evidence

From the diff in style-conventions.md:
```
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
```

The criterion is satisfied -- Check 6 verifies documentation comments using language-specific conventions.
