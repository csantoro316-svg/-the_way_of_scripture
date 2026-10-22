# Full Site Purpose on the Homepage

Date: 2026-10-18
Status: Published

## Result

The homepage now opens with the site's original statement of purpose and the meaning of The Way, followed by the Jesus banner. Its site-focused text covers the authority of the original Scriptures, reading in context, the Berean standard, the choice of the BSB, what the site examines, why that matters, and the site's openness to correction. The original Garden and translation-history teaching examples remain in Study 1. A final transition explains why the Foundations guided studies were developed and retains one direct Study 1 button.

This intentionally full draft lets the owner review all of the site's original purpose material before deciding what to streamline.

## Verification and Release

- Desktop and mobile browser checks confirmed the reading flow, image load, headings, one Study 1 button, and no horizontal overflow at 390px. The button opened Returning to the Word.
- The local homepage link audit found no missing links or duplicate IDs. `tools/check_repo.py` passed with 0 errors and the existing 401 passage warnings; `git diff --check` passed.
- CozPlex certificate-backed Scripture project and Firebase app-list readiness checks passed. Hosting dry run and live deployment passed for the explicit `the-way-of-scripture` project.
- Live homepage, CSS, Study 1, and Studies page matched local bytes and returned `Cache-Control: no-cache`. A live browser confirmed the final section order and single start action.

Live homepage: https://the-way-of-scripture.web.app/
