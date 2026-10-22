# Library Navigation Standard

Updated: 2026-10-18

## Purpose

This document defines the current public routes and reading navigation for studies and passages.

## Primary Routes

The site-level navigation uses Home, Studies, and Passages.

- Home: `apps/web/index.html`
- Studies: `apps/web/library/index.html`
- Passages: `apps/web/library/passages.html`

The homepage opens with the site's purpose and name, offers a small link to `apps/web/why-we-return-to-the-text.html` for the full site-focused explanation, then places the banner above one Foundations invitation into Study 1, Returning to the Word. The approach page ends with its own invitation into Study 1. The former standalone teaching introduction URL, `apps/web/why-this-site-exists.html`, still redirects to Study 1.

## Studies

`apps/web/library/index.html` is the single canonical Studies page. It opens with `Foundations: A Guided Study` and lists every published study in the 14-step order defined by `GUIDED_STUDY_STEPS` in `tools/generate_study_pages.py`. Returning to the Word is Step 1, The Berean Standard is Step 2, and The Angel of the Lord is Step 6 after the Gospel. A second view, Explore by topic, groups those same 14 studies and lets readers filter by one topic. The guided order is preserved when readers switch back.

Individual studies show their step number near the top and Previous/Continue links after the teaching content. Those links name the destination and explain the next topic. The final step returns to the Studies page. All study navigation opens in the same tab.

Older study entry points remain valid:

- `library/guided-study.html` redirects to `library/index.html`.
- `library/studies-all.html` redirects to `library/index.html?view=topics`.
- `library/browse.html?type=studies` redirects to the topic view.

Topic filtering stays on the Studies page. With the current small catalog, a separate keyword search or featured-studies page is unnecessary.

## Passages

`apps/web/library/passages.html` is the canonical passage reader and the direct destination of the site-level Passages link. There is no featured-passages landing page. The reader keeps its full-width article, sticky Book/Chapter/Passage controls, search, and modal library drawer. The article moves with the page scroll; the drawer scrolls independently while open. Its About these sections guide appears once above the reader as a collapsed disclosure. The introduction identifies the passages as those currently available while the full-Bible library is built.

Older passage entry points remain valid: `library/browse.html?type=passages` redirects to the reader and preserves a selected passage; `library/passages-by-book.html` also redirects to the reader.

Passages are ordered by biblical book and numeric chapter/verse. Previous/next passage links on standalone pages and in the reader follow the complete sequence, independent of filters. The drawer groups available passages by book and chapter, with expand/collapse controls and search. Selection reveals and focuses the destination, positions it below the sticky toolbar, and retains it in the URL.

## Maintenance

Use `python3 tools/generate_study_pages.py --guided-only` to refresh study navigation, the canonical Studies page, and legacy study routes without regenerating authored content. Use `--navigation-only` for passage navigation and the shared passage reader. The normal full generator updates both surfaces after content generation. Validate links, reading order, responsive layout, and preservation of study and passage prose before deployment.
