# Passages Reader Direct Entry

Date: 2026-10-18
Status: Published

## Result

The site-level Passages link now opens `library/passages.html` as the full-width passage reader. The former featured-passages landing page is retired. Readers can choose an available Book, Chapter, and Passage immediately, use search or the existing library drawer, and follow previous/next passage links. The page says that these are the passages currently available.

Old `library/browse.html?type=passages` URLs redirect to the reader and preserve the selected `passage` query parameter. `library/passages-by-book.html` redirects there too. Old shared-browse study URLs continue to open the Studies topic view.

## Scope

The passage-library generator now writes the canonical reader and legacy redirects during `--navigation-only` refreshes. The twelve earlier featured-card notes remain available for their individual passage introductions. No passage text or source records were added or revised. Full Bible coverage remains active future work in the [passage library foundation plan](../planning/2026-07-05-passage-library-foundation-plan.md).

## Validation and Release

- Python compilation, `tools/check_repo.py`, and `git diff --check` passed. The repository check reported 0 errors and the existing 401 passage-source warnings.
- `--navigation-only` was idempotent across 1,022 output files; all 1,018 passage HTML files matched the pre-change baseline byte for byte.
- Local browser checks covered direct entry, Book and Chapter selection, old-route redirects, desktop and mobile layout, immediate wheel and touch scrolling, drawer isolation and focus, and keyboard search selection.
- Certificate-backed Hosting readiness and dry run passed. Hosting deployed to `the-way-of-scripture`; seven representative live files matched local output byte for byte. A live browser check restored John 8:58 from an old browse URL and changed to Genesis 1:1-31 through the Book selector.

Live route: https://the-way-of-scripture.web.app/library/passages.html
