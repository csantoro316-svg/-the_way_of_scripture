# Passage Navigation and Prayer Source Reconciliation

Date: 2026-10-18
Host: CozPlex
Project: `the-way-of-scripture`
Scope: website navigation, study source continuity, and Hosting release

## Changes

- Added previous/next navigation after Deeper Study on all 970 library passage pages and inside Browse Library. Links show the destination reference and its section title when available, and stack on mobile.
- Ordered the complete library by canonical book, numeric chapter/verse start, then range end. Navigation crosses book boundaries, omits the unavailable direction at either endpoint, and stays independent of alphabetical views and filters. Existing noncanonical references remain after the canonical books.
- Browse Library navigation expands and highlights the destination, clears filters and search results so it can be seen, moves focus and scrolling to the passage heading, and retains the selected passage in the URL. Ordinary clicks stay in the browse view; modified clicks retain normal link behavior.
- Reconciled the eight revised paragraphs under “Does God Want You to Ask?” in `content/studies/prayer_and_faith.md` with the authored HTML saved in commit `0cbe06d`, preserving their wording verbatim.
- Added `python3 tools/generate_study_pages.py --navigation-only`. It refreshes navigation, library ordering, and the browse template while preserving existing study HTML, passage prose, source JSON records, and the translation audit. Normal generation also refreshes navigation.
- Updated the content execution standard and resume/headless runbooks with the current behavior and resolved source mismatch.

## Verification

- Active-host certificate checks passed on CozPlex: project describe returned exactly `the-way-of-scripture`; Firebase app-list returned `status: success` with an empty list.
- `python3 tools/check_repo.py` passed with 0 errors and the existing 401 passage warnings.
- Checked all 970 passage pages against their Git baseline: removing the added navigation reproduces each original file exactly. Every previous/next destination exists, the sequence is reciprocal, endpoints omit the absent link, and insertion is idempotent. Library payload content is unchanged apart from ordering.
- Confirmed the reconciled Markdown renders the eight saved Prayer and Faith paragraphs verbatim and its existing HTML is unchanged locally.
- Browser checks passed for numeric chapter progression (Genesis 9 → 10), reverse navigation, Genesis → Exodus across books, alphabetical browsing, filters/search, highlighted visible destinations, focus/scrolling, URL selection restoration, cross-chapter references, and both endpoints.
- Inspected desktop (1440 px) and mobile (390 px) navigation. Mobile links stack without horizontal overflow. A real click on a standalone page loaded the expected next passage with a reciprocal previous link.
- `git diff --check` passed.

## Deployment

Both commands passed through CozPlex's host-local certificate wrapper with explicit Scripture project selection:

```bash
~/.local/bin/mg-cloud-firebase deploy --only hosting --project the-way-of-scripture --dry-run
~/.local/bin/mg-cloud-firebase deploy --only hosting --project the-way-of-scripture
```

Firebase finalized and released the Hosting version successfully (1,045 files in `apps/web`, 974 uploaded files). The release is live at `https://the-way-of-scripture.web.app`.

After release, fetched Prayer and Faith, Browse Library, the library index, stylesheet, and representative passage pages (including an endpoint) and confirmed their bytes match the verified local files. A browser check on live Browse Library restored the selected Genesis 9 passage from the URL and navigated to Genesis 10 with the correct visible highlight and focus. The live Prayer and Faith page now contains the saved job example and surrender discussion.

## Remaining Work

The generator's legacy LSB defaults and translation audit still need alignment with the master BSB standard, and the passage-library foundation/schema work remains open. Full content regeneration was deliberately avoided for this change; no passage translations or theological interpretations were edited.
