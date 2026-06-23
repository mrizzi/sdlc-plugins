## Criterion 2: Check 6 verifies each new symbol has a documentation comment using the language's convention

### Verdict: PASS

### Reasoning

The PR adds section "6b -- Check Documentation Comments" to `style-conventions.md` which instructs:

> For each new symbol identified in 6a, check whether a documentation comment immediately precedes the definition. Use the language's standard convention:

It then lists language-specific doc comment patterns:
- **Rust:** `///` or `//!` doc comments
- **TypeScript/Java:** `/** ... */` JSDoc/Javadoc blocks
- **Python:** `"""..."""` docstrings immediately inside the function/class body
- **Go:** `//` comment immediately preceding the symbol declaration
- **Markdown:** not applicable -- skip Markdown files

The check verifies "each new symbol" (iterating over the symbols identified in 6a) and uses "the language's convention" (with five language-specific patterns listed). The instruction to "Record each symbol's documentation status (documented or undocumented)" confirms per-symbol verification.

### Evidence

- File: `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md`
- Diff lines adding section "6b -- Check Documentation Comments" with language-specific doc comment patterns
