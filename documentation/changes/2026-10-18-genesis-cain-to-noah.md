# Genesis Cain-to-Noah editorial batch

Date: 2026-10-18. Status: Published from CozPlex to the explicit `the-way-of-scripture` Firebase Hosting project.

## Result

Completed six existing groups covering Genesis 4–5: Cain and Abel, Cain's descendants, Seth/Enosh, the early family record, Enoch, and Noah's introduction. Added original, plain-language context and common readings; direct NT explanations and clearly labeled parallels connect Abel/Christ, vengeance/forgiveness, the family line/Jesus, Enoch/transformation, and Noah/God's preservation. Necessary lexical explanations use checked BDB entries, not the baseline's unsupported glosses. No new position is invented: all six use the exact approved wording, with existing relationships and URLs retained.

Read the corresponding baseline lessons, checked the Scripture and named lexical entries, and used Wesley's actual commentary where relevant. No artificial denomination breakdown appears where no useful major-tradition distinction was established. Detailed source checks and exclusions are in [the review evidence](../testing/2026-10-18-genesis-cain-to-noah-review.md).

## Numeric quotation-check correction

The prior BSB verifier stripped all numerals when trying to remove printed verse labels. Genesis 5's ages exposed this as a false mismatch. `quotation_matches` now accepts either the exact numbered verses or their exact unnumbered wording, preserving numeric ages and every other word. Added one meaningful regression test covering genuine numbers, missing/changed ages, and a wrong verse label. Reverified all 14 reviewed Genesis 1–5 groups with the stricter checker; all passed. The three Genesis 5 quotation blocks were normalized from BibleHub; no claim that their original numbers were wrong is based on the old comparison.

## Validation and release

- Seven editorial tests and repository validation pass: 0 errors, 401 existing warnings. All 14 full BSB quotation checks pass directly against BibleHub.
- Focused generation is idempotent. Six new passage pages and the library index changed; all 1,042 other published files are byte-preserved from the preceding release.
- Local links exist, no nested citation anchors or raw study Markdown, teacher identity absent, exact no-position text once per page.
- Standalone Genesis 5 shows the actual numeric ages and lexical links, headings in order, no horizontal overflow. The 390px reader displays Enoch with the plan/position sections; next navigation moves to Genesis 5:25–32 with URL/focus updated.
- Certificate-backed project/app readiness passed earlier in this ongoing CozPlex session. Hosting dry run and deployment passed using the host-local wrapper with explicit project selection.
- All six live pages, the library index, and the shared reader were fetched after deployment and match local bytes. Live reader review follows the published source.

The larger owner-authorized project remains active: 14 of 136 existing Genesis groups are now reviewed/published through chapter 5. Next is Genesis 6:1–7. New Testament and remaining covered Old Testament phases remain pending. Telegram silent mode continues; no notification was sent.
