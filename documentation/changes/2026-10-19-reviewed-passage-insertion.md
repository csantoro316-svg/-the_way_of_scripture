# Add missing reviewed passage groups through focused publication

Matthew's legacy library has only 29 scattered reference groups and no chapter-1 coverage. The focused publisher previously rejected any ID absent from the published index, preventing coherent new coverage without running the legacy full generator.

`--passages-only` now accepts a new source whose canonical book/citation matches its filename, requires the same passage-v1 review and BSB-only source as existing updates, adds it in Bible order, and updates the book list. Existing supplemental records such as Didache remain supported in their current trailing position. All new references are known before rendering, so selection order does not affect links or neighboring descriptions.

When an insertion changes an existing page's previous/next destination, only that navigation block is replaced. Existing prose, footer, metadata, sources, and unrelated pages are preserved. Missing or malformed affected pages fail preparation before any output is written. Normal reviewed updates retain their prior bounded behavior.

The new regression scenario failed before implementation and passes afterward. It covers rejection of an unreviewed batch with no writes, a missing affected neighbor with no writes, multiple inserted groups in reverse input order, addition of a new book, a legacy Didache record, preservation of all old prose and untouched-page bytes, unchanged source files, and idempotence. Eight tests plus repository checks pass (0 errors/401 existing warnings). All 138 Genesis release files remain byte-identical after isolated tests. Logs: `/tmp/scripture-new-passage-regression-{before,after}.log`, `/tmp/scripture-legacy-book-regression-before.log`, `/tmp/scripture-new-passage-checks.log`.

No synthetic test record was added to the real library or deployed. The first real use will be source-checked Matthew groups, with local/live rendering and affected-neighbor preservation checks in that batch. No full generator run, commit, or Telegram notification.
