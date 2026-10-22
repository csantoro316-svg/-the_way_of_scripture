# First Genesis Editorial Batch

Date: 2026-10-18
Status: Published

## Result

The owner's passage-writing prompt is now the canonical Passage Editorial Standard. The first two library groups, Genesis 1:1-31 and 2:1-3, replace generic context and interpretation placeholders with source-checked prose and direct primary-source citations. Both include an optional plan section supported by explicit New Testament connections. Neither has an authorized site position, so each uses the owner's exact open-position wording. No unrelated deeper-study link was added.

The owner-supplied Genesis PDF is retained under `content/assets/reference/stephen_armstrong/` with provenance and checksum. Baseline claims that could not be established by Scripture, lexicons, or independent primary documents are excluded from public copy and recorded in the internal review evidence. The first group distinguishes creation-day readings; the second distinguishes Sabbath applications without promoting one to the site's position.

The renderer preserves source paragraph breaks, supports safe linked primary-source citations, and includes the optional plan section only when content exists. Reviewed pages use question headings in both standalone pages and the reader. A focused `--passages-only` mode updates selected reviewed sources without regenerating unrelated content or running the legacy translation audit. Validation requires a BSB verification source, review evidence, a plan inclusion basis, and an authorized position source; a missing position source uses the exact approved wording.

The BSB comparison found and corrected the stored wording of Genesis 1:21 to match BibleHub's `every winged bird`. Genesis 2:1-3's quotation was unchanged.

## Verification and Release

- Direct BibleHub BSB quotation checks passed for both full passage groups.
- Six focused tests cover safe citations, paragraph preservation, optional-section omission/order, position/plan validation, BibleHub extraction, and scoped publication with failure before any writes.
- The first focused generation changed only two passage pages, their shared library index, and the reader; all other published files were byte-preserved.
- Desktop standalone and mobile reader checks confirmed question headings, paragraph breaks, cited sources, the exact no-position copy, no horizontal overflow, and passage navigation with focus/URL updates. The following unreviewed passage correctly omits the optional section.
- The focused refresh was idempotent; repository checks passed with 0 errors and the existing 401 warnings. Local links had no missing targets or nested anchors.
- CozPlex certificate-backed Scripture project/app readiness, Hosting dry run, and live release passed. Representative live files matched local bytes with no-cache headers, and live reader navigation, corrected BSB quotation, section order, and exact open-position text were verified.

Evidence: [opening Genesis review](../testing/2026-10-18-genesis-opening-editorial-review.md). Next existing group: Genesis 2:4-25.

Live pages: https://the-way-of-scripture.web.app/passages/genesis-1-1-31.html and https://the-way-of-scripture.web.app/passages/genesis-2-1-3.html

The owner also assigned this conversation to CozPlex2 Bridge in Telegram normal mode. Both a checkpoint-associated reply and a separate authenticated message reached the same conversation, and the acknowledgement and milestone returned through that bridge. A future conversation must recheck structured assignment state rather than assume this assignment belongs to it.
