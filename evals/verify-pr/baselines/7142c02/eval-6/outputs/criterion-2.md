# Criterion 2: Check 6 verifies each new symbol has a documentation comment using the language's convention

## Verdict: PASS

## Reasoning

Step 6b ("Check Documentation Comments") in the added Check 6 defines language-specific doc comment conventions:

- **Rust:** `///` or `//!` doc comments
- **TypeScript/Java:** `/** ... */` JSDoc/Javadoc blocks
- **Python:** `"""..."""` docstrings immediately inside the function/class body
- **Go:** `//` comment immediately preceding the symbol declaration
- **Markdown:** not applicable -- skip Markdown files

The step instructs: "For each new symbol identified in 6a, check whether a documentation comment immediately precedes the definition."

This covers the major languages with their standard doc comment patterns. Each symbol's documentation status is recorded as documented or undocumented.

The criterion is satisfied: Check 6 verifies each new symbol has a documentation comment using language-appropriate conventions.
