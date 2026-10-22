# Homepage Approach Link

Date: 2026-10-18
Status: Published

## Result

The homepage introduction now ends with a small link, `What changes when we go back to the text?`, to a dedicated `Why We Return to the Text` page. The Jesus banner and single Foundations invitation follow immediately on the homepage. The new page carries the six site-focused sections previously displayed on Home and ends with a Study 1 invitation. The former teaching-introduction URL continues to redirect to Study 1.

## Verification and Release

- Local desktop and mobile browser checks confirmed the homepage flow, the quiet approach link, six sections on the new page, working navigation into Study 1, and no horizontal overflow at 390px.
- Both pages passed a local link/asset and duplicate-ID audit. `tools/check_repo.py` passed with 0 errors and the existing 401 passage warnings; `git diff --check` passed.
- CozPlex certificate-backed Scripture project and Firebase app-list readiness checks passed. Hosting dry run and live deployment passed for `the-way-of-scripture`.
- Live homepage, approach page, CSS, and Study 1 matched local bytes and returned `Cache-Control: no-cache`. A live browser followed the homepage link to the new page and confirmed the six sections and Study 1 destination.

Live pages: https://the-way-of-scripture.web.app/ and https://the-way-of-scripture.web.app/why-we-return-to-the-text.html
