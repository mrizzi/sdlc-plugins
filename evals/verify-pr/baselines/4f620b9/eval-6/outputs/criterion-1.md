## Criterion 1: Check 6 scans the PR diff for new public symbol definitions

### Verdict: PASS

### Reasoning

The PR adds section "6a -- Identify New Symbols" to `style-conventions.md` which explicitly instructs the sub-agent to:

> Scan the PR diff for newly added function, method, struct, class, interface, enum, and type definitions. A symbol is "new" if its definition line appears in the diff with a `+` prefix and has no corresponding `-` line (not a rename or modification of an existing symbol).

This directly satisfies the criterion. The check scans the PR diff (the input source is the PR diff), and it targets new public symbol definitions (function, method, struct, class, interface, enum, type). The definition of "new" is also clearly specified -- a symbol whose definition line has a `+` prefix with no corresponding `-` line.

### Evidence

- File: `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md`
- Diff lines adding section "6a -- Identify New Symbols" with scanning instructions
