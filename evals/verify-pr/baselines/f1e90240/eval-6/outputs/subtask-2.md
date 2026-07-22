## Repository
sdlc-plugins

## Target Branch
main

## Description
Document Markdown documentation standards in CONVENTIONS.md. The existing CONVENTIONS.md notes that this is a "documentation-heavy repository" with "skills defined in Markdown," but does not specify what documentation standards apply to Markdown content (e.g., section headings should have introductory explanatory text). This gap caused Check 6 (Documentation Coverage) to unconditionally skip Markdown files, missing a reviewer-flagged defect.

Add a convention section that defines Markdown documentation standards for skill definition files, so that future tooling (including verify-pr Check 6) and implementers know what documentation quality expectations apply to Markdown sections.

## Files to Modify
- `CONVENTIONS.md` -- add a Markdown documentation standards section under an appropriate heading (e.g., within Code Style or Documentation) that specifies: (1) new section headings in skill files must have introductory explanatory text before sub-sections or code blocks; (2) canonical searchable markers or patterns that tooling can use to verify compliance

## Implementation Notes
- Place the new convention near the existing "Markdown: Use GitHub-flavored Markdown for all documentation" bullet in the Code Style section, or create a dedicated subsection under Documentation
- The convention should be prescriptive enough for automated checking: define what constitutes "introductory explanatory text" (at least one non-empty paragraph between a heading and any sub-heading or code fence)
- Reference the existing CONVENTIONS.md statement: "No source code: This is a documentation-heavy repository -- skills are defined in Markdown (SKILL.md files) rather than traditional programming languages"
- This convention applies specifically to `SKILL.md` files and sub-agent instruction files (e.g., `style-conventions.md`, `intent-alignment.md`)

## Acceptance Criteria
- [ ] CONVENTIONS.md includes a Markdown documentation standard for skill definition files
- [ ] The standard specifies that new section headings must have introductory explanatory text
- [ ] The standard defines what constitutes adequate introductory text (at least one paragraph before sub-sections or code blocks)
- [ ] The standard is placed in a logical location within the existing CONVENTIONS.md structure
