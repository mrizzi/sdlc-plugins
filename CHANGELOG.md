# Changelog

All notable changes to the sdlc-workflow plugin are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Contributors ladder with CONTRIBUTING.md, CODEOWNERS, and GitHub Issue templates (TC-5072)

## [0.12.2] - 2026-07-03

### Fixed

- Non-plannable requirement flagging added to impact map step in `plan-feature`
- Direct dependency requirement clarified for create-branch bookend in `plan-feature`
- Eval assertions rewritten for file-based evidence in `plan-feature`

## [0.12.1] - 2026-07-02

### Added

- Documentation task generation from Feature description signals in `plan-feature`
- Testing task generation from readiness template in `plan-feature`

### Fixed

- Documentation tasks exempted from template and dependency assertions in `plan-feature`

## [0.12.0] - 2026-07-02

### Added

- Epic creation and grouping strategies with configurable hierarchy preferences in `plan-feature` (TC-4869)
- Parent issue linking step in `plan-feature` (TC-4870)
- Early assignment and Assigned transition at Step 0.7 in `triage-security` (TC-5008)
- Cross-CVE traceability links and comments at Step 4.3 in `triage-security` (TC-5009)

### Fixed

- Traceability links created at identification time instead of after confirmation in `triage-security` (TC-5009)

## [0.11.1] - 2026-07-01

### Added

- Deployment context classification for remediation tasks in `triage-security`
- Concurrent triage detection before remediation task creation in `triage-security`
- Staleness detection for `security-matrix.md` in `triage-security`
- Embargo warning gate for high-severity CVEs in `triage-security`
- Optional SBOM-based base image verification via cosign in `triage-security`
- Ready for QA discovery category with remediation task completion check in `triage-security`
- ProdSec contact config and vulnerability creator @mention in `triage-security`
- Description digest comment on remediation task creation in `triage-security`
- External CVE data enrichment from MITRE and OSV.dev in `triage-security`
- Proactive cross-stream remediation with `security-preemptive` label in `triage-security`
- Cross-CVE overlap detection via Upstream Affected Component in `triage-security`
- `get_remote_links` command in `jira-client`
- Priority and `fixVersion` REST API fallback in `jira-client`
- Priority and `fixVersion` inheritance in `plan-feature` task creation
- Priority and `fixVersion` prompts in `define-feature`
- Dynamic issue type discovery and hierarchy mapping in `plan-feature`
- Jira Field Defaults configuration step in `setup`
- Bug and Hierarchy configuration in `setup`
- Hierarchy preferences step and configuration contract in `setup`
- Priority and `fixVersion` field handling constraints

### Changed

- Cross-CVE overlap fields made configurable via `/setup` in `triage-security`
- Unsupported ecosystem message generalized to use placeholder in `triage-security`

### Fixed

- Step numbering consistency (7.0/7 → 7/8) in `triage-security`
- SBOM verification output line made mandatory for RPM packages in `triage-security`
- Created column added to Ready for QA table template in `triage-security`
- `get_remote_links` guarded against non-dict responses in `jira-client`
- ADF `taskList`/`taskItem` node sanitization to prevent `INVALID_INPUT` errors in `jira-client`
- Field handling and test review feedback addressed in `jira-client`
- Feature-branch label included in workflow mode decision output in `plan-feature`
- Convention enrichment completeness check and verification pass in `plan-feature`
- Baseline comparison gate added to eval failure subtask creation in `verify-pr`
- Idempotent sibling link check documented in `triage-security` Step 4.2

## [0.11.0] - 2026-06-19

### Added

- `report-bug` skill for structured bug reporting with Jira issue creation
- `triage-bug` skill for bug lifecycle pipeline triage
- Bug Configuration scaffolding step in `setup` skill
- Bug description template scaffold
- Bug lifecycle pipeline documentation and constraints
- Eval infrastructure for `report-bug` and `triage-bug` skills

### Changed

- Improved `triage-bug` skill discoverability and navigation

### Fixed

- `triage-bug` digest comment exempted from Comment Footnote rule
- `triage-bug` eval assertion for `ai-generated-jira` label
- `report-bug` programmatic input format and composed output examples
- Bug lifecycle docs heading levels aligned with feature phases
- Corrected `report-bug` constraint source reference

## [0.10.0] - 2026-06-15

### Added

