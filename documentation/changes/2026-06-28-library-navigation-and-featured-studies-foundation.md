# Library Navigation And Featured Studies Foundation

Date: 2026-06-28
Scope: website

## Summary

- Added a shared library navigation surface under `apps/web/library/`.
- Created:
  - `apps/web/library/index.html` as the main studies-facing library landing page
  - `apps/web/library/studies-all.html` as the exhaustive study list
- Updated the study generator to:
  - keep study content pages under `apps/web/studies/`
  - route library browsing through the new `library/` area
  - redirect `apps/web/studies/index.html` to the shared library
- Updated the homepage to link into the library rather than exposing a growing inline study list.
- Documented the rule that the studies-facing library landing page should surface up to 6 featured studies.

## Why

- The earlier study index pattern would not scale well as the study count grows.
- The site needed one clear navigation home for content browsing while still preserving separate study and passage content pages.
- The featured-vs-browse-all split gives the studies area a curated landing experience without losing access to the full corpus.

## Notes

- Passage browsing is not yet implemented in the library surface.
- The documented next direction remains passage browsing by biblical book with expand and collapse behavior.
