> Superseded: all six Matthew11 groups are now complete/live. See `2026-10-19-matthew-eleven-review.md` and next-source handoff `2026-10-19-matthew-twelve-research-in-progress.md`. This file preserves the earlier research state.

# Matthew 11: next research

2026-10-19. Genesis is complete/live. Matthew chapters 1–10 are complete/live: 70 reviewed groups, all 315 verses; 83 source records and 13 unreviewed legacy records. Full goal remains active: finish Matthew, covered NT in Bible order, then Exodus and remaining PDF-covered OT in Bible order. Telegram silent mode continues. No question/blocker and no running deployment.

The previous goal turn made progress: all seven Matthew10 groups researched, verified, and published in two releases. Latest evidence `2026-10-19-matthew-ten-completion-review.md`; earlier `2026-10-19-matthew-first-mission-review.md`. Final four-page release preserved 1,096 unaffected files and byte-matched eight live files. Current website1,103 files; eight tests pass; repository0 errors/375 warnings. All70 reviewed Matthew navigation blocks checked.

## Next source work

No chapter11 JSON yet. Likely coherent groups:11:1–6,7–15,16–19,20–24,25–27,28–30; adjust if actual context warrants. The next legacy Matthew record remains12:38–39. Continue full sequential coverage, not only study-reference records.

Baseline11A PDF537–547 fully read.11B548–557/11C558–567/11D568–578/11E579–588/11F589–599 are identified by page headers but remain unread.12A starts600. Earlier10F514–525 and10G526–536 fully read.10G includes40–42 despite a header ending39.

Actual Matthew11:2–6 BSB was read as a cross-reference in prior chapters; Isaiah35 was read fully during chapter9, and Isaiah53 was read in prior work. Do not treat other cached/fetched documents as read without inspecting target text. No complete independent research for chapter11's own pages yet. Wesley's actual11:1–13 notes were visible/read during chapter10 research; the remaining11 notes require inspection. His11:2 explanation says John's question is for his disciples' benefit, not his own doubt; that differs from many other commentators and should be fairly described rather than suppressed.

## Baseline11A: useful connections and unverified claims

Useful direction: Jesus answers by pointing to His works and the prophetic Scriptures, including Isaiah35 and61; bodily restoration and good news to the poor belong in His identity and God's purpose. The blessed-not-offended saying calls for receiving Him even when expectations differ. The transition connects the disciples' mission with Jesus' continuing teaching. John brings a real question from prison; the Gospels should govern what is known about its motive.

Do not copy the following as facts without primary verification:

- “We know John grew up accepting two Messiahs, called the Prophet/son of Joseph and the Christ/son of David.” John1's separate questions do not prove John's private theology, and silence is not assent. Dating later rabbinic Messiah-ben-Joseph traditions to this precise first-century setting needs independent evidence. No universal claim every rabbi taught one identical scheme.
- The notes reverse a supposed Isaiah division: they assign the suffering servant to1–39 and ruling Christ to40–66, despite Isaiah53 belonging to the latter. Do not import that mapping or an unverified universal rabbinic First/Second-Isaiah classification. Isaiah35/61 can be read directly without it; no authorship theory is required for the passage.
- “John was not asking whether Jesus was Messiah, only which Messiah.” This is the teacher's reconstruction, not the question's stated meaning. Compare actual BSB and primary commentators. No invented expectation of prison release, known disappointment at popularity figures, or exact change in John's emotions after the reply. Jesus' response is recorded; John's later response is not.
- Elijah returning “from the dead” needs care: read2Kings2 if discussing his departure. No fixed eight-miracle count needed. Malachi's messenger/Elijah connection belongs with the later verses and Luke1:17/Matthew17:10–13 if verified, rather than an automatic prediction of two separate Messiahs.
- No claim Luke and Matthew provide a complete identical chronological sequence, every short-term trip mainly trains disciples rather than helps hearers, or nationwide conversion percentages. John is imprisoned and later killed in Gospel narrative; exact site, date, and Herod biography require Scripture or independent historical evidence if used.
- Jesus and John being related does not establish that they were first cousins or grew up together; check Luke1's actual wording. No claimed memorization of all Isaiah, every Jew's ordinary knowledge, or private repeated reading history.
- Do not derive full omniscience at death from1Cor13:12, declare every misunderstood detail easy to solve, or tell readers that inadequate knowledge by itself decides holiness. Retain the useful lesson of humble study and Jesus' scriptural answer without teacher anecdotes or speculative psychology.
- Do not impose the rejected-kingdom/postponement four-stage system from the baseline. Describe God's purposes as Scripture states them. Future links and parallels must meet the optional-plan tests; no secret Joseph-to-Jesus/John mindset biography is established by resemblance alone.

