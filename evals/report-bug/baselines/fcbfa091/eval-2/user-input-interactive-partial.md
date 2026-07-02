<!-- SYNTHETIC TEST DATA — user input with only Required sections, all Optional sections skipped -->

# User Input: Partial Bug Report (Interactive)

Only Required sections are provided. All Optional sections are
explicitly marked as SKIP to test that skipped sections are omitted
from the output rather than appearing as empty headings.

**Bug Summary**: Search results pagination returns duplicate entries

---

## Description

When paginating through search results on the SBOM list page, some
entries appear on both the current and next page. This happens
consistently when sorting by creation date descending. Approximately
10-15% of entries are duplicated across page boundaries.

## Steps to reproduce

1. Ingest at least 50 SBOMs into the system
2. Navigate to the SBOM list page
3. Set sort order to "Created Date (Newest First)"
4. Scroll through pages using the pagination controls
5. Compare entries on page 2 with entries on page 1

## Expected Result

Each SBOM appears exactly once across all pages. No duplicates when
paginating through the full result set.

## Actual Result

Several SBOMs that appeared at the bottom of page 1 also appear at
the top of page 2. The total count shown in the pagination footer
is correct, but the actual displayed items exceed this count due to
duplicates.

## Attachments

None — the issue is reproducible with any dataset of 50+ SBOMs.

## Root Cause

SKIP

## Suggested Fix

SKIP
