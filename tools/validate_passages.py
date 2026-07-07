#!/usr/bin/env python3

from __future__ import annotations

import json
import re
import sys
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path


ROOT = Path("/home/cozwood/Documents/Dev/the_way_of_scripture")
PASSAGES_DIR = ROOT / "content" / "passages"
STUDIES_DIR = ROOT / "content" / "studies"

BOOK_ORDER = [
    "Genesis", "Exodus", "Leviticus", "Numbers", "Deuteronomy", "Joshua", "Judges",
    "Ruth", "1 Samuel", "2 Samuel", "1 Kings", "2 Kings", "1 Chronicles",
    "2 Chronicles", "Ezra", "Nehemiah", "Esther", "Job", "Psalm", "Psalms",
    "Proverbs", "Ecclesiastes", "Song of Solomon", "Isaiah", "Jeremiah",
    "Lamentations", "Ezekiel", "Daniel", "Hosea", "Joel", "Amos", "Obadiah",
    "Jonah", "Micah", "Nahum", "Habakkuk", "Zephaniah", "Haggai", "Zechariah",
    "Malachi", "Matthew", "Mark", "Luke", "John", "Acts", "Romans",
    "1 Corinthians", "2 Corinthians", "Galatians", "Ephesians", "Philippians",
    "Colossians", "1 Thessalonians", "2 Thessalonians", "1 Timothy", "2 Timothy",
    "Titus", "Philemon", "Hebrews", "James", "1 Peter", "2 Peter", "1 John",
    "2 John", "3 John", "Jude", "Revelation",
]

CITATION_RE = re.compile(r"^(?P<chapter>\d+):(?P<start>\d+)(?:-(?:(?P<end_chapter>\d+):)?(?P<end>\d+))?$")


def slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-") or "study"


@dataclass(frozen=True)
class CitationRange:
    chapter: int
    start_verse: int
    end_chapter: int
    end_verse: int


@dataclass
class ValidationIssue:
    severity: str
    path: Path
    message: str


def parse_citation(citation: str) -> CitationRange | None:
    match = CITATION_RE.match(citation)
    if not match:
        return None
    chapter = int(match.group("chapter"))
    start = int(match.group("start"))
    end_chapter = int(match.group("end_chapter") or chapter)
    end = int(match.group("end") or start)
    return CitationRange(chapter=chapter, start_verse=start, end_chapter=end_chapter, end_verse=end)


def collect_study_slugs() -> set[str]:
    return {path.stem.replace("_", "-") for path in STUDIES_DIR.glob("*.md")}


def validate_versions(payload: dict, path: Path, issues: list[ValidationIssue]) -> None:
    versions = payload.get("versions")
    if not isinstance(versions, list):
        issues.append(ValidationIssue("error", path, "`versions` must be a list."))
        return

    seen_labels: set[str] = set()
    has_bsb = False
    for idx, version in enumerate(versions):
        if not isinstance(version, dict):
            issues.append(ValidationIssue("error", path, f"`versions[{idx}]` must be an object."))
            continue
        label = str(version.get("label", "")).strip()
        text = str(version.get("text", "")).strip()
        raw_paragraphs = version.get("paragraphs")
        paragraphs = []
        if raw_paragraphs is not None:
            if not isinstance(raw_paragraphs, list):
                issues.append(ValidationIssue("error", path, f"`versions[{idx}].paragraphs` must be a list when present."))
            else:
                paragraphs = [str(paragraph).strip() for paragraph in raw_paragraphs if str(paragraph).strip()]
        if not label:
            issues.append(ValidationIssue("error", path, f"`versions[{idx}].label` is required."))
        if not text and not paragraphs:
            issues.append(ValidationIssue("error", path, f"`versions[{idx}]` must include non-empty `text` or `paragraphs`."))
        if label in seen_labels:
            issues.append(ValidationIssue("error", path, f"Duplicate version label `{label}`."))
        seen_labels.add(label)
        if label == "BSB":
            has_bsb = True

    if not has_bsb:
        issues.append(ValidationIssue("warning", path, "Missing `BSB` version block."))


def validate_lines(payload: dict, key: str, path: Path, issues: list[ValidationIssue], *, warn_if_empty: bool = True, fallback_key: str | None = None) -> None:
    lines = payload.get(key, payload.get(fallback_key) if fallback_key else None)
    if not isinstance(lines, list):
        issues.append(ValidationIssue("error", path, f"`{key}` must be a list."))
        return
    if warn_if_empty and not [str(line).strip() for line in lines if str(line).strip()]:
        issues.append(ValidationIssue("warning", path, f"`{key}` is empty."))