- `triage-security` skill for version-aware CVE triage with Jira sub-task creation and security matrix integration
- Security Configuration step in `setup` skill for local security-matrix scaffolding
- Security matrix template (`security-matrix.md`) for Konflux repositories
- Triage-security architectural constraints and guardrails
- Eval infrastructure for `triage-security` with discovery mode and RPM ecosystem test cases

### Changed

- `triage-security` Step 2.1 matrix loading now prefers local files with Konflux API fallback
- Applied progressive disclosure to `triage-security` SKILL.md for improved readability

### Fixed

- `verify-pr` now classifies review body suggestions alongside inline comments
- Corrected traceability index constraint references in `triage-security`
- Aligned Vulnerability issue type ID field name with project config contract in `triage-security`

## [0.9.2] - 2026-06-03

### Added

- Description digest protocol for cross-phase integrity verification in `plan-feature` and `implement-task`
- Convention applicability rules with file-type scoping for convention upgrades in `plan-feature` and `verify-pr`
- Eval-aware Test Quality integration with autonomous eval failure sub-task creation in `verify-pr`
- Description digest verification step in `implement-task`
- Documentation scope preservation check in `implement-task`
- Eval infrastructure change detection in `verify-pr` correctness check
- Failure evidence rendering in `run-evals` summary output
- Cross-phase integrity and convention applicability constraints

### Fixed

- Standardized digest computation on ADF JSON with format-tagged digests for access-method-agnostic verification
- Multiple digest comment handling disambiguation in `implement-task`
- Convention applicability format enforcement and self-verification guards in `plan-feature`
- Issue link direction for Incorporates and Depend in `plan-feature`
- Digest protocol inlined in SKILL.md to fix eval regression
- CI reporting success when no evals need to run
- HTML special character escaping in eval failure evidence output

## [0.9.1] - 2026-05-20

### Fixed

- Resolved CONVENTIONS.md lookup to use Repository Registry Path instead of hardcoded path
- Hard stop on CI check failure before commit in `implement-task`

## [0.9.0] - 2026-05-14

### Added

- Feature-branch workflow mode with automatic bookend task generation in `plan-feature`
- Target Branch support and bookend handling in `implement-task`
- Target Branch and Bookend Type sections in the task description template
- Feature-branch workflow constraints and documentation
- Fork PR eval dispatch CI workflow for cross-fork eval runs
- Commit status reporting for eval PR visibility

### Changed

- Migrated eval CI workflows to direct Workload Identity Federation
- Hardened eval dispatch against artifact poisoning and injection

### Fixed

- Resolved stale pending commit status when eval discover fails
- Fork PR resolution via `pulls.list` with pagination

### Documentation

- Excluded eval baselines from changelog scope

## [0.8.2] - 2026-04-29

### Changed

- Added skill name to eval result summary headings for clearer multi-skill output

### Added

- Eval baselines for latest skill changes

## [0.8.1] - 2026-04-29

### Changed

- Added external API claim verification to define-feature section collection
- Extracted eval coverage propagation into shared resource

### Added

- Eval coverage for external API claim verification in define-feature

## [0.8.0] - 2026-04-28

### Changed

- Rewrote `verify-pr` as a parallel sub-agent orchestrator with dedicated dispatch and finding templates
- Added intent alignment sub-agent skill file
- Added security sub-agent skill file
- Added correctness sub-agent skill file
- Added style/conventions sub-agent skill file

### Fixed

- CI: restored idempotent upsert for eval PR reviews
- CI: post eval results as PR review instead of issue comment
- Evals: stabilized assertions for stochastic behavior and sub-agent observable outputs

### Documentation

- Added verify-pr decomposition design spec
- Re-scoped verify-pr constraints for sub-agent decomposition
- Added policy mapping for autonomous skill execution with fullsend ADR references

## [0.7.2] - 2026-04-24

### Added

- Eval suite for `setup` skill
- Eval suite for `define-feature` skill
- Eval coverage for test change classification in `verify-pr`

### Changed

- Added additive-vs-reductive test change detection to verify-pr Step 12
- Added eval coverage detection to plan-feature task generation
- Added eval coverage currency check to implement-task Step 9

### Documentation

- Added test change classification constraints §1.18-§1.21

## [0.7.1] - 2026-04-23

### Added

- Eval suite for `implement-task` skill
- Eval suite for `verify-pr` skill

