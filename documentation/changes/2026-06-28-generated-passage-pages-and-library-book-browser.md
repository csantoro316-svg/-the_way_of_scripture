# Generated Passage Pages And Library Book Browser

Date: 2026-06-28
Scope: website

## Summary

- Added automatic passage-page generation from study references.
- Generated passage pages under `apps/web/passages/`.
- Added a book-grouped passage browser at `apps/web/library/passages-by-book.html`.
- Added expand-all and collapse-all behavior for the book-grouped passage browser.
- Updated study rendering so Scripture references now link outward to generated passage pages.
- Added reciprocal passage-side related study links based on study usage.

## Why

- The documented content model requires reciprocal study-to-passage and passage-to-study relationships.
- The library needed a first implementation of the passages browsing model so content navigation no longer stopped at studies alone.
- Passage browsing by biblical book scales better than a flat list of references.

## Notes

- Current passage pages are generated reference scaffolds, not final full exegesis pages.
- Passage pages currently focus on navigation, reciprocal study links, and translation-policy framing.
- The next layer can add fuller passage metadata, translation text handling, and richer context blocks.
