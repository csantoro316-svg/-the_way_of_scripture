# Homepage Simplification

Date: 2026-10-18
Status: Published

## Result

The homepage places the existing Jesus banner directly beneath the site navigation. A short introduction explains why the site returns to Scripture's words, context, and original languages. The page then offers one Foundations invitation to begin Study 1, with a secondary link to view the full 14-study path. The former numbered how-to section and duplicate start action were removed.

The first study, Returning to the Word, continues to carry the full introduction. Study and passage routes remain unchanged.

## Verification and Release

- Desktop and mobile browser checks confirmed the section order, readable layout, and no horizontal overflow at 390px. The single Study 1 button opened Returning to the Word.
- `tools/check_repo.py` passed with 0 errors and the existing 401 passage warnings; `git diff --check` passed.
- CozPlex certificate-backed Scripture project and Firebase app-list readiness checks passed. Hosting dry run and live deployment passed for `the-way-of-scripture`.
- Live homepage, CSS, Study 1, and Studies page matched local bytes and returned `Cache-Control: no-cache`. The live browser confirmed banner → introduction → Foundations, one Study 1 link, and no how-to section.

Live homepage: https://the-way-of-scripture.web.app/
