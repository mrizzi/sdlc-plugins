# Criterion 2: Check 6 verifies each new symbol has a documentation comment using the language's convention

## Verdict: PASS

## Reasoning

The PR diff adds step "6b -- Check Documentation Comments" to `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md`. This step instructs the sub-agent to check whether a documentation comment immediately precedes each new symbol definition, using language-specific conventions:

- **Rust:** `///` or `//!` doc comments
- **TypeScript/Java:** `/** ... */` JSDoc/Javadoc blocks
- **Python:** `"""..."""` docstrings immediately inside the function/class body
- **Go:** `//` comment immediately preceding the symbol declaration
- **Markdown:** not applicable -- skip Markdown files

The step also instructs recording each symbol's documentation status (documented or undocumented).

This satisfies the criterion. The check verifies documentation comments using four distinct language-specific patterns that match the conventions specified in the task's Implementation Notes.

## Evidence

- File: `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md`
- Diff lines: step 6b added at approximately line 298-310 of the new file
- Language-specific patterns match those specified in the task Implementation Notes: `///` for Rust, `/** */` for Java/TypeScript, `"""` for Python, `//` for Go
