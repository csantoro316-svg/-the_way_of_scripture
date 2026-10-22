# Guided Foundations Study

Date: 2026-10-18  
Host: CozPlex  
Project: `the-way-of-scripture`

## Result

Published `Foundations: A Guided Study` as a connected 12-study path. The homepage ends its main reading flow with a direct link to The Berean Standard. The Studies page presents the path before its individual featured studies. A dedicated overview lists the complete order and the purpose of each step.

Each study in the path shows its step number and a link to the overview at the top. At the end, readers can move to the previous or next study, with the next topic explained. The final study returns to the overview. `Who is The Angel of the Lord?` appears as an optional companion after The Gospel According to Jesus and leads back to Step 5.

The agreed order is defined in `GUIDED_STUDY_STEPS` in `tools/generate_study_pages.py`:

1. The Berean Standard
2. Is the Bible the Inerrant Word of God?
3. Is There a Source of Truth?
4. The Gospel According to Jesus
5. I Am a Disciple
6. Baptism
7. Prayer and Faith
8. What Does Prayer Look Like?
9. Should We Seek Signs From God?
10. The True Church According to Jesus
11. Who Shepherds the Church?
12. Worship as the Early Church Knew It

The focused command `python3 tools/generate_study_pages.py --guided-only` refreshes guidance in the 13 existing study pages, the Studies landing feature, and the new overview from the published index. It preserves the current study and passage prose. The full generator runs this refresh at the end of normal generation. The homepage invitation remains a hand-maintained page section.

## Verification

- `python3 tools/check_repo.py` passed with 0 errors and 401 existing passage-source warnings; `git diff --check` passed.
- All 12 positions and reciprocal previous/next links were checked. The overview contains 12 steps and the optional companion. All local links on the Home, Studies, overview, and 13 guided study pages resolved.
- Removing the guidance blocks left every published study page byte-for-byte identical to its baseline. The focused refresh was also byte-idempotent.
- Desktop and mobile screenshots were inspected. A browser click from Step 1 to Step 2 opened the correct page in the same tab. The live overview showed all 12 steps and the companion, and its Begin button opened Step 1 without horizontal overflow.
- CozPlex certificate-backed project describe and Firebase app-list passed for `the-way-of-scripture`; the Hosting dry run passed.

## Deployment

The first live Hosting request failed at the Hosting API site lookup without a release result. A subsequent site-list request and project read succeeded; the retry finalized and released the new version. Hosting reported 1,046 public files. Cache-bypassed live byte comparisons matched the local Home, Studies, guided overview, representative first/middle/final and companion study pages, and CSS.

```bash
~/.local/bin/mg-cloud-firebase deploy --only hosting --project the-way-of-scripture --dry-run
~/.local/bin/mg-cloud-firebase deploy --only hosting --project the-way-of-scripture
```

Existing generator translation debt and passage-source warnings remain separate follow-up work. The published study prose and earlier passage-reader changes were preserved.
