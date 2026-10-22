# Studies Page Consolidation

Date: 2026-10-18  
Host: CozPlex  
Project: `the-way-of-scripture`

## Result

The canonical Studies route, `apps/web/library/index.html`, now presents the complete Foundations guided path as its default view. The former Featured Studies list is gone. All 13 published studies are in one sequence; `Who is The Angel of the Lord?` is Step 5 after `The Gospel According to Jesus`, followed by `I Am a Disciple` at Step 6.

The same page offers an Explore by topic view. Readers can show all six topic groups or filter to one topic. The topic view covers the same 13 studies and retains each study's position in the guided sequence. The homepage's complete-path link and each study's path link point to this canonical Studies route. The homepage still offers a direct Begin action to Step 1.

`library/guided-study.html` now redirects to the canonical path, and `library/studies-all.html` and prior `library/browse.html?type=studies` entry points redirect to its topic view. The passage reader continues to serve `browse.html?type=passages`; its Studies selector also opens the new topic view. No separate study keyword search or featured-studies page remains in the active navigation.

`GUIDED_STUDY_STEPS` is the single source of order in `tools/generate_study_pages.py`. The full generator checks that every source study appears exactly once before writing generated content. The focused `--guided-only` refresh checks the published index, updates all 13 study navigation blocks and study routes, and preserves authored prose.

## Verification

- `python3 tools/check_repo.py` passed with 0 errors and the existing 401 passage-source warnings; `git diff --check` passed.
- All 13 steps, adjacent previous/next links, topic coverage, local links, full-template parity, and byte-idempotent focused refresh passed local checks.
- Removing the new guidance blocks reproduced the prior bytes of all 14 study HTML files, including the study redirect. All 1,018 passage HTML files remained byte-identical.
- Desktop and mobile browser checks covered the guided list, topic switch, all-topic and single-topic counts, direct topic URL restoration, 320 px overflow, legacy redirects, and the passage reader. A browser click from the Gospel study opened The Angel of the Lord as Step 5, with I Am a Disciple next.
- CozPlex's certificate-backed Scripture project and Firebase app-list checks passed. Hosting dry run and live deployment completed successfully. Hosting reported 1,046 public files and uploaded 20 new or changed files.
- Cache-bypassed live byte comparisons matched Home, Studies, both legacy redirect pages, browse, the library index, CSS, representative study pages, and a representative passage page. Live browser checks confirmed all 13 steps, topic filtering, the Gospel → Angel link, and passage browsing.

## Deployment

```bash
~/.local/bin/mg-cloud-firebase deploy --only hosting --project the-way-of-scripture --dry-run
~/.local/bin/mg-cloud-firebase deploy --only hosting --project the-way-of-scripture
```

The existing generator translation debt and passage-source warnings remain separate follow-up work. Prior study and passage teaching content was preserved.
