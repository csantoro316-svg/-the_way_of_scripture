# Introduction Becomes the First Study

Date: 2026-10-18
Status: Published

## Result

The former standalone introduction is now **Returning to the Word**, Study 1 of the 14-study Foundations path. It explains why Scripture's wording and context matter, beginning in Genesis and continuing through translation, inherited interpretation, and the need to examine the text. The Berean Standard is Study 2 and develops the method of testing teachings against Scripture. The homepage and Studies page start at Study 1; the former `why-this-site-exists.html` URL redirects there.

The new canonical source is `content/studies/returning_to_the_word.md`, reconciled from the published introduction instead of the older, drifted `way_of_scripture_intro.md`. The new study preserves the original introduction's eight main topics, quotations, and arguments. Its Scripture references link to available passage pages, and ten canonical passage pages and reader entries now link back to the study. Existing study prose was preserved; only guided navigation changed on the prior 13 pages.

## Verification and Release

- `--guided-only` and `--navigation-only` were jointly idempotent across 1,035 generated pages and index files. All prior study prose remained unchanged, and only the ten cited passage pages changed relative to the saved passage baseline.
- Local link audit, Python compilation, `tools/check_repo.py`, and `git diff --check` passed. Passage validation reported 0 errors and the existing 401 warnings.
- Local and live browsers confirmed the 14-study order, topic view, Step 1 → Step 2 navigation, legacy introduction redirect, mobile layout, and passage backlink.
- CozPlex certificate-backed project/app readiness, Hosting dry run, and deployment passed. Representative live pages, CSS, and library index matched local bytes.
- Hosting now sends `Cache-Control: no-cache` for HTML, the homepage route, the library index, and CSS. The live headers were verified; images retain their existing cache lifetime. This follows [Firebase Hosting's cache guidance](https://firebase.google.com/docs/hosting/manage-cache).

Live Study 1: https://the-way-of-scripture.web.app/studies/returning-to-the-word.html