### Changed

- Added cross-section reference consistency check to implement-task Step 9
- Strengthened implement-task §1.6 to explicitly stop on incomplete input

### Fixed

- Eval fixture corrections: Axum framework syntax alignment, service file path, model wiring file
- CI: guard git pull --rebase against set -e abort
- CI: add pull-rebase retry loop to eval-baseline push

### Documentation

- Added framework syntax alignment convention for eval fixtures

## [0.7.0] - 2026-04-22

### Added

- `run-evals` skill for running skill evals with deterministic output layout and CI-compatible results
- `eval-pr` GitHub Actions workflow for PR-triggered eval comparisons against baselines
- `eval-baseline` GitHub Actions workflow for push-to-main baseline generation
- Plan-feature eval fixtures with cross-skill handoff contract validation assertions
- Feedback.json tracking in eval baselines for human review

### Changed

- Added convention gap task structuring guidance to verify-pr Step 5b
- Moved eval fixtures outside plugin distribution path

### Fixed

- Replaced dangerously-skip-permissions with dontAsk mode in eval workflows
- Various eval CI fixes (Vertex AI auth, plugin installation, verbose output, prompt qualification)

### Documentation

- Added skill evaluation framework design spec
- Added eval usage guide for plan-feature
- Added eval skills CI workflow design spec
- Added eval fixture annotation conventions

## [0.6.1] - 2026-04-14

### Fixed

- Fixed script execution context for jira-client.py — all examples now `cd` to plugin root before running the script, since it lives in the plugin cache, not the working directory

## [0.6.0] - 2026-04-14

### Changed

- Added test doc comment check to verify-pr Step 12
- Added REST API v3 fallback for Jira when MCP is unavailable
- Updated Jira client description format
- Added .env file support for credential management
- Refactored Jira client to accept args directly instead of using subprocess

### Fixed

- Handle code blocks with blank lines and validate JSON input in Jira client

### Documentation

- Added CONVENTIONS.md to document project coding standards

Thanks to @mrrajan for his contributions to this release!

## [0.5.11] - 2026-04-08

### Changed

- Added CONVENTIONS.md CI check verification to implement-task Step 9
- Added test documentation guidance with given-when-then structure to implement-task
- Added test quality check for repetitive test functions to verify-pr
- Added parameterized test preference guidance to implement-task
- Added untracked file check to implement-task self-verification

## [0.5.10] - 2026-04-03

### Changed

- Added example consistency check to implement-task self-verification
- Added display text vs API value comparison guidance for Figma analysis in plan-feature
- Added data component rendering scope extraction from Figma context hierarchy in plan-feature
- Added list endpoint sort order verification to implement-task cross-repo API checks

### Fixed

- Corrected inconsistent example mapping in plan-feature display text comparison

## [0.5.9] - 2026-04-03

### Changed

- Added custom sub-component visual spec extraction guidance to plan-feature

## [0.5.8] - 2026-04-02

### Changed

- Added cross-module shared entity analysis to implement-task sibling parity
- Added cross-repo API contract verification for manual REST calls

## [0.5.7] - 2026-04-01

### Changed

- Added method-vs-fact secondary test to verify-pr root-cause universality gate
- Added code quality and test assertion guidance to implement-task

Thanks to @ruromero for his contributions to this release!

## [0.5.6] - 2026-04-01

### Changed

- Added caller-site parity check to implement-task sibling parity analysis
- Updated verify-pr workflow diagram with root-cause task

## [0.5.5] - 2026-03-27

### Changed

- Extended verify-pr CI status step with failure analysis, fix sub-task creation, and root-cause investigation integration

## [0.5.4] - 2026-03-27

### Changed

- Added universality-test classification gate to verify-pr root-cause investigation, preventing skill drift from repo-specific patterns
- Added test convention analysis to implement-task Step 4, discovering sibling test patterns for use during test writing

## [0.5.3] - 2026-03-27

### Changed

- Enforced mandatory thread enumeration on every verify-pr run to prevent missed review comments
- Used structured task description template for root-cause tasks in verify-pr, with analysis posted as Jira comment
- Added convention-aware task enrichment to plan-feature Step 5

### Fixed

- Prefixed classification markers with skill name to avoid false positives from human reviewers

## [0.5.2] - 2026-03-26

### Changed

