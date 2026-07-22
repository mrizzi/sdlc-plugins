# Criterion 1: Check 6 scans the PR diff for new public symbol definitions

## Verdict: PASS

## Reasoning

The PR diff adds section "6a -- Identify New Symbols" to `style-conventions.md` with the following instruction:

> Scan the PR diff for newly added function, method, struct, class, interface, enum, and type definitions. A symbol is "new" if its definition line appears in the diff with a `+` prefix and has no corresponding `-` line (not a rename or modification of an existing symbol).

This explicitly directs the sub-agent to scan the PR diff for new public symbol definitions. The instruction covers the full range of symbol types (function, method, struct, class, interface, enum, type) and includes a clear definition of what constitutes a "new" symbol (added line with `+` prefix, no corresponding `-` line to indicate rename/modification).

The criterion is satisfied: Check 6 scans the PR diff for new public symbol definitions.
