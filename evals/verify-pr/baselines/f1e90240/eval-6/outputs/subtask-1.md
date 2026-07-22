## Repository
sdlc-plugins

## Target Branch
main

## Description
Add a Markdown-specific documentation rule to Check 6 (Documentation Coverage) in the style-conventions sub-agent. Currently Check 6 unconditionally skips Markdown files ("Markdown: not applicable -- skip Markdown files"), but this repository is documentation-heavy with skills defined in Markdown. The check should verify that new Markdown section headings (`###` and below) have at least one paragraph of introductory explanatory text before any sub-sections or code blocks.

## Files to Modify
- `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` -- update Check 6 section 6b to replace the "Markdown: not applicable" rule with a Markdown-specific documentation rule that checks for introductory text after new section headings

## Implementation Notes
- In section "6b -- Check Documentation Comments", replace the Markdown bullet:
  - Current: `- **Markdown:** not applicable -- skip Markdown files`
  - New: Add a rule that for Markdown files, checks whether new `###` (or deeper) headings have at least one paragraph of explanatory text before any sub-sections or code blocks
- Follow the structure of the other language-specific rules in 6b (Rust, TypeScript/Java, Python, Go)
- The rule should only apply to new headings introduced in the PR diff (lines with `+` prefix), not existing headings
- CONVENTIONS.md documents: "This is a documentation-heavy repository -- skills are defined in Markdown (SKILL.md files) rather than traditional programming languages" -- this confirms Markdown should receive documentation coverage attention

## Acceptance Criteria
- [ ] Check 6 section 6b includes a Markdown-specific documentation rule
- [ ] The Markdown rule checks that new section headings have introductory explanatory text
- [ ] The Markdown rule does not flag headings that already have explanatory text
- [ ] The "not applicable -- skip Markdown files" exclusion is removed

## Review Context
**Original review comment (comment 50001 on PR #747):**

> The Check 6 description says 'Markdown: not applicable -- skip Markdown files' but this is a documentation-heavy repository where skills are defined in Markdown. The check should still verify that new Markdown sections have introductory text explaining their purpose, even if traditional doc comments don't apply. Consider adding a Markdown-specific rule that checks whether new `###` headings have at least one paragraph of explanatory text before any sub-sections or code blocks.

**File:** `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md`, line 310

## Target PR
https://github.com/mrizzi/sdlc-plugins/pull/747
