## Repository
sdlc-plugins

## Target Branch
TC-9106

## Description
Add a Markdown-specific documentation coverage rule to Check 6 in the style-conventions sub-agent. The current implementation skips Markdown files entirely ("Markdown: not applicable -- skip Markdown files"), but since this is a documentation-heavy repository where skills are defined in Markdown, the check should verify that new Markdown sections have introductory explanatory text. Specifically, when new `###` headings are introduced in a PR, verify that each heading has at least one paragraph of explanatory text before any sub-sections or code blocks.

## Files to Modify
- `plugins/sdlc-workflow/skills/verify-pr/style-conventions.md` -- replace the "Markdown: not applicable" rule in Check 6b with a Markdown-specific rule that checks new headings for introductory text

## Implementation Notes
- In section "6b -- Check Documentation Comments", the current Markdown entry reads: "**Markdown:** not applicable -- skip Markdown files"
- Replace this with a rule that checks whether new `###` headings (identified in the diff with `+` prefix) have at least one paragraph of explanatory text before any sub-sections or code blocks
- Follow the structure of the existing language-specific rules in 6b (Rust, TypeScript/Java, Python, Go)
- The Markdown rule should specify what constitutes "introductory text" -- at least one non-empty paragraph (not a heading, not a code block) between the heading and any sub-sections or code blocks
- This change aligns with the repository's documentation-heavy nature where skills are defined in Markdown files

## Acceptance Criteria
- [ ] Check 6b includes a Markdown-specific rule for documentation coverage
- [ ] The Markdown rule checks that new `###` headings have at least one paragraph of explanatory text
- [ ] The rule specifies that explanatory text must appear before any sub-sections or code blocks
- [ ] The Markdown rule replaces the previous "not applicable -- skip Markdown files" entry

## Test Requirements
- [ ] Verify the Markdown rule correctly identifies new headings lacking introductory text
- [ ] Verify the Markdown rule does not flag headings that already have explanatory text
- [ ] Verify the rule applies only to new headings (those with `+` prefix in the diff)

## Target PR
https://github.com/mrizzi/sdlc-plugins/pull/747

## Review Context
**Comment ID:** 50001
**Author:** reviewer-b
**File:** plugins/sdlc-workflow/skills/verify-pr/style-conventions.md, line 310

**Original comment:**
> The Check 6 description says 'Markdown: not applicable — skip Markdown files' but this is a documentation-heavy repository where skills are defined in Markdown. The check should still verify that new Markdown sections have introductory text explaining their purpose, even if traditional doc comments don't apply. Consider adding a Markdown-specific rule that checks whether new `###` headings have at least one paragraph of explanatory text before any sub-sections or code blocks.
