# Study Page Generation Foundation

Date: 2026-06-28
Scope: website

## Summary

- Added a repeatable study-page generator at `tools/generate_study_pages.py`.
- Generated the first study library pages under `apps/web/studies/`.
- Added a study index page and individual study pages for:
  - `prayer_and_faith.md`
  - `what_does_prayer_look_like.md`
- Wired the homepage into the study library.
- Updated the content execution standard to make reciprocal study-to-passage and passage-to-study relationships explicit.

## Why

- The site needed a content-page system comparable to the knowledge-base workflow rather than one-off hand-authored pages.
- Study markdown files now have a direct path into the website as browsable pages.
- The reciprocal linking rule needed to be documented before passage-page generation begins in earnest.

## Notes

- Passage pages are not yet generated in this slice.
- The documented rule now requires passage pages to link back to all studies that reference them, and study pages to link outward to their referenced passages when that layer is built.