def validate_deeper_study(payload: dict, path: Path, study_slugs: set[str], issues: list[ValidationIssue]) -> None:
    links = payload.get("deeper_study")
    if links is None:
        return
    if not isinstance(links, list):
        issues.append(ValidationIssue("error", path, "`deeper_study` must be a list when present."))
        return
    for idx, link in enumerate(links):
        if not isinstance(link, dict):
            issues.append(ValidationIssue("error", path, f"`deeper_study[{idx}]` must be an object."))
            continue
        href = str(link.get("href", "")).strip()
        title = str(link.get("title", "")).strip()
        if not href:
            issues.append(ValidationIssue("error", path, f"`deeper_study[{idx}].href` is required."))
        if not title:
            issues.append(ValidationIssue("error", path, f"`deeper_study[{idx}].title` is required."))
        if href.startswith("../studies/") and href.endswith(".html"):
            slug = href.removeprefix("../studies/").removesuffix(".html")
            if slug not in study_slugs:
                issues.append(ValidationIssue("warning", path, f"`deeper_study[{idx}]` points to missing study slug `{slug}`."))


def validate_optional_lines(payload: dict, key: str, path: Path, issues: list[ValidationIssue]) -> None:
    if key not in payload:
        return
    lines = payload.get(key)
    if not isinstance(lines, list):
        issues.append(ValidationIssue("error", path, f"`{key}` must be a list when present."))
        return
    if not [str(line).strip() for line in lines if str(line).strip()]:
        issues.append(ValidationIssue("warning", path, f"`{key}` is empty."))


def main() -> int:
    issues: list[ValidationIssue] = []
    seen_references: dict[tuple[str, str], Path] = {}
    chapter_ranges: dict[tuple[str, int], list[tuple[CitationRange, Path]]] = defaultdict(list)
    study_slugs = collect_study_slugs()

    for path in sorted(PASSAGES_DIR.glob("*.json")):
        if path.name.startswith("_"):
            continue

        try:
          payload = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            issues.append(ValidationIssue("error", path, f"Invalid JSON: {exc}"))
            continue

        if not isinstance(payload, dict):
            issues.append(ValidationIssue("error", path, "Top-level JSON must be an object."))
            continue

        reference = payload.get("reference")
        if not isinstance(reference, dict):
            issues.append(ValidationIssue("error", path, "`reference` must be an object."))
            continue

        book = str(reference.get("book", "")).strip()
        citation = str(reference.get("citation", "")).strip()
        label = str(reference.get("label", "")).strip()
        slug = str(reference.get("slug", "")).strip()

        if not book:
            issues.append(ValidationIssue("error", path, "`reference.book` is required."))
        elif book not in BOOK_ORDER:
            issues.append(ValidationIssue("warning", path, f"`reference.book` `{book}` is not in the known book order list."))

        parsed = parse_citation(citation)
        if not citation:
            issues.append(ValidationIssue("error", path, "`reference.citation` is required."))
        elif parsed is None:
            issues.append(ValidationIssue("error", path, f"`reference.citation` `{citation}` is invalid."))

        expected_label = f"{book} {citation}".strip()
        if label != expected_label:
            issues.append(ValidationIssue("error", path, f"`reference.label` must equal `{expected_label}`."))

        expected_slug = slugify(f"{book}-{citation}")
        if slug != expected_slug:
            issues.append(ValidationIssue("error", path, f"`reference.slug` must equal `{expected_slug}`."))
        if path.stem != expected_slug:
            issues.append(ValidationIssue("error", path, f"Filename stem must equal `{expected_slug}`."))

        if parsed:
            if parsed.chapter != parsed.end_chapter:
                issues.append(ValidationIssue("warning", path, "Cross-chapter ranges are present; confirm this is intentional."))
            if parsed.end_chapter == parsed.chapter and parsed.end_verse < parsed.start_verse:
                issues.append(ValidationIssue("error", path, "End verse must not be less than start verse."))

            ref_key = (book, citation)
            if ref_key in seen_references:
                issues.append(ValidationIssue("error", path, f"Duplicate reference also defined in `{seen_references[ref_key].name}`."))
            else:
                seen_references[ref_key] = path

            chapter_ranges[(book, parsed.chapter)].append((parsed, path))

        section_title = str(payload.get("section_title", "")).strip()
        if not section_title:
            issues.append(ValidationIssue("warning", path, "Missing `section_title`."))

        validate_versions(payload, path, issues)
        validate_lines(payload, "context_lines", path, issues)
        validate_lines(payload, "common_interpretation_lines", path, issues, fallback_key="explanation_lines")
        validate_optional_lines(payload, "current_position_lines", path, issues)
        validate_deeper_study(payload, path, study_slugs, issues)

    for (book, chapter), entries in sorted(chapter_ranges.items()):
        entries.sort(key=lambda item: (item[0].start_verse, item[0].end_verse))
        for index in range(1, len(entries)):
            prev, prev_path = entries[index - 1]
            current, current_path = entries[index]
            if current.start_verse <= prev.end_verse:
                issues.append(
                    ValidationIssue(
                        "warning",
                        current_path,
                        f"Overlapping section range with `{prev_path.name}` in {book} {chapter}.",
                    )
                )

    errors = [issue for issue in issues if issue.severity == "error"]
    warnings = [issue for issue in issues if issue.severity == "warning"]

    for issue in issues:
        rel = issue.path.relative_to(ROOT)
        print(f"{issue.severity.upper()}: {rel}: {issue.message}")

    print()
    print(f"Passage validation complete: {len(errors)} error(s), {len(warnings)} warning(s).")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
