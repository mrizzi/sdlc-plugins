# Criterion 2: Check 6 verifies each new symbol has a documentation comment using the language's convention

## Verdict: PASS

## Reasoning

The PR diff adds section 6b ("Check Documentation Comments") to style-conventions.md. This section specifies checking whether a documentation comment immediately precedes each new symbol definition. It lists language-specific conventions:

- **Rust:** `///` or `//!` doc comments
- **TypeScript/Java:** `/** ... */` JSDoc/Javadoc blocks
- **Python:** `"""..."""` docstrings immediately inside the function/class body
- **Go:** `//` comment immediately preceding the symbol declaration
- **Markdown:** not applicable -- skip Markdown files

Each symbol's documentation status is recorded as documented or undocumented.

This satisfies the criterion -- Check 6 verifies each new symbol has a documentation comment using the language's convention.
