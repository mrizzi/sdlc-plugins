# Criterion 2: Check 6 verifies each new symbol has a documentation comment using the language's convention

## Verdict: PASS

## Analysis

The diff adds Step 6b ("Check Documentation Comments") to `style-conventions.md`. This step instructs the sub-agent to check whether a documentation comment immediately precedes each new symbol definition, using language-specific conventions:

- **Rust:** `///` or `//!` doc comments
- **TypeScript/Java:** `/** ... */` JSDoc/Javadoc blocks
- **Python:** `"""..."""` docstrings immediately inside the function/class body
- **Go:** `//` comment immediately preceding the symbol declaration
- **Markdown:** not applicable -- skip Markdown files

The step records each symbol's documentation status (documented or undocumented), directly satisfying this acceptance criterion.

## Evidence

- File: `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md`
- Step 6b provides language-specific doc comment patterns for Rust, TypeScript/Java, Python, Go
- Explicitly records documentation status per symbol