## Primary-source leads and existing research

For11:1–6 read actual Matthew11/Luke7:18–23, Isaiah35/61 and relevant question/title passages. Compare Wesley's own note with Catholic bishops' Matthew11 explanatory notes (not a binding decree) and other original commentators if needed. Do not call a teacher's reading the common view. Check any proposed Greek meaning in Thayer/BDB, not BibleHub's generated Topical Lexicon.

For11:12 the violence/force wording has materially different readings; inspect the actual Greek and primary commentary rather than relying on one gloss. For Elijah, distinguish Jesus' own identification and Luke's spirit-and-power explanation from later speculative timelines. For11:25–27, if discussing grace/election/revelation differences, use traditions' own primary documents and keep their claims recognizable. For11:28–30, check whether the Gospel or Prayer studies have a developed position before filling it; a generic topic match is not enough. Preserve exact open notice otherwise. Do not copy inexact study quotations.

Sources already actually read in chapter10 and reusable if directly relevant:

- Wesley's Matthew notes, full10 and opening11:1–13, at wesley.nnu.edu. Use rfind for chapter headings; find can hit table of contents.
- Westminster Confession17.1–3 (preservation/temporary falls);25.1–6 (Church/headship), primary OPC text.
-1689 Baptist Confession17.1–3 and26.4–5, Founders modern-English edition. urllib often403; web tool cached references opened successfully. Correct URLs `/library/chapter-17-the-perseverance-of-the-saints/` and `/library/chapter-26-the-church/`.
- UMC official Articles of Religion XII at `https://www.umc.org/en/content/articles-of-religion`, direct web open worked; urllib failed.
- Catholic Catechism161–165 at official characteristics-of-faith page;1815–1818 at theological-virtues page; Compendium109 and178–187 at official2005 Compendium. Record actual paragraph limits, not an assertion of having read whole books.
- Scofield1917 Matthew10:16–23 original notes, legal public-domain reprint `https://bible-strong.app/commentary/en/scofield/matt/10`; direct web open worked. StudyLight403, BlueLetter failed, BibleStudyTools paywall provided no commentary and was not used. No need to repeat those failed paths.
- US Catholic bishops' Matthew10 notes1–42 read, but chapter11 notes still need reading. Explain publisher interpretation as such.

## Implementation and publication state

Focused generator only: `python3 tools/generate_study_pages.py --passages-only <selected>`. Never run full generator, reset, or commit the huge preexisting dirty tree. Capture source/index/web hash/all-standalone preimages before edits. Derive affected neighbors by full rendered navigation including description changes. Preserve neighbor prose, nonselected index records, book/study metadata, and unrelated website files.

Reusable temporary helpers:

- `/tmp/audit-scripture-matthew-ten-completion.py`: adapt prefix/message and any permitted study-position names.
- `/tmp/audit-matthew-editorial-state.py <prefix> <endchapter> <endverse>`: full BSB paragraph alignment, all reviewed navigation, continuous coverage. Its known chapter-count map currently ends10:42; add chapter11:30 before using it for11.
- `/tmp/verify-live-scripture-batch.py <prefix>`: selected+affected-neighbor+index+reader bytes, four fetch workers, final live manifest. Run after deploy process is terminal; don't restart a running deploy just because an observation times out.
- Research fetch definitions from `/tmp/scripture-source-fetch-6-9.py` before `urls=`; cache `/tmp/scripture-research-cache/`. Fetched is not read. Keep output bounded; truncated segments need recovery.

Latest artifacts `/tmp/scripture-matthew-ten-completion-` include BSB/check logs, preimages/index/hashes, navigation, coverage, dry-run/deploy, final live.json. All final checks describe the published bytes after plain wording polish. Earlier first-mission index/reader/neighbors are superseded where this release changed them.

Same CozPlex certificate-backed explicit-project readiness passed; all cloud commands use mg-cloud wrappers and `--project the-way-of-scripture`. No account/host switch. Final dry run and deploy exited0. Local HTTP server remains127.0.0.1:8765 serving apps/web. Browser last live10:16–23 at390px: seven choices, five sections, final plain wording, exact open notice, correct previous/next, no overflow. No Telegram notifications.
