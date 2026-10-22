# Homepage Start and Full Introduction

Date: 2026-10-18
Status: Superseded by [Introduction Becomes First Study](2026-10-18-introduction-becomes-first-study.md)

## Result

The homepage is now a short starting point. Its first panel explains the site's purpose, offers a primary action into the first guided study, and links to the full introduction. A three-step explanation shows how to continue through the 13 studies and use Passages as a reference. The guided-study invitation appears again at the end. The banner remains but follows the first action, so it does not delay the next step on smaller screens.

The original homepage introduction is preserved at `apps/web/why-this-site-exists.html`. Its eight prose sections, translation note, Scripture quotations, and feedback text remain intact, now presented as one continuous article. An orientation note at the top explains how to read it, and a final action leads directly into The Berean Standard.

## Validation and Release

- Compared the eight original narrative sections and feedback block against the previous homepage: their content was preserved.
- Checked the homepage and introduction in desktop and mobile browsers, including the first action, ending action, article structure, and horizontal overflow.
- Audited all links and assets on both new pages; none were missing. `tools/check_repo.py` passed with 0 errors and the existing 401 passage-source warnings; `git diff --check` passed.
- On CozPlex, certificate-backed `the-way-of-scripture` project and Firebase app reads passed, followed by a Hosting dry run and live deployment. Five representative live files matched local output byte for byte. Live browser navigation from Home to the introduction and its Step 1 destination passed.

Live pages: https://the-way-of-scripture.web.app/ and https://the-way-of-scripture.web.app/why-this-site-exists.html
