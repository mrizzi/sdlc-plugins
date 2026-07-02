## Criterion 2: Check 6 verifies each new symbol has a documentation comment using the language's convention

**Verdict: PASS**

The diff adds section "6b -- Check Documentation Comments" which specifies language-specific doc comment conventions:

- **Rust:** `///` or `//!` doc comments
- **TypeScript/Java:** `/** ... */` JSDoc/Javadoc blocks
- **Python:** `"""..."""` docstrings immediately inside the function/class body
- **Go:** `//` comment immediately preceding the symbol declaration
- **Markdown:** not applicable -- skip Markdown files

The section instructs: "For each new symbol identified in 6a, check whether a documentation comment immediately precedes the definition." This covers the five major languages with their standard doc comment conventions, satisfying the criterion that each new symbol is verified against the language's convention.