- Added convention check before classifying review feedback in verify-pr
- Reply to all review comments and use per-run GitHub comments in verify-pr

## [0.5.1] - 2026-03-26

### Changed

- Added review feedback resolution and full-chain root-cause investigation to verify-pr
- Added contract and sibling parity self-verification check to implement-task

### Documentation

- Added missing define-feature skill to README

## [0.5.0] - 2026-03-25

### Added

- `define-feature` skill for interactive Feature creation with guided template walkthrough

## [0.4.5] - 2026-03-25

### Changed

- Added data-flow trace self-verification check to implement-task

## [0.4.4] - 2026-03-25

### Changed

- Added convention conformance analysis guardrail to implement-task

### Fixed

- Used gh pr comment --edit-last for idempotent report posting in verify-pr
- Added --jq to commit traceability and CI refresh for revised reports in verify-pr

## [0.4.3] - 2026-03-24

### Changed

- Added conditional PR branch checkout to verify-pr skill
- Added systematic duplication-risk scan and Reuse Candidates section to plan-feature

### Fixed

- Replaced invalid --stat flag with gh api for diff size check in verify-pr

### Documentation

- Updated README with all four skills, complete doc index, and setup step
- Added Mermaid diagram, expanded Verify Phase, and restructured Setup in workflow docs

## [0.4.2] - 2026-03-23

### Changed

- Added documentation-impact evaluation to planning and implementation skills
- Enforced DRY principle across planning and implementation skills
- Added GitHub Issue custom field to setup skill and project configuration
- Added GitHub issue Closes reference to PR description
- Added Markdown link for Jira issue in PR description

## [0.4.1] - 2026-03-23

### Fixed

- Use inlineCard ADF node for Git Pull Request custom field

## [0.4.0] - 2026-03-20

### Added

- `verify-pr` skill for PR verification against Jira tasks

### Changed

- Added CONVENTIONS.md fill-in prompt to setup skill

### Fixed

- Added markdown footnote to verify-pr GitHub PR comment

### Documentation

- Added version bump decision guide with y-stream vs z-stream criteria

## [0.3.2] - 2026-03-20

### Changed

- Enhanced comment footer with plugin link, skill name, and version
- Added loop detection guidance to implement-task skill
- Added CONVENTIONS.md lookup to plan-feature, implement-task, and setup skills

### Documentation

- Added GitHub release creation step to releasing guide

## [0.3.1] - 2026-03-20

### Changed

- Enhanced `/setup` skill to ship a `constraints.md` template
- Enhanced `/plan-feature` with constraint-aware task generation
- Clarified PR link fallback in `/implement-task` when custom field is not configured

### Documentation

- Added workflow, tools, and conventions documentation
- Added documentation table of contents to CLAUDE.md
- Added PR description format to conventions-spec
- Added release process and changelog entries for v0.2.0 and v0.2.2

## [0.3.0] - 2025-03-20

### Added

- `/setup` skill for project configuration validation
- Project config template and reference documentation

### Changed

- Bumped version to 0.3.0

## [0.2.4] - 2025-03-19

### Added

- Self-verification step in implement-task before commit
- Verification Commands section in plan-feature task template
- Metrics definitions for AI-assisted SDLC workflow
- Architectural constraints document

## [0.2.3] - 2025-03-18

### Added

- Assign-to-me on task start in implement-task

### Fixed

- Removed hardcoded Git Pull Request custom field ID from implement-task

## [0.2.2] - 2025-03-17

### Added

- GitHub Actions workflow for plugin validation
- CLAUDE.md with version sync instructions

### Fixed

- Added version and author fields to plugin manifest
- Updated Git Pull Request custom field ID to customfield_10875
- Removed smoke-test job that requires authentication
- Fixed version reference and marketplace add command in README
- Removed invalid skills array from plugin manifest

## [0.2.1] - 2025-03-17

### Fixed

- Added missing description field to skill entries

## [0.2.0] - 2025-03-16

### Changed

- Genericized skill files to use project configuration contract references

## [0.1.0] - 2025-03-16

### Added

- Initial release of the sdlc-workflow plugin
- `plan-feature` skill — generate implementation plans and Jira tasks from a feature
- `implement-task` skill — implement Jira tasks with structured descriptions
- Plugin marketplace repository structure
- Project configuration contract documentation
- SDLC methodology documentation
- README with installation guide
