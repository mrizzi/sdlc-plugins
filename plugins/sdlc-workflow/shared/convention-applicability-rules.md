# Convention Applicability Rules

Skills that apply conventions from CONVENTIONS.md to tasks (plan-feature) or use
conventions to upgrade review suggestions (verify-pr) must validate that the
convention's scope matches the target files before applying it. This prevents
conventions intended for one file type from being incorrectly applied to unrelated
files.

## Determining a Convention's Target File Types

Extract the convention's scope from its CONVENTIONS.md section by inspecting, in
order of precedence:

1. **Explicit scope statements** — phrases like "for migration files", "applies to
   `.tsx` components", or "when creating `.rs` modules". These directly state the
   convention's target.
2. **File paths in examples** — paths like `migration/m0001200_*.rs` or
   `src/components/*.tsx` in code examples or references. Extract the file
   extensions and directory patterns.
3. **Language-specific syntax** — code snippets using Rust syntax (`.rs`), TypeScript
   syntax (`.ts`/`.tsx`), Python syntax (`.py`), etc. The language implies the
   target file type.

If none of these signals are present, the convention has **no explicit scope** — see
the ambiguous-case rule below.

## Comparing Convention Scope Against Target Files

**For plan-feature (task enrichment):**

Compare the convention's target file types against the task's **Files to Modify**
and **Files to Create** sections. A convention applies if at least one file in
either section matches the convention's scope (by extension or directory pattern).

**For verify-pr (suggestion upgrade):**

Compare the convention's target file types against the PR's changed files list.
A convention applies if at least one changed file matches the convention's scope.

## Applicability Rationale

When a convention passes the applicability check, append a rationale to the
`"Per CONVENTIONS.md §..."` line in Implementation Notes (plan-feature) or to the
upgrade evidence (verify-pr). The rationale is a short sentence explaining why the
convention applies:

```
Per CONVENTIONS.md §<Section Name>: <action required>.
Applies: task modifies <matching file(s)> matching the convention's <scope signal>.
```

Example:

```
Per CONVENTIONS.md §Migration Patterns: add Index::create() for all FK columns.
Applies: task modifies migration/m0042_add_user_fk.rs matching the convention's
migration file scope.
```

## Ambiguous Cases

When a convention does **not** explicitly specify target file types (no scope
statements, no file paths in examples, no language-specific syntax), treat it as
**broadly applicable** — do not filter it out. Broadly applicable conventions
include project-wide rules like naming conventions, commit message formats, or
documentation standards.

The rationale for broadly applicable conventions uses:

```
Applies: convention has no file-type restriction (broadly applicable).
```

## Filtering Example

Given a CONVENTIONS.md with these conventions:

- **§Migration Patterns** — "When creating migrations, add `Index::create()` for
  FK columns. See `migration/m0001200_source_document_fk_indexes.rs`."
- **§Commit Messages** — "Use Conventional Commits format: `type(scope): description`"

And a task with:

```
## Files to Modify
- `src/components/Dashboard.tsx` — add risk score widget
- `src/components/Dashboard.css` — widget styling
```

**Result:**

- **§Migration Patterns** — **excluded**. Convention scope is `.rs` migration files;
  task only modifies `.tsx` and `.css` files. No overlap.
- **§Commit Messages** — **included**. Convention has no file-type restriction
  (broadly applicable). Rationale: "Applies: convention has no file-type restriction
  (broadly applicable)."

## Rules

- Always check applicability before including a convention in Implementation Notes
  or upgrading a suggestion — never apply a convention based on topic match alone
- Conventions without explicit scope are broadly applicable — do not filter them
- The rationale must be included so downstream skills can audit the decision
- When multiple scope signals conflict within a convention section, use the most
  restrictive signal (explicit scope statement > file paths > language syntax)
