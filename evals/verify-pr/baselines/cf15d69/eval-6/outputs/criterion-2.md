# Criterion 2: Check 6 verifies each new symbol has a documentation comment using the language's convention

## Verdict: PASS

## Reasoning

The PR diff adds section "6b -- Check Documentation Comments" to `style-conventions.md` that explicitly verifies each new symbol has a documentation comment using language-specific conventions:

> For each new symbol identified in 6a, check whether a documentation comment
> immediately precedes the definition. Use the language's standard convention:
>
> - **Rust:** `///` or `//!` doc comments
> - **TypeScript/Java:** `/** ... */` JSDoc/Javadoc blocks
> - **Python:** `"""..."""` docstrings immediately inside the function/class body
> - **Go:** `//` comment immediately preceding the symbol declaration
> - **Markdown:** not applicable -- skip Markdown files

The check covers all five languages mentioned in the task's Implementation Notes (Rust `///`, Java/TypeScript `/** */`, Python `"""`, Go `//`) and adds an explicit Markdown exclusion. Each language's standard doc comment convention is correctly identified.

The criterion is satisfied.
