#!/usr/bin/env python3

from __future__ import annotations

import argparse
import html
import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from collections import defaultdict

from passage_chapter_contexts import CHAPTER_CONTEXTS


ROOT = Path("/home/cozwood/Documents/Dev/the_way_of_scripture")
SOURCE_DIR = ROOT / "content" / "studies"
PASSAGE_SOURCE_DIR = ROOT / "content" / "passages"
WEB_DIR = ROOT / "apps" / "web"
OUTPUT_DIR = WEB_DIR / "studies"
LIBRARY_DIR = WEB_DIR / "library"
PASSAGES_DIR = WEB_DIR / "passages"
PASSAGE_AUDIT_PATH = PASSAGE_SOURCE_DIR / "_audit.json"
GUIDED_STUDY_STEPS = [
    ("returning-to-the-word", "See why Scripture's words and context matter before learning how to test claims."),
    ("the-berean-standard", "Learn to examine every teaching against Scripture, including the claims on this site."),
    ("inerrancy", "Consider what Scripture's authority means when we read translations of ancient texts."),
    ("is-there-a-source-of-truth", "Examine the manuscripts and the question of whether the text can be trusted."),
    ("the-gospel-according-to-jesus", "Hear the central message of Jesus, His death and resurrection, and our response."),
    ("angel-of-the-lord", "Trace the Angel of the Lord in the Old Testament and consider what these passages reveal about Christ."),
    ("i-am-a-disciple", "Move from hearing the gospel to following Jesus in daily life."),
    ("baptism", "Study the response of baptism and the meaning of being buried and raised with Christ."),
    ("prayer-and-faith", "Consider how faith, trust, and surrender shape our approach to God."),
    ("what-does-prayer-look-like", "Watch how Jesus, Paul, and the early church actually pray."),
    ("seek-signs", "Test experiences, signs, and guidance against the pattern Scripture gives."),
    ("true-church", "See how disciples belong together as Christ's people."),
    ("who-shepherds-the-church", "Consider responsibility, teaching, and leadership within the gathered church."),
    ("worship", "Explore worship and participation in the life of the early church."),
]
GUIDED_STUDY_COPY = (
    "Work through a connected series of studies, beginning with why we return to Scripture's "
    "words and context, then how to examine every teaching against the text. Continue through "
    "the gospel, discipleship, prayer, and life together as Christ’s people. "
    "Each study builds on what came before. Take your time, examine the passages, and continue when you’re ready."
)

STUDY_TOPIC_MAP = {
    "returning_to_the_word.md": "Foundations",
    "the_berean_standard.md": "Foundations",
    "is_there_a_source_of_truth.md": "Foundations",
    "inerrancy.md": "Foundations",
    "the_gospel_according_to_jesus.md": "Gospel & Salvation",
    "baptism.md": "Gospel & Salvation",
    "prayer_and_faith.md": "Prayer & Discernment",
    "what_does_prayer_look_like.md": "Prayer & Discernment",
    "seek_signs.md": "Prayer & Discernment",
    "true_church.md": "Church & Worship",
    "who_shepherds_the_church.md": "Church & Worship",
    "worship.md": "Church & Worship",
    "i_am_a_disciple.md": "Identity & Discipleship",
    "angel_of_the_lord.md": "Christ In The Old Testament",
}

STUDY_TOPIC_ORDER = [
    "Foundations",
    "Gospel & Salvation",
    "Christ In The Old Testament",
    "Identity & Discipleship",
    "Prayer & Discernment",
    "Church & Worship",
]

PASSAGE_INTRO_NOTES = {
    ("1 John", "5:14-15"): "The governing principle of prayer: we approach God on His terms, not ours.",
    ("Matthew", "26:39"): "Gethsemane and surrendered faith: not as I will, but as You will.",
    ("Proverbs", "3:5-6"): "Trust that runs through prayer, baptism, faith, and the site’s entire posture.",
    ("Acts", "17:11"): "The Berean standard: examine everything against the Word yourself.",
    ("Hebrews", "4:12"): "What the site believes about Scripture itself: living, active, and discerning.",
    ("1 Corinthians", "3:16"): "A core church passage: the people of God are His temple.",
    ("1 Peter", "2:9"): "Every believer as priest: a royal priesthood, not a clerical class.",
    ("Romans", "8:26-27"): "When words fail, the Spirit intercedes according to the will of God.",
    ("Romans", "6:3-4"): "The theological heart of baptism: buried and raised with Christ.",
    ("John", "13:34-35"): "Love as the identifying mark of the true Church.",
    ("Deuteronomy", "4:2"): "Do not add to the Word: stated plainly in the Law and echoed across the site.",
    ("1 Corinthians", "14:26"): "Let all things be done for edification: a closing standard for the whole project.",
}

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

REFERENCE_PATTERN = re.compile(
    r"(?<![A-Za-z0-9])((?:[1-3]\s)?[A-Z][A-Za-z]+(?:\s[A-Z][A-Za-z]+)*)\s(\d+:\d+(?:-(?:(?:\d+):)?\d+)?)"
)
ORDERED_LIST_PATTERN = re.compile(r"^\d+\.\s+")


@dataclass
class Study:
    title: str
    subtitle: str
    translation: str
    slug: str
    source_name: str
    summary: str
    intro_lines: list[str]
    intro_html: str
    body_html: str
    body_lines: list[str]
    references: list["PassageReference"]


@dataclass(frozen=True)
class PassageReference:
    book: str
    citation: str

    @property
    def slug(self) -> str:
        return slugify(f"{self.book}-{self.citation}")

    @property
    def label(self) -> str:
        return f"{self.book} {self.citation}"


@dataclass(frozen=True)
class PassageSource:
    title: str
    href: str


@dataclass(frozen=True)
class PassageVersion:
    label: str
    text: str
    paragraphs: tuple[str, ...] = ()


@dataclass(frozen=True)
class PassageContent:
    verses: list[PassageVersion]
    context_lines: list[str]
    common_interpretation_lines: list[str]
    current_position_lines: list[str]
    deeper_study: list[PassageSource]
    section_title: str = ""
    god_plan_lines: list[str] = field(default_factory=list)
    editorial_review: dict[str, object] = field(default_factory=dict)


NO_PASSAGE_POSITION = "We don't have a position on this passage yet. When our study reaches a conclusion the text supports, it will appear here."


def passage_section_headings(content: PassageContent) -> dict[str, str]:
    if content.editorial_review.get("standard") == "passage-v1":
        return {
            "context": "What is the context?",
            "common": "How is this passage commonly understood?",
            "plan": "Where does this fit in God's plan?",
            "position": "What is our position?",
            "deeper": "Where can I study this further?",
        }
    return {"context": "Context", "common": "Common Interpretations", "plan": "Where does this fit in God's plan?", "position": "Current Position", "deeper": "Deeper Study"}


@dataclass(frozen=True)
class MarkdownBlock:
    kind: str
    text: str


KNOWN_PASSAGE_REFERENCES: set["PassageReference"] = set()


def slugify(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug or "study"


def sort_key_without_numeric_prefix(text: str) -> tuple[str, str]:
    normalized = re.sub(r"^[1-3]\s+", "", text).strip().lower()
    return normalized, text.lower()


def passage_sort_key(reference: PassageReference) -> tuple:
    """Order books canonically and ranges by numeric start, then numeric end."""
    match = re.fullmatch(r"(\d+):(\d+)(?:-(?:(\d+):)?(\d+))?", reference.citation)
    if not match:
        raise ValueError(f"Cannot order passage: {reference.label}")
    chapter, verse, end_chapter, end_verse = match.groups()
    return (
        BOOK_ORDER.index(reference.book) if reference.book in BOOK_ORDER else len(BOOK_ORDER),
        reference.book,
        int(chapter),
        int(verse),
        int(end_chapter or chapter),
        int(end_verse or verse),
    )


def render_passage_navigation(previous: dict | None, following: dict | None) -> str:
    links = []
    for direction, item in (("previous", previous), ("next", following)):
        if item is None:
            continue
        label = "← Previous passage" if direction == "previous" else "Next passage →"
        relation = "prev" if direction == "previous" else "next"
        subtitle = (
            f'\n                <span class="passage-navigation-title">{html.escape(item["section_title"])}</span>'
            if item.get("section_title") else ""
        )
        links.append(f'''              <a class="passage-navigation-link passage-navigation-{direction}" href="{html.escape(item["href"], quote=True)}" rel="{relation}">
                <span class="passage-navigation-label">{label}</span>
                <strong>{html.escape(item["title"])}</strong>{subtitle}
              </a>''')
    if not links:
        return ""
    return ('            <nav class="passage-navigation" aria-label="Passage navigation">\n'
            + "\n".join(links) + '\n            </nav>\n')


def insert_passage_navigation(page: str, navigation: str) -> str:
    """Replace only navigation, preserving all authored passage HTML."""
    page = re.sub(
        r'            <nav class="passage-navigation" aria-label="Passage navigation">.*?            </nav>\n',
        "", page, flags=re.DOTALL,
    )
    marker = "          </article>"
    if page.count(marker) != 1:
        raise ValueError("Expected one passage article; refusing to change page")
    return page.replace(marker, navigation + marker, 1)


def refresh_passage_navigation() -> None:
    """Refresh navigation from the published library without regenerating prose."""
    index_path = WEB_DIR / "assets" / "library_index.json"
    data = json.loads(index_path.read_text(encoding="utf-8"))
    passages = sorted(data["passages"], key=lambda item: passage_sort_key(
        PassageReference(item["book"], item["citation"])
    ))
    updates = []
    for position, item in enumerate(passages):
        path = PASSAGES_DIR / f'{item["id"]}.html'
        page = path.read_text(encoding="utf-8")
        navigation = render_passage_navigation(
            passages[position - 1] if position else None,
            passages[position + 1] if position + 1 < len(passages) else None,
        )
        updates.append((path, insert_passage_navigation(page, navigation)))
    data["passages"] = passages
    # Prepare all pages before writing so a missing page or marker fails safely.
    updates.append((index_path, json.dumps(data, ensure_ascii=True, indent=2)))
    updates.append((LIBRARY_DIR / "passages.html", passages_page_html()))
    updates.append((LIBRARY_DIR / "browse.html", legacy_browse_html()))
    updates.append((LIBRARY_DIR / "passages-by-book.html", browse_redirect_html("./passages.html")))
    for path, text in updates:
        path.write_text(text, encoding="utf-8")


def studies_page_html(studies_by_slug: dict[str, dict]) -> str:
    """Make the complete guided path the canonical Studies page."""
    cards = []
    for position, (slug, description) in enumerate(GUIDED_STUDY_STEPS, start=1):
        study = studies_by_slug[slug]
        cards.append(f'''          <li class="guided-step">
            <span class="guided-step-number">{position:02d}</span>
            <div>
              <h2><a href="../studies/{slug}.html">{html.escape(study["title"])}</a></h2>
              <p>{html.escape(description)}</p>
            </div>
            <a class="guided-step-action" href="../studies/{slug}.html">Read study →</a>
          </li>''')
    topics = list(dict.fromkeys(studies_by_slug[slug]["topic"] for slug, _ in GUIDED_STUDY_STEPS))
    topic_options = '\n'.join(
        f'              <option value="{html.escape(topic, quote=True)}">{html.escape(topic)}</option>'
        for topic in topics
    )
    topic_groups = []
    for topic in topics:
        items = []
        for position, (slug, description) in enumerate(GUIDED_STUDY_STEPS, start=1):
            study = studies_by_slug[slug]
            if study["topic"] != topic:
                continue
            items.append(f'''              <li class="topic-study-card">
                <div>
                  <span class="topic-study-position">Study {position} of {len(GUIDED_STUDY_STEPS)}</span>
                  <h3><a href="../studies/{slug}.html">{html.escape(study["title"])}</a></h3>
                  <p>{html.escape(description)}</p>
                </div>
                <a href="../studies/{slug}.html">Read study →</a>
              </li>''')
        topic_groups.append(f'''          <section class="topic-group" data-topic="{html.escape(topic, quote=True)}" aria-label="{html.escape(topic, quote=True)}">
            <h2>{html.escape(topic)}</h2>
            <ul class="topic-study-list">
{chr(10).join(items)}
            </ul>
          </section>''')
    script = """    <script>
      const viewButtons = [...document.querySelectorAll('[data-study-view]')];
      const pathView = document.getElementById('guidedPathView');
      const topicsView = document.getElementById('studyTopicsView');
      const topicSelect = document.getElementById('studyTopicSelect');
      const topicGroups = [...document.querySelectorAll('.topic-group')];
      const topicCount = document.getElementById('topicCount');
      const params = new URLSearchParams(location.search);

      function showView(view, updateUrl = true) {
        const showTopics = view === 'topics';
        pathView.hidden = showTopics;
        topicsView.hidden = !showTopics;
        viewButtons.forEach((button) => {
          button.setAttribute('aria-pressed', String(button.dataset.studyView === (showTopics ? 'topics' : 'path')));
        });
        if (updateUrl) {
          const url = new URL(location.href);
          if (showTopics) {
            url.searchParams.set('view', 'topics');
            if (topicSelect.value !== 'all') url.searchParams.set('topic', topicSelect.value);
          }
          else {
            url.searchParams.delete('view');
            url.searchParams.delete('topic');
          }
          history.replaceState(null, '', url);
        }
      }

      function filterTopics(updateUrl = true) {
        const selected = topicSelect.value;
        let count = 0;
        topicGroups.forEach((group) => {
          const visible = selected === 'all' || group.dataset.topic === selected;
          group.hidden = !visible;
          if (visible) count += group.querySelectorAll('.topic-study-card').length;
        });
        topicCount.textContent = `Showing ${count} ${count === 1 ? 'study' : 'studies'}${selected === 'all' ? ' across all topics' : ''}.`;
        if (updateUrl) {
          const url = new URL(location.href);
          if (selected === 'all') url.searchParams.delete('topic');
          else url.searchParams.set('topic', selected);
          history.replaceState(null, '', url);
        }
      }

      viewButtons.forEach((button) => button.addEventListener('click', () => showView(button.dataset.studyView)));
      topicSelect.addEventListener('change', () => filterTopics());
      if ([...topicSelect.options].some((option) => option.value === params.get('topic'))) {
        topicSelect.value = params.get('topic');
      }
      filterTopics(false);
      showView(params.get('view') === 'topics' ? 'topics' : 'path', false);
    </script>"""
    return f'''<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Studies | The Way of Scripture</title>
    <meta name="description" content="Follow all {len(GUIDED_STUDY_STEPS)} studies in a guided path or explore them by topic." />
    <link rel="stylesheet" href="../styles.css" />
  </head>
  <body>
    <div class="page-shell">
      <header class="site-header">
        <a class="brand" href="../index.html" aria-label="The Way of Scripture home">
          <img class="brand-mark" src="../assets/icons/icon.jpg" alt="The Way of Scripture icon" />
          <div class="brand-copy">
            <span class="brand-title">The Way of Scripture</span>
            <span class="brand-subtitle">Returning to the text itself</span>
          </div>
        </a>
{primary_nav("studies")}
      </header>

      <main>
        <section class="article-hero">
          <p class="eyebrow">Studies · {len(GUIDED_STUDY_STEPS)} steps</p>
          <h1>Foundations: A Guided Study</h1>
          <p class="lead">{html.escape(GUIDED_STUDY_COPY)}</p>
          <div class="guided-actions">
            <a class="guided-button" href="../studies/{GUIDED_STUDY_STEPS[0][0]}.html">Begin the first study →</a>
          </div>
        </section>

        <div class="study-view-switch" role="group" aria-label="Choose how to explore studies">
          <button type="button" data-study-view="path" aria-pressed="true" aria-controls="guidedPathView">Guided path</button>
          <button type="button" data-study-view="topics" aria-pressed="false" aria-controls="studyTopicsView">Explore by topic</button>
        </div>

        <section id="guidedPathView" aria-label="Guided study path">
          <ol class="guided-step-list" aria-label="Guided study order">
{chr(10).join(cards)}
          </ol>
        </section>

        <section id="studyTopicsView" aria-label="Studies by topic" hidden>
          <div class="topic-filter-bar">
            <label for="studyTopicSelect">Filter by topic</label>
            <select id="studyTopicSelect">
              <option value="all">All topics</option>
{topic_options}
            </select>
            <p id="topicCount" role="status" aria-live="polite">Showing {len(GUIDED_STUDY_STEPS)} studies across all topics.</p>
          </div>
          <div class="topic-group-list">
{chr(10).join(topic_groups)}
          </div>
        </section>
      </main>
    </div>
{script}
  </body>
</html>
'''


def guided_study_inserts(slug: str, studies_by_slug: dict[str, dict]) -> tuple[str, str]:
    steps = [name for name, _ in GUIDED_STUDY_STEPS]
    position = steps.index(slug)
    previous = studies_by_slug[steps[position - 1]] if position else None
    following = studies_by_slug[steps[position + 1]] if position + 1 < len(steps) else None
    top = f'''          <div class="guided-study-top">
            <span>Study {position + 1} of {len(steps)} in Foundations</span>
            <a href="../library/index.html">View the guided path</a>
          </div>'''
    links = []
    if previous:
        links.append(f'''          <a class="guided-navigation-link" href="../studies/{previous["id"]}.html" rel="prev"><span>← Previous study</span><strong>{html.escape(previous["title"])}</strong></a>''')
    if following:
        links.append(f'''          <a class="guided-navigation-link guided-navigation-next" href="../studies/{following["id"]}.html" rel="next"><span>Continue with Study {position + 2} of {len(steps)} →</span><strong>{html.escape(following["title"])}</strong></a>''')
    else:
        links.append('''          <a class="guided-navigation-link guided-navigation-next" href="../library/index.html"><span>You've completed the path</span><strong>See the complete path →</strong></a>''')
    next_context = (
        f'          <p class="guided-next-context">Next: {html.escape(GUIDED_STUDY_STEPS[position + 1][1])}</p>\n'
        if following else f'          <p class="guided-next-context">You have reached the end of the {len(steps)}-study foundation path.</p>\n'
    )
    bottom = f'''        <nav class="guided-study-navigation" aria-label="Guided study navigation">
          <p class="eyebrow">Foundations · Study {position + 1} of {len(steps)}</p>
          <h2>Keep studying</h2>
          <div class="guided-navigation-links">
{chr(10).join(links)}
          </div>
{next_context}          <a class="guided-path-link" href="../library/index.html">View the complete path</a>
        </nav>'''
    return top, bottom


def insert_guided_study_blocks(page: str, top: str, bottom: str) -> str:
    """Update guidance only, leaving the published study prose intact."""
    for block in ("top", "bottom"):
        page = re.sub(
            rf'        <!-- guided-study-{block}:start -->.*?        <!-- guided-study-{block}:end -->\n',
            "", page, flags=re.DOTALL,
        )
    hero_marker = '          <div class="article-hero-copy prose">'
    footer_marker = '        <section class="feedback-note" aria-label="Feedback note">'
    if page.count(hero_marker) != 1 or page.count(footer_marker) != 1:
        raise ValueError("Expected one study hero and feedback note; refusing to change page")
    page = page.replace(hero_marker, f'        <!-- guided-study-top:start -->\n{top}\n        <!-- guided-study-top:end -->\n{hero_marker}', 1)
    return page.replace(footer_marker, f'        <!-- guided-study-bottom:start -->\n{bottom}\n        <!-- guided-study-bottom:end -->\n{footer_marker}', 1)


def refresh_guided_study() -> None:
    """Refresh the path and page navigation without regenerating study content."""
    index_path = WEB_DIR / "assets" / "library_index.json"
    index = json.loads(index_path.read_text(encoding="utf-8"))
    studies_by_slug = {study["id"]: study for study in index["studies"]}
    slugs = [slug for slug, _ in GUIDED_STUDY_STEPS]
    if len(slugs) != len(set(slugs)) or set(slugs) != set(studies_by_slug):
        raise ValueError("Guided study order must include every published study exactly once")
    updates = []
    for slug in slugs:
        path = OUTPUT_DIR / f"{slug}.html"
        top, bottom = guided_study_inserts(slug, studies_by_slug)
        updates.append((path, insert_guided_study_blocks(path.read_text(encoding="utf-8"), top, bottom)))
    index["studies"] = [studies_by_slug[slug] for slug in slugs]
    index["study_topic_order"] = STUDY_TOPIC_ORDER
    updates.append((index_path, json.dumps(index, ensure_ascii=True, indent=2)))
    updates.append((LIBRARY_DIR / "index.html", studies_page_html(studies_by_slug)))
    updates.append((LIBRARY_DIR / "guided-study.html", browse_redirect_html("./index.html")))
    updates.append((LIBRARY_DIR / "studies-all.html", browse_redirect_html("./index.html?view=topics")))
    for path, page in updates:
        path.write_text(page, encoding="utf-8")


def extract_references(text: str) -> list[PassageReference]:
    seen: set[PassageReference] = set()
    references: list[PassageReference] = []
    for match in REFERENCE_PATTERN.finditer(text):
        book = match.group(1).strip()
        citation = match.group(2).strip()
        ref = PassageReference(book=book, citation=citation)
        if ref not in seen:
            seen.add(ref)
            references.append(ref)
    return references


def passage_reference(book: str, citation: str) -> PassageReference:
    return PassageReference(book=book, citation=citation)


def passage_href(reference: PassageReference, depth: str = "..") -> str:
    return f"{depth}/passages/{reference.slug}.html"


def passage_link_attrs() -> str:
    return ' target="_blank" rel="noopener noreferrer"'


def parse_citation(citation: str) -> tuple[int, int, int, int] | None:
    match = re.fullmatch(r"(\d+):(\d+)(?:-(?:(\d+):)?(\d+))?", citation)
    if not match:
        return None
    start_chapter = int(match.group(1))
    start_verse = int(match.group(2))
    end_chapter = int(match.group(3) or match.group(1))
    end_verse = int(match.group(4) or match.group(2))
    return start_chapter, start_verse, end_chapter, end_verse


def reference_contains(container: PassageReference, target: PassageReference) -> bool:
    if container.book != target.book:
        return False
    container_range = parse_citation(container.citation)
    target_range = parse_citation(target.citation)
    if not container_range or not target_range:
        return False
    container_start_chapter, container_start_verse, container_end_chapter, container_end_verse = container_range
    target_start_chapter, target_start_verse, target_end_chapter, target_end_verse = target_range
    return (
        (container_start_chapter, container_start_verse) <= (target_start_chapter, target_start_verse)
        and (container_end_chapter, container_end_verse) >= (target_end_chapter, target_end_verse)
    )


def resolve_alias_reference(
    reference: PassageReference,
    source_references: set[PassageReference],
) -> PassageReference | None:
    if reference in source_references:
        return None

    candidates = [
        candidate
        for candidate in source_references
        if reference_contains(candidate, reference)
    ]
    if not candidates:
        return None

    def sort_key(candidate: PassageReference) -> tuple[int, int, str]:
        parsed = parse_citation(candidate.citation)
        assert parsed is not None
        start_chapter, start_verse, end_chapter, end_verse = parsed
        span = ((end_chapter - start_chapter) * 1000) + (end_verse - start_verse)
        return span, start_verse, candidate.label

    return min(candidates, key=sort_key)


def render_reference_links(
    text: str,
    current_reference: PassageReference | None = None,
) -> str:
    rendered = html.escape(text)

    def replace(match: re.Match[str]) -> str:
        book = match.group(1).strip()
        citation = match.group(2).strip()
        ref = PassageReference(book=book, citation=citation)
        label = html.escape(f"{book} {citation}")
        if current_reference and ref == current_reference:
            return label
        if KNOWN_PASSAGE_REFERENCES and ref not in KNOWN_PASSAGE_REFERENCES:
            return label
        return f'<a href="{passage_href(ref)}"{passage_link_attrs()}>{label}</a>'

    rendered = re.sub(
        r"((?:[1-3]\s)?[A-Z][A-Za-z]+(?:\s[A-Z][A-Za-z]+)*)\s(\d+:\d+(?:-\d+)?)",
        replace,
        rendered,
    )
    rendered = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", rendered)
    rendered = re.sub(r"\*(.+?)\*", r"<em>\1</em>", rendered)
    return rendered


def render_inline(text: str) -> str:
    rendered = html.escape(text)
    rendered = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", rendered)
    rendered = re.sub(r"\*(.+?)\*", r"<em>\1</em>", rendered)
    return rendered


STUDY_LINKS: dict[str, str] = {}


def render_study_links(text: str, current_study_slug: str | None = None) -> str:
    rendered = text
    for title, slug in sorted(STUDY_LINKS.items(), key=lambda item: len(item[0]), reverse=True):
        if current_study_slug and slug == current_study_slug:
            continue
        escaped_title = re.escape(html.escape(title))
        rendered = re.sub(
            escaped_title,
            lambda _: f'<a href="../studies/{slug}.html">{html.escape(title)}</a>',
            rendered,
        )
    return rendered


def render_blocks(
    lines: list[str],
    enable_reference_links: bool = False,
    current_reference: PassageReference | None = None,
    current_study_slug: str | None = None,
) -> str:
    output: list[str] = []
    i = 0
    inline_renderer = (
        (
            lambda text: render_study_links(
                render_reference_links(text, current_reference=current_reference),
                current_study_slug=current_study_slug,
            )
        )
        if enable_reference_links
        else render_inline
    )

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if not stripped:
            i += 1
            continue

        if stripped == "---":
            if output:
                output.append('<hr class="prose-divider" />')
            i += 1
            continue

        if stripped.startswith("#### "):
            output.append(f"<h4>{inline_renderer(stripped[5:])}</h4>")
            i += 1
            continue

        if stripped.startswith("### "):
            output.append(f"<h3>{inline_renderer(stripped[4:])}</h3>")
            i += 1
            continue

        if stripped.startswith("## "):
            output.append(f"<h2>{inline_renderer(stripped[3:])}</h2>")
            i += 1
            continue

        if stripped.startswith("> "):
            quote_lines: list[str] = []
            while i < len(lines) and lines[i].strip().startswith("> "):
                quote_lines.append(lines[i].strip()[2:])
                i += 1
            quote_text = " ".join(part.strip() for part in quote_lines)
            output.append(f"<blockquote><p>{inline_renderer(quote_text)}</p></blockquote>")
            continue

        if stripped.startswith("- "):
            items: list[str] = []
            while i < len(lines) and lines[i].strip().startswith("- "):
                items.append(lines[i].strip()[2:])
                i += 1
            rendered_items = "".join(
                f"<li>{inline_renderer(item)}</li>" for item in items
            )
            output.append(f'<ul class="prose-list">{rendered_items}</ul>')
            continue

        if ORDERED_LIST_PATTERN.match(stripped):
            items: list[str] = []
            while i < len(lines) and ORDERED_LIST_PATTERN.match(lines[i].strip()):
                items.append(ORDERED_LIST_PATTERN.sub("", lines[i].strip(), count=1))
                i += 1
            rendered_items = "".join(
                f"<li>{inline_renderer(item)}</li>" for item in items
            )
            output.append(f'<ol class="prose-list">{rendered_items}</ol>')
            continue

        paragraph_lines = [stripped]
        i += 1
        while i < len(lines):
            next_stripped = lines[i].strip()
            if not next_stripped:
                break
            if (
                next_stripped == "---"
                or next_stripped.startswith("## ")
                or next_stripped.startswith("### ")
                or next_stripped.startswith("#### ")
                or next_stripped.startswith("> ")
                or next_stripped.startswith("- ")
                or ORDERED_LIST_PATTERN.match(next_stripped)
            ):
                break
            paragraph_lines.append(next_stripped)
            i += 1
        paragraph = " ".join(paragraph_lines)
        output.append(f"<p>{inline_renderer(paragraph)}</p>")

    return "\n              ".join(output)


def markdown_blocks(lines: list[str]) -> list[MarkdownBlock]:
    blocks: list[MarkdownBlock] = []
    i = 0
    while i < len(lines):
        stripped = lines[i].strip()
        if not stripped:
            i += 1
            continue
        if stripped == "---":
            i += 1
            continue
        if stripped.startswith("#### "):
            blocks.append(MarkdownBlock(kind="heading4", text=stripped[5:].strip()))
            i += 1
            continue
        if stripped.startswith("### "):
            blocks.append(MarkdownBlock(kind="heading3", text=stripped[4:].strip()))
            i += 1
            continue
        if stripped.startswith("## "):
            blocks.append(MarkdownBlock(kind="heading2", text=stripped[3:].strip()))
            i += 1
            continue
        if stripped.startswith("> "):
            quote_lines: list[str] = []
            while i < len(lines) and lines[i].strip().startswith("> "):
                quote_lines.append(lines[i].strip()[2:])
                i += 1
            blocks.append(MarkdownBlock(kind="quote", text=" ".join(quote_lines).strip()))
            continue
        if stripped.startswith("- "):
            items: list[str] = []
            while i < len(lines) and lines[i].strip().startswith("- "):
                items.append(lines[i].strip()[2:])
                i += 1
            blocks.append(MarkdownBlock(kind="list", text="\n".join(items)))
            continue
        if ORDERED_LIST_PATTERN.match(stripped):
            items: list[str] = []
            while i < len(lines) and ORDERED_LIST_PATTERN.match(lines[i].strip()):
                items.append(ORDERED_LIST_PATTERN.sub("", lines[i].strip(), count=1))
                i += 1
            blocks.append(MarkdownBlock(kind="list", text="\n".join(items)))
            continue

        paragraph_lines = [stripped]
        i += 1
        while i < len(lines):
            next_stripped = lines[i].strip()
            if (
                not next_stripped
                or next_stripped == "---"
                or next_stripped.startswith("## ")
                or next_stripped.startswith("### ")
                or next_stripped.startswith("#### ")
                or next_stripped.startswith("> ")
                or next_stripped.startswith("- ")
                or ORDERED_LIST_PATTERN.match(next_stripped)
            ):
                break
            paragraph_lines.append(next_stripped)
            i += 1
        blocks.append(MarkdownBlock(kind="paragraph", text=" ".join(paragraph_lines)))
    return blocks


def summarize_blocks(lines: list[str]) -> str:
    parts: list[str] = []
    for block in markdown_blocks(lines):
        if block.kind == "paragraph":
            text = re.sub(r"\s+", " ", block.text).strip()
            text = text.replace("**", "").replace("*", "")
            parts.append(text)
        elif block.kind == "list":
            items = [
                re.sub(r"\s+", " ", item).strip().replace("**", "").replace("*", "")
                for item in block.text.splitlines()
            ]
            parts.extend(item for item in items if item)
    return " ".join(part for part in parts if part).strip()


def hoist_leading_body_intro(body_lines: list[str]) -> tuple[list[str], list[str]]:
    if not body_lines:
        return [], body_lines

    i = 0
    while i < len(body_lines) and not body_lines[i].strip():
        i += 1

    if i >= len(body_lines):
        return [], body_lines

    first_heading_index = None
    if body_lines[i].strip().startswith("## "):
        first_heading_index = i
        i += 1
        while i < len(body_lines) and not body_lines[i].strip():
            i += 1

    intro_start = i
    saw_paragraph_content = False

    while i < len(body_lines):
        stripped = body_lines[i].strip()
        if not stripped:
            if saw_paragraph_content:
                i += 1
                continue
            break
        if (
            stripped == "---"
            or stripped.startswith("## ")
            or stripped.startswith("### ")
            or stripped.startswith("#### ")
            or stripped.startswith("> ")
            or stripped.startswith("- ")
            or ORDERED_LIST_PATTERN.match(stripped)
        ):
            break
        saw_paragraph_content = True
        i += 1

    intro_lines = body_lines[intro_start:i]
    if not summarize_blocks(intro_lines):
        return [], body_lines

    remove_start = first_heading_index if first_heading_index is not None else intro_start
    remaining_lines = body_lines[i:]
    while remaining_lines and not remaining_lines[0].strip():
        remaining_lines = remaining_lines[1:]
    if remaining_lines and remaining_lines[0].strip() == "---":
        remaining_lines = remaining_lines[1:]
        while remaining_lines and not remaining_lines[0].strip():
            remaining_lines = remaining_lines[1:]

    return intro_lines, body_lines[:remove_start] + remaining_lines


def block_mentions_reference(block: MarkdownBlock, reference: PassageReference) -> bool:
    return reference.label in block.text


def extract_lsb_verse_text(reference: PassageReference, studies: list[Study]) -> str | None:
    heading_marker = f"### {reference.label}"
    reference_pattern = re.compile(rf"\*\*{re.escape(reference.label)}(?:\*\*|\s*\()")
    verse_pattern = re.compile(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)")
    for study in studies:
        lines = study.body_lines
        for idx, line in enumerate(lines):
            stripped = line.strip()
            if stripped.startswith("> ") and reference_pattern.search(stripped):
                quote_lines = [stripped[2:]]
                j = idx + 1
                while j < len(lines) and lines[j].strip().startswith("> "):
                    quote_lines.append(lines[j].strip()[2:])
                    j += 1
                quote_text = " ".join(quote_lines)
                matches = verse_pattern.findall(quote_text)
                if matches:
                    return max((match.strip() for match in matches), key=len)
            if stripped == heading_marker:
                j = idx + 1
                while j < len(lines) and not lines[j].strip():
                    j += 1
                quote_lines: list[str] = []
                while j < len(lines) and lines[j].strip().startswith("> "):
                    quote_lines.append(lines[j].strip()[2:])
                    j += 1
                if quote_lines:
                    matches = verse_pattern.findall(" ".join(quote_lines))
                    if matches:
                        return max((match.strip() for match in matches), key=len)
    return None


def extract_explanation_lines(reference: PassageReference, studies: list[Study]) -> list[str]:
    seen: set[str] = set()
    for study in studies:
        blocks = markdown_blocks(study.body_lines)
        gathered: list[str] = []

        exact_heading_indexes = [
            idx for idx, block in enumerate(blocks)
            if block.kind in {"heading2", "heading3"} and block.text.strip() == reference.label
        ]
        candidate_indexes = exact_heading_indexes or [
            idx for idx, block in enumerate(blocks) if block_mentions_reference(block, reference)
        ]
        for idx in candidate_indexes:
            block = blocks[idx]

            candidate_texts: list[str] = []
            if block.kind == "paragraph":
                candidate_texts.append(block.text)

            capture_count = 0
            for next_block in blocks[idx + 1:]:
                if next_block.kind in {"heading2", "heading3"} and capture_count:
                    break
                if next_block.kind == "paragraph":
                    candidate_texts.append(next_block.text)
                    capture_count += 1
                elif next_block.kind == "list" and capture_count < 2:
                    candidate_texts.append("\n".join(f"- {item}" for item in next_block.text.splitlines()))
                    capture_count += 1
                elif next_block.kind == "quote":
                    continue
                if capture_count >= 2:
                    break

            for text in candidate_texts:
                normalized = re.sub(r"\s+", " ", text).strip()
                if not normalized or normalized in seen:
                    continue
                seen.add(normalized)
                gathered.extend(text.splitlines())
                gathered.append("")
            if len(gathered) >= 6:
                break

        while gathered and not gathered[-1].strip():
            gathered.pop()
        if gathered:
            return gathered

    return []


def derive_passage_content(reference: PassageReference, linked_studies: list[Study]) -> PassageContent:
    override = PASSAGE_CONTENT.get(reference)
    if override:
        return override

    chapter = reference.citation.split(":", 1)[0]
    context_lines = CHAPTER_CONTEXTS.get(
        (reference.book, chapter),
        [f"{reference.label} should be read within the flow of its chapter and the larger argument of {reference.book}."],
    )
    common_interpretation_lines = extract_explanation_lines(reference, linked_studies)
    verses: list[PassageVersion] = []
    lsb_text = extract_lsb_verse_text(reference, linked_studies)
    if lsb_text:
        verses.append(PassageVersion(label="LSB", text=lsb_text))

    if not common_interpretation_lines:
        common_interpretation_lines = [
            f"{reference.label} should be read first within its own scriptural setting rather than as an isolated slogan.",
            "",
            "Where this passage is brought into conversation with other texts, its force should still be governed by its immediate chapter flow and the larger argument of the book.",
        ]

    return PassageContent(
        verses=verses,
        context_lines=context_lines,
        common_interpretation_lines=common_interpretation_lines,
        current_position_lines=[NO_PASSAGE_POSITION],
        deeper_study=[
            PassageSource(title=study.title, href=f"../studies/{study.slug}.html")
            for study in linked_studies
        ],
    )


def passage_source_path(reference: PassageReference) -> Path:
    return PASSAGE_SOURCE_DIR / f"{reference.slug}.json"


def serialize_passage_content(reference: PassageReference, content: PassageContent) -> str:
    payload = {
        "reference": {
            "book": reference.book,
            "citation": reference.citation,
            "label": reference.label,
            "slug": reference.slug,
        },
        "section_title": content.section_title,
        "versions": [
            (
                {"label": version.label, "paragraphs": list(version.paragraphs)}
                if version.paragraphs
                else {"label": version.label, "text": version.text}
            )
            for version in content.verses
        ],
        "context_lines": content.context_lines,
        "common_interpretation_lines": content.common_interpretation_lines,
        "current_position_lines": content.current_position_lines,
        "deeper_study": [
            {"title": item.title, "href": item.href}
            for item in content.deeper_study
        ],
    }
    if any(line.strip() for line in content.god_plan_lines):
        payload["god_plan_lines"] = content.god_plan_lines
    if content.editorial_review:
        payload["editorial_review"] = content.editorial_review
    return json.dumps(payload, ensure_ascii=True, indent=2) + "\n"


def load_passage_source_content(reference: PassageReference) -> PassageContent | None:
    path = passage_source_path(reference)
    if not path.exists():
        return None

    payload = json.loads(path.read_text(encoding="utf-8"))
    versions: list[PassageVersion] = []
    for item in payload.get("versions", []):
        label = str(item.get("label", "")).strip()
        if not label:
            continue
        raw_paragraphs = item.get("paragraphs")
        paragraphs = tuple(
            str(paragraph).strip()
            for paragraph in raw_paragraphs
            if str(paragraph).strip()
        ) if isinstance(raw_paragraphs, list) else ()
        text = str(item.get("text", "")).strip()
        if not paragraphs and not text:
            continue
        versions.append(
            PassageVersion(
                label=label,
                text=text or " ".join(paragraphs),
                paragraphs=paragraphs,
            )
        )
    context_lines = [str(line) for line in payload.get("context_lines", [])]
    raw_common_lines = payload.get("common_interpretation_lines", payload.get("explanation_lines", []))
    common_interpretation_lines = [str(line) for line in raw_common_lines]
    raw_current_position_lines = payload.get("current_position_lines", [])
    current_position_lines = [str(line) for line in raw_current_position_lines]
    if not any(line.strip() for line in current_position_lines):
        current_position_lines = [NO_PASSAGE_POSITION]
    deeper_study = [
        PassageSource(title=str(item.get("title", "")).strip(), href=str(item.get("href", "")).strip())
        for item in payload.get("deeper_study", [])
        if isinstance(item, dict) and str(item.get("title", "")).strip() and str(item.get("href", "")).strip()
    ]
    return PassageContent(
        verses=versions,
        context_lines=context_lines,
        common_interpretation_lines=common_interpretation_lines,
        current_position_lines=current_position_lines,
        deeper_study=deeper_study,
        section_title=str(payload.get("section_title", "")).strip(),
        god_plan_lines=[str(line) for line in payload.get("god_plan_lines", [])],
        editorial_review=payload.get("editorial_review", {}),
    )


def standalone_passage_references() -> list[PassageReference]:
    references: list[PassageReference] = []
    seen: set[PassageReference] = set()
    for path in sorted(PASSAGE_SOURCE_DIR.glob("*.json")):
        if path.name.startswith("_"):
            continue
        payload = json.loads(path.read_text(encoding="utf-8"))
        reference_payload = payload.get("reference", {})
        book = str(reference_payload.get("book", "")).strip()
        citation = str(reference_payload.get("citation", "")).strip()
        if not book or not citation:
            continue
        reference = passage_reference(book, citation)
        if reference in seen:
            continue
        seen.add(reference)
        references.append(reference)
    return references


def ensure_passage_source_files(reference_map: dict[PassageReference, list[Study]]) -> None:
    PASSAGE_SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    for reference in sorted(reference_map.keys(), key=lambda ref: ref.label):
        path = passage_source_path(reference)
        if path.exists():
            continue
        derived = derive_passage_content(reference, reference_map.get(reference, []))
        path.write_text(serialize_passage_content(reference, derived), encoding="utf-8")


def build_passage_content(reference: PassageReference, linked_studies: list[Study]) -> PassageContent:
    sourced = load_passage_source_content(reference)
    if sourced:
        return sourced
    return derive_passage_content(reference, linked_studies)


def write_passage_source_audit(reference_map: dict[PassageReference, list[Study]]) -> None:
    required_versions = ["LSB", "NKJV", "NABRE"]
    audit_rows: list[dict[str, object]] = []
    for reference in sorted(reference_map.keys(), key=lambda ref: ref.label):
        content = build_passage_content(reference, reference_map.get(reference, []))
        present = [version.label for version in content.verses]
        missing = [label for label in required_versions if label not in present]
        audit_rows.append(
            {
                "reference": reference.label,
                "slug": reference.slug,
                "source_file": str(passage_source_path(reference).relative_to(ROOT)),
                "present_versions": present,
                "missing_versions": missing,
                "has_context": bool(content.context_lines),
                "has_common_interpretations": bool(content.common_interpretation_lines),
                "has_deeper_study": bool(content.deeper_study),
            }
        )

    summary = {
        "total_passages": len(audit_rows),
        "fully_populated": sum(1 for row in audit_rows if not row["missing_versions"]),
        "missing_any_version": sum(1 for row in audit_rows if row["missing_versions"]),
        "rows": audit_rows,
    }
    PASSAGE_AUDIT_PATH.write_text(
        json.dumps(summary, ensure_ascii=True, indent=2) + "\n",
        encoding="utf-8",
    )


PASSAGE_CONTENT: dict[PassageReference, PassageContent] = {
    passage_reference("1 John", "5:14-15"): PassageContent(
        verses=[
            PassageVersion(
                label="LSB",
                text=(
                    "Now this is the confidence which we have before Him, that if we ask "
                    "anything according to His will, He hears us. And if we know that He "
                    "hears us in whatever we ask, we know that we have the requests which "
                    "we have asked from Him."
                ),
            ),
            PassageVersion(
                label="NKJV",
                text=(
                    "Now this is the confidence that we have in Him, that if we ask "
                    "anything according to His will, He hears us. And if we know that He "
                    "hears us, whatever we ask, we know that we have the petitions that we "
                    "have asked of Him."
                ),
            ),
            PassageVersion(
                label="NABRE",
                text=(
                    "And we have this confidence in him, that if we ask anything according "
                    "to his will, he hears us. And if we know that he hears us in regard to "
                    "whatever we ask, we know that what we have asked him for is ours."
                ),
            ),
        ],
        context_lines=[
            "**1 John 5:14-15** comes near the close of the letter, where John is drawing "
            "together his pastoral purpose: that believers may know the life they have in the "
            "Son and live with confidence before God.",
            "",
            "The immediate context matters. In **1 John 5:13**, John says he is writing so "
            "that believers may know they have eternal life. Then in verses 14-15 he moves "
            "straight into confidence in prayer, and in verses 16-17 he applies that confidence "
            "to a concrete case involving prayer for a brother in sin. The passage is therefore "
            "not an isolated slogan about getting what one wants from God. It sits inside a "
            "larger argument about abiding in the Son, walking in truth, and praying in a way "
            "consistent with God's own life and character.",
            "",
            "That wider setting also guards against cherry-picking. Throughout **1 John**, John "
            "contrasts truth and falsehood, obedience and disobedience, love and hatred, life "
            "and death. By the time chapter 5 arrives, confidence before God is already tied to "
            "remaining in Him, believing rightly about Christ, and keeping His commandments. "
            "Verses 14-15 belong inside that whole framework.",
        ],
        common_interpretation_lines=[
            "The promise is conditional at every step. The text does not say, 'ask and you will "
            "receive' without qualification. It says that **if** we ask according to His will, "
            "**then** He hears us; and if He hears us, **then** we know we have what we asked.",
            "",
            "That means the controlling issue is not sincerity, repetition, or emotional force. "
            "The controlling issue is alignment with God's will. John places confidence in "
            "prayer under God's rule, not under human desire.",
            "",
            "Read that way, the verse becomes a boundary for other prayer passages. "
            "**Acts 4:29-31** shows believers asking for boldness so the word of God may go "
            "forward, and the request is granted. By contrast, **2 Corinthians 12:7-9** and "
            "**Romans 15:30-32** show that even earnest, specific requests are not granted "
            "simply because they are heartfelt. The issue remains whether the request serves "
            "God's purpose rather than personal relief or preference.",
            "",
            "The same principle fits naturally with **John 15:7**, where abiding in Christ shapes "
            "what is desired and asked, and with **Romans 8:26-27**, where the Spirit intercedes "
            "according to the will of God when believers do not know how to pray as they should. "
            "Taken together, **1 John 5:14-15** presents prayer as confidence under God's will, "
            "not leverage for securing personal outcomes.",
        ],
        current_position_lines=[
            "This site's current position is that **1 John 5:14-15** functions as a governing boundary for prayer. The passage does not present prayer as a blank check for desired outcomes, but as confidence that rests under the will of God.",
            "",
            "That means requests are not measured by intensity, repetition, or sincerity alone. They are measured by whether they align with God's purposes. The fuller argument for that reading is developed in the linked studies below.",
        ],
        deeper_study=[
            PassageSource(title="Prayer and Faith", href="../studies/prayer-and-faith.html"),
            PassageSource(title="What Does Prayer Look Like?", href="../studies/what-does-prayer-look-like.html"),
        ],
    ),
}


def parse_study(path: Path) -> Study:
    lines = path.read_text(encoding="utf-8").splitlines()
    title = ""
    subtitle = ""
    translation = "Legacy Standard Bible (LSB)"
    body_start = 0
    seen_header_divider = False

    for idx, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("# ") and not title:
            title = stripped[2:].strip()
            body_start = idx + 1
            continue
        if stripped == "---":
            seen_header_divider = True
            continue
        if stripped.startswith("## ") and not subtitle and not seen_header_divider:
            subtitle = stripped[3:].strip()
            continue
        if stripped.startswith("*Primary Translation:"):
            translation = stripped.strip("*").replace("Primary Translation:", "").strip()
            continue
    if not subtitle:
        preface_lines: list[str] = []
        preface_raw_lines: list[str] = []
        in_intro_block = False
        for line in lines[body_start:]:
            stripped = line.strip()
            if not stripped:
                continue
            if stripped == "---":
                if in_intro_block:
                    break
                in_intro_block = True
                continue
            if stripped.startswith("## "):
                break
            if stripped.startswith("*Primary Translation:"):
                continue
            if in_intro_block:
                preface_raw_lines.append(stripped)
                preface_lines.append(stripped.strip("*").strip())

        stylized_preface = bool(preface_raw_lines) and all(
            raw.startswith("*") and raw.endswith("*") for raw in preface_raw_lines
        )

        if preface_lines and stylized_preface:
            subtitle = preface_lines[0]

    filtered_body: list[str] = []
    consumed_subtitle = False
    consumed_translation = False

    for idx, line in enumerate(lines[body_start:], start=body_start):
        stripped = line.strip()
        if idx == body_start - 1:
            continue
        if stripped.startswith("## ") and not consumed_subtitle and stripped[3:].strip() == subtitle:
            consumed_subtitle = True
            continue
        if (
            stripped.startswith("*Primary Translation:")
            and not consumed_translation
        ):
            consumed_translation = True
            continue
        filtered_body.append(line)

    intro_started = False
    intro_complete = False
    intro_lines: list[str] = []
    body_lines: list[str] = []

    for line in filtered_body:
        stripped = line.strip()
        if not intro_complete:
            if not stripped:
                if intro_started and intro_lines:
                    intro_lines.append(line)
                continue
            if stripped == "---":
                if not intro_started:
                    intro_started = True
                    continue
                intro_complete = True
                continue
            if not intro_started:
                continue
            if stripped.startswith("## "):
                intro_complete = True
                body_lines.append(line)
                continue
            intro_lines.append(line)
            continue
        body_lines.append(line)

    if not intro_complete and intro_lines:
        body_lines = []

    if not intro_lines:
        hoisted_intro_lines, body_lines = hoist_leading_body_intro(body_lines)
        if hoisted_intro_lines:
            intro_lines = hoisted_intro_lines

    study_text = "\n".join(intro_lines + body_lines)
    references = extract_references(study_text)
    slug = slugify(path.stem.replace("_", "-"))
    intro_html = render_blocks(intro_lines, enable_reference_links=True, current_study_slug=slug)
    body_html = render_blocks(body_lines, enable_reference_links=True, current_study_slug=slug)
    summary = summarize_blocks(intro_lines)
    if not summary:
        summary = title or path.stem.replace("_", " ").title()

    return Study(
        title=title or path.stem.replace("_", " ").title(),
        subtitle=subtitle,
        translation=translation,
        slug=slug,
        source_name=path.name,
        summary=summary,
        intro_lines=intro_lines,
        intro_html=intro_html,
        body_html=body_html,
        body_lines=body_lines,
        references=references,
    )


def primary_nav(current: str, depth: str = "..") -> str:
    studies_href = f"{depth}/library/index.html"
    passages_href = f"{depth}/library/passages.html"
    return f"""        <nav class="site-nav" aria-label="Primary">
          <a href="{depth}/index.html">Home</a>
          <a href="{studies_href}"{" aria-current=\"page\"" if current == "studies" else ""}>Studies</a>
          <a href="{passages_href}"{" aria-current=\"page\"" if current == "passages" else ""}>Passages</a>
        </nav>"""


def browse_redirect_html(target: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta http-equiv="refresh" content="0; url={target}" />
    <title>Redirecting...</title>
  </head>
  <body>
    <p><a href="{target}">Continue to browse.</a></p>
  </body>
</html>
"""


def passage_redirect_html(reference: PassageReference, target: PassageReference) -> str:
    target_href = f"./{target.slug}.html"
    return f"""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta http-equiv="refresh" content="0; url={target_href}" />
    <title>{html.escape(reference.label)} | Redirecting</title>
  </head>
  <body>
    <p><a href="{target_href}">Continue to {html.escape(target.label)}.</a></p>
  </body>
</html>
"""


def study_page_html(study: Study) -> str:
    subtitle_html = (
        f'            <p class="article-subtitle">{html.escape(study.subtitle)}</p>\n'
        if study.subtitle
        else ""
    )
    intro_html = study.intro_html or f'<p class="lead">{html.escape(study.summary)}</p>'
    return f"""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{html.escape(study.title)} | The Way of Scripture</title>
    <meta
      name="description"
      content="{html.escape(study.summary)}"
    />
    <link rel="stylesheet" href="../styles.css" />
  </head>
  <body>
    <div class="page-shell">
      <header class="site-header">
        <a class="brand" href="../index.html" aria-label="The Way of Scripture home">
          <img
            class="brand-mark"
            src="../assets/icons/icon.jpg"
            alt="The Way of Scripture icon"
          />
          <div class="brand-copy">
            <span class="brand-title">The Way of Scripture</span>
            <span class="brand-subtitle">Returning to the text itself</span>
          </div>
        </a>
{primary_nav("studies")}
      </header>

      <main>
        <section class="article-hero">
          <p class="eyebrow">Study</p>
          <h1>{html.escape(study.title)}</h1>
{subtitle_html}          <p class="article-meta">Primary Translation: {html.escape(study.translation)}</p>
          <div class="article-hero-copy prose">
            {intro_html}
          </div>
        </section>

        <div class="article-layout">
          <article class="article-body">
            <div class="prose">
              {study.body_html}
            </div>
          </article>
        </div>

        <section class="feedback-note" aria-label="Feedback note">
          <h2>A Living Study And Exchange</h2>
          <p>
            This site is a living study effort. Thoughtful feedback is welcome, and future study may lead to clarification, correction, or revision.
          </p>
          <p>
            Public comments, when enabled, will be reviewed before appearing on the site so discussion remains respectful and relevant. The goal is to grow in understanding, test everything by Scripture, and remain willing to change where the text requires it.
          </p>
        </section>
      </main>
    </div>
  </body>
</html>
"""


def render_passage_versions(versions: list[PassageVersion]) -> str:
    def display_label(label: str) -> str:
        return "Berean Standard Bible" if label == "BSB" else label

    def render_version_text(version: PassageVersion) -> str:
        paragraphs = version.paragraphs or ((version.text,) if version.text else ())
        return "".join(f"<p>{html.escape(paragraph)}</p>" for paragraph in paragraphs)

    return "\n".join(
        f"""          <div class="passage-version">
            <h2>{html.escape(display_label(version.label))}</h2>
            <blockquote>{render_version_text(version)}</blockquote>
          </div>"""
        for version in versions
    )


def render_passage_hero(reference: PassageReference) -> str:
    content = build_passage_content(reference, [])
    if not content.verses:
        return """          <p class="lead">Full passage content has not been curated from the study material yet.</p>"""

    return render_passage_versions(content.verses)


def render_passage_lines(lines: list[str], reference: PassageReference) -> str:
    """Render source citations separately so Scripture auto-links cannot nest anchors."""
    citations: list[str] = []

    def protect(match: re.Match[str]) -> str:
        label, href = match.groups()
        token = f"\ue000citation{len(citations)}\ue001"
        citations.append(f'<a href="{html.escape(href, quote=True)}"{passage_link_attrs()}>{render_inline(label)}</a>')
        return token

    protected = [re.sub(r"\[([^\]\n]+)\]\((https?://[^\s)]+)\)", protect, line) for line in lines]
    rendered = render_blocks(protected, enable_reference_links=True, current_reference=reference)
    for index, citation in enumerate(citations):
        rendered = rendered.replace(f"\ue000citation{index}\ue001", citation)
    return rendered


def render_passage_body_sections(reference: PassageReference, linked_studies: list[Study]) -> str:
    content = build_passage_content(reference, linked_studies)
    if not content:
        return """              <h2>Context</h2>
              <p>
                This passage still needs its reviewed contextual summary.
              </p>

              <h2>Common Interpretations</h2>
              <p>
                This passage still needs its full treatment from the source material.
              </p>

              <h2>Current Position</h2>
              <p>
                No defined position is stated here yet beyond the common interpretations above.
                As related study develops, this section will be updated where the text warrants a clearer conclusion.
              </p>

              <h2>Deeper Study</h2>
              <p>
                No deeper study linked yet.
              </p>"""

    headings = passage_section_headings(content)
    context_html = render_passage_lines(content.context_lines, reference)
    common_interpretations_html = render_passage_lines(content.common_interpretation_lines, reference)
    current_position_html = render_passage_lines(content.current_position_lines, reference)
    plan_html = (
        f"\n              <h2>{html.escape(headings['plan'])}</h2>\n"
        f"              {render_passage_lines(content.god_plan_lines, reference)}\n"
        if any(line.strip() for line in content.god_plan_lines) else ""
    )
    deeper_study_html = (
        "<ul class=\"study-link-list\">"
        + "".join(
            f'<li><a href="{html.escape(item.href)}">{html.escape(item.title)}</a></li>'
            for item in content.deeper_study
        )
        + "</ul>"
        if content.deeper_study
        else "<p>No deeper study linked yet.</p>"
    )
    return f"""              <h2>{html.escape(headings['context'])}</h2>
              {context_html}

              <h2>{html.escape(headings['common'])}</h2>
              {common_interpretations_html}
{plan_html}
              <h2>{html.escape(headings['position'])}</h2>
              {current_position_html}

              <h2>{html.escape(headings['deeper'])}</h2>
              {deeper_study_html}"""


def passage_payload(reference: PassageReference, linked_studies: list[Study]) -> dict[str, object]:
    content = build_passage_content(reference, linked_studies)
    return {
        "id": reference.slug,
        "title": reference.label,
        "section_title": content.section_title,
        "book": reference.book,
        "citation": reference.citation,
        "note": PASSAGE_INTRO_NOTES.get((reference.book, reference.citation), ""),
        "href": f"../passages/{reference.slug}.html",
        "versions": [
            {
                "label": version.label,
                "text": version.text,
                "paragraphs": list(version.paragraphs),
            }
            for version in content.verses
        ],
        "section_headings": passage_section_headings(content),
        "context_html": render_passage_lines(content.context_lines, reference),
        "common_interpretations_html": render_passage_lines(content.common_interpretation_lines, reference),
        "god_plan_html": render_passage_lines(content.god_plan_lines, reference),
        "current_position_html": render_passage_lines(content.current_position_lines, reference),
        "deeper_study": [
            {
                "title": item.title,
                "href": item.href,
            }
            for item in content.deeper_study
        ],
    }


def passage_page_html(reference: PassageReference, linked_studies: list[Study]) -> str:
    content = build_passage_content(reference, linked_studies)
    subtitle_parts = []
    if content.section_title:
        subtitle_parts.append(f'          <p class="article-subtitle">{html.escape(content.section_title)}</p>')
    note = PASSAGE_INTRO_NOTES.get((reference.book, reference.citation), "").strip()
    if note:
        subtitle_parts.append(f'          <p class="lead">{html.escape(note)}</p>')
    subtitle_html = "\n".join(subtitle_parts) + ("\n" if subtitle_parts else "")
    return f"""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{html.escape(reference.label)} | The Way of Scripture</title>
    <meta
      name="description"
      content="Passage reference page for {html.escape(reference.label)}."
    />
    <link rel="stylesheet" href="../styles.css" />
  </head>
  <body>
    <div class="page-shell">
      <header class="site-header">
        <a class="brand" href="../index.html" aria-label="The Way of Scripture home">
          <img
            class="brand-mark"
            src="../assets/icons/icon.jpg"
            alt="The Way of Scripture icon"
          />
          <div class="brand-copy">
            <span class="brand-title">The Way of Scripture</span>
            <span class="brand-subtitle">Returning to the text itself</span>
          </div>
        </a>
{primary_nav("passages")}
      </header>

      <main>
        <section class="article-hero">
          <p class="eyebrow">Passage</p>
          <h1>{html.escape(reference.label)}</h1>
{subtitle_html}{render_passage_versions(content.verses) if content.verses else '          <p class="lead">Full passage text for this reference is not yet quoted in the current local source material.</p>'}
        </section>

        <div class="article-layout">
          <article class="article-body">
            <div class="prose">
{render_passage_body_sections(reference, linked_studies)}
            </div>
          </article>
        </div>

        <section class="feedback-note" aria-label="Feedback note">
          <h2>A Living Study And Exchange</h2>
          <p>
            This site is a living study effort. Thoughtful feedback is welcome, and future study may lead to clarification, correction, or revision.
          </p>
          <p>
            Public comments, when enabled, will be reviewed before appearing on the site so discussion remains respectful and relevant. The goal is to grow in understanding, test everything by Scripture, and remain willing to change where the text requires it.
          </p>
        </section>
      </main>
    </div>
  </body>
</html>
"""


def studies_all_html(studies: list[Study]) -> str:
    return browse_redirect_html("./index.html?view=topics")


def library_index_html(studies: list[Study]) -> str:
    by_slug = {
        study.slug: {
            "id": study.slug,
            "title": study.title,
            "topic": STUDY_TOPIC_MAP.get(study.source_name, "Other Studies"),
        }
        for study in studies
    }
    return studies_page_html(by_slug)


def passages_by_book_html(grouped_references: dict[str, list[PassageReference]]) -> str:
    return browse_redirect_html("./passages.html")


def legacy_browse_html() -> str:
    """Send old shared-library URLs to the canonical study or passage page."""
    return """<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Redirecting | The Way of Scripture</title>
    <script>
      const params = new URLSearchParams(location.search);
      if (params.get("type") === "passages") {
        params.delete("type");
        const query = params.toString();
        location.replace("./passages.html" + (query ? "?" + query : ""));
      } else {
        location.replace("./index.html?view=topics");
      }
    </script>
  </head>
  <body>
    <p><a href="./passages.html">Continue to Passages</a> or <a href="./index.html?view=topics">explore Studies by topic</a>.</p>
  </body>
</html>
"""


def passages_page_html() -> str:
    return """<!DOCTYPE html>
<html lang="en" class="library-reader-page">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Passages | The Way of Scripture</title>
    <meta
      name="description"
      content="Read the Scripture passages currently available in The Way of Scripture library."
    />
    <link rel="stylesheet" href="../styles.css" />
  </head>
  <body>
    <div class="page-shell">
      <header class="site-header">
        <a class="brand" href="../index.html" aria-label="The Way of Scripture home">
          <img
            class="brand-mark"
            src="../assets/icons/icon.jpg"
            alt="The Way of Scripture icon"
          />
          <div class="brand-copy">
            <span class="brand-title">The Way of Scripture</span>
            <span class="brand-subtitle">Returning to the text itself</span>
          </div>
        </a>
        <nav class="site-nav" aria-label="Primary">
          <a href="../index.html">Home</a>
          <a href="./index.html">Studies</a>
          <a href="./passages.html" aria-current="page">Passages</a>
        </nav>
      </header>

      <main class="kb-shell">
        <section class="kb-topbar scripture-kb-topbar">
          <div class="kb-topbar-inner scripture-kb-topbar-inner">
            <div class="kb-topbar-copy">
              <h1 class="kb-title">Passages</h1>
              <p>Explore the passages currently available in the library. Choose a book, chapter, and passage to read.</p>
            </div>
            <input id="librarySearch" class="kb-search" type="search" placeholder="Search passages or books..." />
          </div>
        </section>

        <section id="readerToolbar" class="reader-toolbar" aria-label="Library reading controls">
          <div id="passageJumpControls" class="reader-jump-controls" hidden>
            <label class="reader-field" for="passageBookSelect">
              <span>Book</span>
              <select id="passageBookSelect" class="kb-select"></select>
            </label>
            <label class="reader-field" for="passageChapterSelect">
              <span>Chapter</span>
              <select id="passageChapterSelect" class="kb-select"></select>
            </label>
            <label class="reader-field reader-passage-field" for="passageSectionSelect">
              <span>Passage</span>
              <select id="passageSectionSelect" class="kb-select"></select>
            </label>
          </div>
          <span id="readerStudyLabel" class="reader-study-label">Study library</span>
          <button id="libraryBrowseBtn" class="kb-browse-btn" aria-haspopup="dialog" aria-controls="libraryNavDrawer" aria-expanded="false">Browse Library</button>
        </section>

        <details id="browsePassageGuide" class="feedback-note kb-guide-note" hidden>
          <summary>About these sections</summary>
          <div class="kb-guide-copy">
          <p>
            <strong>Context</strong> explains where the passage sits in its chapter and larger scriptural setting so it is not read in isolation.
          </p>
          <p>
            <strong>Common Interpretations</strong> summarizes the main ways the passage is commonly understood. This section is descriptive, not declarative, and does not imply the site agrees with every reading listed there.
          </p>
          <p>
            <strong>Where does this fit in God's plan?</strong> appears only where Scripture supports a connection beyond the interpretation already given.
          </p>
          <p>
            <strong>Our Position</strong> states where our study has reached a supported conclusion. If no position has been developed, the page leaves the matter open.
          </p>
          <p>
            <strong>Deeper Study</strong> points to fuller studies connected to the passage, especially where the broader argument or supporting reasoning has already been developed.
          </p>
          </div>
        </details>

          <dialog class="kb-nav kb-drawer" id="libraryNavDrawer" aria-labelledby="libraryDrawerTitle">
            <div class="kb-drawer-header">
              <h2 id="libraryDrawerTitle">Browse Library</h2>
              <button id="libraryCloseBtn" class="kb-nav-action-btn" type="button" autofocus>Close</button>
            </div>
            <div class="kb-nav-controls">
              <label class="kb-control-label" for="libraryViewSelect">Browse By</label>
              <select id="libraryViewSelect" class="kb-select">
                <option value="alpha">Alphabetical</option>
                <option value="book">By Book</option>
              </select>

              <div class="kb-nav-actions">
                <button id="libraryExpandAll" class="kb-nav-action-btn">Expand All</button>
                <button id="libraryCollapseAll" class="kb-nav-action-btn">Collapse All</button>
              </div>
            </div>
            <div class="kb-nav-filter">
              <label class="kb-control-label" for="libraryNavSearch">Filter Navigation</label>
              <input id="libraryNavSearch" class="kb-search kb-nav-search" type="search" placeholder="Book, chapter, passage..." />
            </div>
            <div id="libraryNav"></div>
          </dialog>

        <section class="kb-layout scripture-kb-layout">
          <article class="kb-content">
            <div id="libraryResults" class="kb-results"></div>
            <div id="libraryArticle"></div>
          </article>
        </section>
      </main>
    </div>

    <script>
      let LIBRARY_DATA = { studies: [], passages: [] };
      let activeType = "passages";
      let activeId = "";
      let navView = "alpha";
      let navFilter = "";
      let returnDrawerFocus = true;
      const collapsedGroups = new Set();

      const viewSelectEl = document.getElementById("libraryViewSelect");
      const expandAllEl = document.getElementById("libraryExpandAll");
      const collapseAllEl = document.getElementById("libraryCollapseAll");
      const navSearchEl = document.getElementById("libraryNavSearch");
      const navEl = document.getElementById("libraryNav");
      const navDrawerEl = document.getElementById("libraryNavDrawer");
      const closeBtnEl = document.getElementById("libraryCloseBtn");
      const browseBtnEl = document.getElementById("libraryBrowseBtn");
      const articleEl = document.getElementById("libraryArticle");
      const resultsEl = document.getElementById("libraryResults");
      const searchEl = document.getElementById("librarySearch");
      const passageGuideEl = document.getElementById("browsePassageGuide");
      const readerToolbarEl = document.getElementById("readerToolbar");
      const jumpControlsEl = document.getElementById("passageJumpControls");
      const studyLabelEl = document.getElementById("readerStudyLabel");
      const bookSelectEl = document.getElementById("passageBookSelect");
      const chapterSelectEl = document.getElementById("passageChapterSelect");
      const passageSelectEl = document.getElementById("passageSectionSelect");

      // Keep selected headings below the sticky controls at every screen size.
      new ResizeObserver(() => {
        document.documentElement.style.setProperty(
          "--reader-toolbar-height", `${readerToolbarEl.getBoundingClientRect().height}px`
        );
      }).observe(readerToolbarEl);

      function getStudyTopic(item) {
        return item.topic || "Other Studies";
      }

      function compareStudyTitles(a, b) {
        return (a.title || "").localeCompare(b.title || "");
      }

      function getCurrentItems() {
        return LIBRARY_DATA[activeType] || [];
      }

      function normalizeBookLabel(value) {
        return (value || "").replace(/^[1-3]\\s+/, "").trim().toLowerCase();
      }

      function compactSectionLabel(value) {
        return (value || "").replace(/\\s+and\\s+/g, " & ");
      }

      function parseCitation(citation) {
        const match = /^(\\d+):(\\d+)(?:-(?:(\\d+):)?(\\d+))?$/.exec(citation || "");
        if (!match) {
          return {
            startChapter: Number.MAX_SAFE_INTEGER,
            startVerse: Number.MAX_SAFE_INTEGER,
            endChapter: Number.MAX_SAFE_INTEGER,
            endVerse: Number.MAX_SAFE_INTEGER,
          };
        }
        const startChapter = Number(match[1]);
        const startVerse = Number(match[2]);
        const endChapter = Number(match[3] || match[1]);
        const endVerse = Number(match[4] || match[2]);
        return { startChapter, startVerse, endChapter, endVerse };
      }

      function buildPassageBooks() {
        const byBook = new Map();
        getCurrentItems().forEach((item) => {
          const book = item.book || "Other";
          const parsed = parseCitation(item.citation);
          const chapterKey = String(parsed.startChapter);
          if (!byBook.has(book)) {
            byBook.set(book, { key: book, label: book, items: [], chapters: new Map() });
          }
          const bookEntry = byBook.get(book);
          bookEntry.items.push(item);
          if (!bookEntry.chapters.has(chapterKey)) {
            bookEntry.chapters.set(chapterKey, {
              key: chapterKey,
              label: `Chapter ${parsed.startChapter}`,
              chapterNumber: parsed.startChapter,
              items: [],
            });
          }
          bookEntry.chapters.get(chapterKey).items.push({
            ...item,
            parsedCitation: parsed,
          });
        });

        const canonicalOrder = LIBRARY_DATA.book_order || [];
        return Array.from(byBook.values())
          .sort((a, b) => {
            if (navView === "book") {
              const ai = canonicalOrder.indexOf(a.key);
              const bi = canonicalOrder.indexOf(b.key);
              const ar = ai === -1 ? Number.MAX_SAFE_INTEGER : ai;
              const br = bi === -1 ? Number.MAX_SAFE_INTEGER : bi;
              return ar - br || normalizeBookLabel(a.label).localeCompare(normalizeBookLabel(b.label)) || a.label.localeCompare(b.label);
            }
            return normalizeBookLabel(a.label).localeCompare(normalizeBookLabel(b.label)) || a.label.localeCompare(b.label);
          })
          .map((bookEntry) => ({
            ...bookEntry,
            chapters: Array.from(bookEntry.chapters.values())
              .sort((a, b) => a.chapterNumber - b.chapterNumber)
              .map((chapter) => ({
                ...chapter,
                items: chapter.items.slice().sort((a, b) => {
                  return a.parsedCitation.startVerse - b.parsedCitation.startVerse
                    || a.parsedCitation.endVerse - b.parsedCitation.endVerse
                    || a.title.localeCompare(b.title);
                }),
              })),
          }));
      }

      function syncQuery() {
        const url = new URL(window.location.href);
        url.searchParams.delete("type");
        if (navView === "book") url.searchParams.delete("view");
        else url.searchParams.set("view", navView);
        if (activeType === "passages" && activeId) url.searchParams.set("passage", activeId);
        else url.searchParams.delete("passage");
        window.history.replaceState({}, "", url);
      }

      function syncViewOptions() {
        if (activeType === "studies") {
          viewSelectEl.innerHTML = '<option value="alpha">Alphabetical</option><option value="topic">By Topic</option>';
          if (navView !== "alpha" && navView !== "topic") {
            navView = "alpha";
          }
        } else {
          viewSelectEl.innerHTML = '<option value="book">By Book</option><option value="alpha">Alphabetical</option>';
          if (navView !== "book" && navView !== "alpha") {
            navView = "book";
          }
        }
        viewSelectEl.value = navView;
      }

      function syncNavFilterPlaceholder() {
        navSearchEl.placeholder = activeType === "studies"
          ? (navView === "topic" ? "Study title or topic..." : "Study title...")
          : "Book, chapter, verse...";
      }

      function syncNavActionVisibility() {
        const showActions = activeType === "passages" || (activeType === "studies" && navView === "topic");
        expandAllEl.style.display = showActions ? "" : "none";
        collapseAllEl.style.display = showActions ? "" : "none";
      }

      function syncPassageGuideVisibility() {
        passageGuideEl.hidden = activeType !== "passages";
      }

      function syncPassageSelectors(item) {
        const isPassage = activeType === "passages";
        jumpControlsEl.hidden = !isPassage;
        studyLabelEl.hidden = isPassage;
        if (!isPassage) return;
        const passages = LIBRARY_DATA.passages || [];
        const setOptions = (select, options, value) => {
          select.replaceChildren(...options.map(([label, id]) => new Option(label, id)));
          select.value = value || "";
          select.disabled = !options.length;
        };
        const books = [...new Set(passages.map((entry) => entry.book))];
        setOptions(bookSelectEl, books.map((book) => [book, book]), item?.book);
        const bookPassages = passages.filter((entry) => entry.book === item?.book);
        const chapters = [...new Set(bookPassages.map((entry) => parseCitation(entry.citation).startChapter))];
        const chapter = item ? parseCitation(item.citation).startChapter : "";
        setOptions(chapterSelectEl, chapters.map((number) => [String(number), String(number)]), String(chapter));
        const sections = bookPassages.filter((entry) => parseCitation(entry.citation).startChapter === chapter);
        setOptions(passageSelectEl, sections.map((entry) => [
          `${entry.citation}${entry.section_title ? ` · ${entry.section_title}` : ""}`, entry.id,
        ]), item?.id);
      }

      function openDrawer() {
        if (navDrawerEl.open) return;
        returnDrawerFocus = true;
        browseBtnEl.focus({ preventScroll: true });
        navDrawerEl.showModal();
        document.body.classList.add("kb-nav-open");
        browseBtnEl.setAttribute("aria-expanded", "true");
        navEl.querySelector(".is-active")?.scrollIntoView({ block: "nearest", behavior: "instant" });
      }

      function closeDrawer(restoreFocus = true) {
        if (!navDrawerEl.open) return;
        returnDrawerFocus = restoreFocus !== false;
        navDrawerEl.close();
        finishClosingDrawer();
      }

      function finishClosingDrawer() {
        if (navDrawerEl.open) return;
        document.body.classList.remove("kb-nav-open");
        browseBtnEl.setAttribute("aria-expanded", "false");
        if (returnDrawerFocus) browseBtnEl.focus({ preventScroll: true });
      }

      function getGroups() {
        const items = getCurrentItems();
        if (activeType === "passages") {
          return buildPassageBooks();
        }
        if (activeType === "studies" && navView === "alpha") {
          return [
            {
              key: "all-studies",
              label: "All Studies",
              items: items.slice().sort(compareStudyTitles),
            },
          ];
        }
        if (activeType === "studies" && navView === "topic") {
          const groups = new Map();
          items.forEach((item) => {
            const topic = getStudyTopic(item);
            if (!groups.has(topic)) groups.set(topic, []);
            groups.get(topic).push(item);
          });
          const topicOrder = LIBRARY_DATA.study_topic_order || [];
          return Array.from(groups.entries())
            .sort((a, b) => {
              const ai = topicOrder.indexOf(a[0]);
              const bi = topicOrder.indexOf(b[0]);
              const ar = ai === -1 ? Number.MAX_SAFE_INTEGER : ai;
              const br = bi === -1 ? Number.MAX_SAFE_INTEGER : bi;
              return ar - br || a[0].localeCompare(b[0]);
            })
            .map(([key, groupedItems]) => ({
              key,
              label: key,
              items: groupedItems.slice().sort(compareStudyTitles),
            }));
        }

        const groups = {};
        items.forEach((item) => {
          const key = activeType === "passages"
            ? (item.book || "Other")
            : item.title;
          if (!groups[key]) groups[key] = [];
          groups[key].push(item);
        });
        const order = activeType === "passages" && navView === "book"
          ? (LIBRARY_DATA.book_order || [])
          : [];
        return Object.keys(groups)
          .sort((a, b) => {
            const ai = order.indexOf(a);
            const bi = order.indexOf(b);
            const ar = ai === -1 ? Number.MAX_SAFE_INTEGER : ai;
            const br = bi === -1 ? Number.MAX_SAFE_INTEGER : bi;
            return ar - br || normalizeBookLabel(a).localeCompare(normalizeBookLabel(b)) || a.localeCompare(b);
          })
          .map((key) => ({ key, label: key, items: groups[key] }));
      }

      function filterGroups(groups) {
        const query = navFilter.trim().toLowerCase();
        if (!query) return groups;

        if (activeType === "passages") {
          return groups
            .map((book) => {
              const bookMatches = book.label.toLowerCase().includes(query);
              const chapters = book.chapters
                .map((chapter) => {
                  const chapterMatches = `${chapter.chapterNumber}`.includes(query) || chapter.label.toLowerCase().includes(query);
                  const items = chapter.items.filter((item) => {
                    const parts = [
                      item.title,
                      item.section_title || "",
                      item.citation || "",
                      `${item.book} ${item.citation}`,
                    ];
                    return parts.join(" ").toLowerCase().includes(query);
                  });
                  if (bookMatches || chapterMatches) {
                    return chapter;
                  }
                  if (!items.length) return null;
                  return { ...chapter, items };
                })
                .filter(Boolean);
              if (bookMatches) return book;
              if (!chapters.length) return null;
              const items = chapters.flatMap((chapter) => chapter.items);
              return { ...book, items, chapters };
            })
            .filter(Boolean);
        }

        return groups
          .map((group) => {
            const groupMatches = group.label.toLowerCase().includes(query);
            if (groupMatches) return group;
            const items = group.items.filter((item) => {
              const parts = [item.title, item.subtitle || "", item.summary || ""];
              return parts.join(" ").toLowerCase().includes(query);
            });
            if (!items.length) return null;
            return { ...group, items };
          })
          .filter(Boolean);
      }

      function renderNav() {
        navEl.innerHTML = "";
        const groups = filterGroups(getGroups());
        if (!groups.length) {
          navEl.innerHTML = '<p class="kb-paragraph">No navigation matches that filter.</p>';
          return;
        }

        if (!activeId) {
          activeId = groups[0].items[0] ? groups[0].items[0].id : "";
        }

        if (activeType === "studies" && navView === "alpha") {
          const items = groups[0].items.slice().sort(compareStudyTitles);
          const list = document.createElement("ul");
          list.className = "kb-nav-list kb-nav-flat-list";
          items.forEach((item) => {
            const li = document.createElement("li");
            li.className = "kb-nav-item";
            const btn = document.createElement("button");
            btn.className = item.id === activeId ? "is-active" : "";
            btn.textContent = item.title;
            btn.addEventListener("click", () => {
              selectLibraryItem(item.id);
            });
            li.appendChild(btn);
            list.appendChild(li);
          });
          navEl.appendChild(list);
          return;
        }

        if (activeType === "passages") {
          groups.forEach((book) => {
            const bookKey = `${activeType}:book:${book.key}`;
            const bookWrap = document.createElement("section");
            bookWrap.className = "kb-nav-group";

            const bookBtn = document.createElement("button");
            bookBtn.className = "kb-nav-group-toggle";
            const bookCollapsed = navFilter ? false : collapsedGroups.has(bookKey);
            bookBtn.setAttribute("aria-expanded", bookCollapsed ? "false" : "true");
            bookBtn.innerHTML = `<span>${book.label}</span><span class="kb-chevron">${bookCollapsed ? "▸" : "▾"}</span>`;
            bookBtn.addEventListener("click", () => {
              if (collapsedGroups.has(bookKey)) collapsedGroups.delete(bookKey);
              else collapsedGroups.add(bookKey);
              renderNav();
            });
            bookWrap.appendChild(bookBtn);

            const chapterList = document.createElement("div");
            chapterList.className = "kb-nav-list kb-nav-subgroups";
            if (bookCollapsed) chapterList.style.display = "none";

            book.chapters.forEach((chapter) => {
              const chapterKey = `${activeType}:chapter:${book.key}:${chapter.chapterNumber}`;
              const chapterWrap = document.createElement("section");
              chapterWrap.className = "kb-nav-subgroup";

              const chapterBtn = document.createElement("button");
              chapterBtn.className = "kb-nav-subgroup-toggle";
              const chapterCollapsed = navFilter ? false : collapsedGroups.has(chapterKey);
              chapterBtn.setAttribute("aria-expanded", chapterCollapsed ? "false" : "true");
              chapterBtn.innerHTML = `<span>${chapter.label}</span><span class="kb-chevron">${chapterCollapsed ? "▸" : "▾"}</span>`;
              chapterBtn.addEventListener("click", () => {
                if (collapsedGroups.has(chapterKey)) collapsedGroups.delete(chapterKey);
                else collapsedGroups.add(chapterKey);
                renderNav();
              });
              chapterWrap.appendChild(chapterBtn);

              const sectionList = document.createElement("ul");
              sectionList.className = "kb-nav-list kb-nav-section-list";
              if (chapterCollapsed) sectionList.style.display = "none";

              chapter.items.forEach((item) => {
                const li = document.createElement("li");
                li.className = "kb-nav-item";
                const btn = document.createElement("button");
                btn.className = `kb-section-link${item.id === activeId ? " is-active" : ""}`;
                const isSingleVerse = item.parsedCitation.startVerse === item.parsedCitation.endVerse
                  && item.parsedCitation.startChapter === item.parsedCitation.endChapter;
                btn.innerHTML = `
                  <span class="kb-section-range" aria-hidden="true">
                    <span class="kb-section-verse-start">${item.parsedCitation.startVerse}</span>
                    <span class="kb-section-range-dash">${isSingleVerse ? "" : "-"}</span>
                    <span class="kb-section-verse-end">${isSingleVerse ? "" : item.parsedCitation.endVerse}</span>
                  </span>
                  <span class="kb-section-title-text">${compactSectionLabel(item.section_title || item.title)}</span>
                `;
                btn.setAttribute("aria-label", `${item.title}${item.section_title ? ` — ${item.section_title}` : ""}`);
                btn.addEventListener("click", () => {
                  selectLibraryItem(item.id);
                });
                li.appendChild(btn);
                sectionList.appendChild(li);
              });

              chapterWrap.appendChild(sectionList);
              chapterList.appendChild(chapterWrap);
            });

            bookWrap.appendChild(chapterList);
            navEl.appendChild(bookWrap);
          });
          return;
        }

        groups.forEach((group, index) => {
          const key = `${activeType}:${group.key}`;
          const wrap = document.createElement("section");
          wrap.className = "kb-nav-group";

          const headerBtn = document.createElement("button");
          headerBtn.className = "kb-nav-group-toggle";
          const shouldCollapse = navFilter ? false : collapsedGroups.has(key);
          headerBtn.setAttribute("aria-expanded", shouldCollapse ? "false" : "true");
          headerBtn.innerHTML = `<span>${group.label}</span><span class="kb-chevron">${shouldCollapse ? "▸" : "▾"}</span>`;
          headerBtn.addEventListener("click", () => {
            if (collapsedGroups.has(key)) {
              collapsedGroups.delete(key);
            } else {
              collapsedGroups.add(key);
            }
            renderNav();
          });
          wrap.appendChild(headerBtn);

          const list = document.createElement("ul");
          list.className = "kb-nav-list";
          if (shouldCollapse) list.style.display = "none";
          group.items
            .slice()
            .sort((a, b) => a.title.localeCompare(b.title))
            .forEach((item) => {
              const li = document.createElement("li");
              li.className = "kb-nav-item";
              const btn = document.createElement("button");
              btn.className = item.id === activeId ? "is-active" : "";
              btn.textContent = item.title;
              btn.addEventListener("click", () => {
                selectLibraryItem(item.id);
              });
              li.appendChild(btn);
              list.appendChild(li);
            });
          wrap.appendChild(list);
          navEl.appendChild(wrap);

          if (index === 0 && !activeId) {
            activeId = group.items[0] ? group.items[0].id : "";
          }
        });
      }

      function collapseAllGroups() {
        collapsedGroups.clear();
        if (activeType === "passages") {
          getGroups().forEach((book) => {
            collapsedGroups.add(`${activeType}:book:${book.key}`);
            book.chapters.forEach((chapter) => {
              collapsedGroups.add(`${activeType}:chapter:${book.key}:${chapter.chapterNumber}`);
            });
          });
        } else if (activeType === "studies" && navView === "topic") {
          getGroups().forEach((group) => {
            collapsedGroups.add(`${activeType}:${group.key}`);
          });
        }
      }

      function renderStudy(item) {
        return `
          <p class="kb-breadcrumb">Library / Studies / ${item.title}</p>
          <h2 class="kb-article-title">${item.title}</h2>
          ${item.subtitle ? `<p class="article-subtitle">${item.subtitle}</p>` : ""}
          <p class="kb-meta">Primary Translation: ${item.translation}</p>
          <p class="kb-paragraph">${item.summary}</p>
          <p class="kb-paragraph"><a href="${item.href}">Open study page</a></p>
        `;
      }

      function escapeHtml(value) {
        return String(value || "").replace(/[&<>"']/g, (character) => ({
          "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;",
        }[character]));
      }

      function renderPassageNavigation(item) {
        // The library index uses canonical book and numeric chapter/verse order.
        // Use the complete sequence, regardless of the current search or view.
        const passages = LIBRARY_DATA.passages || [];
        const position = passages.findIndex((entry) => entry.id === item.id);
        if (position === -1) return "";
        const link = (entry, direction) => {
          if (!entry) return "";
          const label = direction === "previous" ? "← Previous passage" : "Next passage →";
          const relation = direction === "previous" ? "prev" : "next";
          return `<a class="passage-navigation-link passage-navigation-${direction}" href="${escapeHtml(entry.href)}" rel="${relation}" data-passage-id="${escapeHtml(entry.id)}">
            <span class="passage-navigation-label">${label}</span>
            <strong>${escapeHtml(entry.title)}</strong>
            ${entry.section_title ? `<span class="passage-navigation-title">${escapeHtml(entry.section_title)}</span>` : ""}
          </a>`;
        };
        const links = link(passages[position - 1], "previous") + link(passages[position + 1], "next");
        return links ? `<nav class="passage-navigation" aria-label="Passage navigation">${links}</nav>` : "";
      }

      function navigatePassage(id) {
        if (!(LIBRARY_DATA.passages || []).some((item) => item.id === id)) return;
        // Reveal the destination even when the previous passage was filtered.
        navFilter = "";
        navSearchEl.value = "";
        selectLibraryItem(id);
      }

      function selectLibraryItem(id) {
        if (!getCurrentItems().some((item) => item.id === id)) return;
        searchEl.value = "";
        hideResults();
        renderArticle(id);
        renderNav();
        closeDrawer(false);
        const heading = articleEl.querySelector(".kb-article-title");
        heading.setAttribute("tabindex", "-1");
        heading.focus({ preventScroll: true });
        heading.scrollIntoView({ block: "start", behavior: "instant" });
      }

      function renderPassage(item) {
        const displayLabel = (label) => label === "BSB" ? "Berean Standard Bible" : label;
        const renderVersionParagraphs = (version) => {
          const paragraphs = Array.isArray(version.paragraphs) && version.paragraphs.length
            ? version.paragraphs
            : (version.text ? [version.text] : []);
          return paragraphs.map((paragraph) => `<p>${paragraph}</p>`).join("");
        };
        const versions = item.versions && item.versions.length
          ? item.versions.map((version) => `
              <div class="passage-version">
                <h2>${displayLabel(version.label)}</h2>
                <blockquote>${renderVersionParagraphs(version)}</blockquote>
              </div>
            `).join("")
          : `<p class="kb-paragraph">Full passage text for this reference is not yet quoted in the current local source material.</p>`;
        const deeperStudy = item.deeper_study && item.deeper_study.length
          ? `<ul class="study-link-list">${item.deeper_study.map((study) => `<li><a href="${study.href}">${study.title}</a></li>`).join("")}</ul>`
          : `<p class="kb-paragraph">No deeper study linked yet.</p>`;
        return `
          <p class="kb-breadcrumb">Library / Passages / ${item.book} / ${item.title}</p>
          <h2 class="kb-article-title">${item.title}</h2>
          ${item.section_title ? `<p class="article-subtitle">${item.section_title}</p>` : ""}
          ${item.note ? `<p class="kb-paragraph">${item.note}</p>` : ""}
          ${versions}
          <h3 class="kb-section-title">${item.section_headings?.context || "Context"}</h3>
          ${item.context_html}
          <h3 class="kb-section-title">${item.section_headings?.common || "Common Interpretations"}</h3>
          ${item.common_interpretations_html}
          ${item.god_plan_html ? `<h3 class="kb-section-title">${item.section_headings?.plan || "Where does this fit in God's plan?"}</h3>${item.god_plan_html}` : ""}
          <h3 class="kb-section-title">${item.section_headings?.position || "Current Position"}</h3>
          ${item.current_position_html}
          <h3 class="kb-section-title">${item.section_headings?.deeper || "Deeper Study"}</h3>
          ${deeperStudy}
          ${renderPassageNavigation(item)}
        `;
      }

      function renderArticle(id) {
        const item = getCurrentItems().find((entry) => entry.id === id) || getCurrentItems()[0];
        syncPassageSelectors(item);
        if (!item) {
          activeId = "";
          articleEl.innerHTML = '<p class="kb-paragraph">No content is available yet.</p>';
          syncQuery();
          return;
        }
        activeId = item.id;
        articleEl.innerHTML = activeType === "studies" ? renderStudy(item) : renderPassage(item);
        if (activeType === "passages") {
          const parsed = parseCitation(item.citation);
          collapsedGroups.delete(`passages:book:${item.book}`);
          collapsedGroups.delete(`passages:chapter:${item.book}:${parsed.startChapter}`);
          articleEl.querySelectorAll(".passage-navigation a").forEach((link) => {
            link.addEventListener("click", (event) => {
              if (event.button !== 0 || event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
              event.preventDefault();
              navigatePassage(link.dataset.passageId);
            });
          });
        }
        syncQuery();
      }

      function hideResults() {
        resultsEl.classList.remove("is-visible");
        resultsEl.innerHTML = "";
      }

      function renderResults(query) {
        const q = query.trim().toLowerCase();
        if (!q) {
          hideResults();
          return;
        }
        const hits = getCurrentItems().filter((item) => {
          const parts = [item.title, item.summary || "", item.subtitle || "", item.book || "", item.note || ""];
          return parts.join(" ").toLowerCase().includes(q);
        });
        resultsEl.classList.add("is-visible");
        if (!hits.length) {
          resultsEl.innerHTML = '<div class="kb-result-item"><h4>No results</h4><p>Try searching by study title, passage, or biblical book.</p></div>';
          return;
        }
        resultsEl.innerHTML = hits.map((item) => `
          <button class="kb-result-item" type="button" data-id="${escapeHtml(item.id)}">
            <strong>${escapeHtml(item.title)}</strong>
            <span>${activeType === "studies" ? "Study" : escapeHtml(item.book)}</span>
          </button>
        `).join("");
        resultsEl.querySelectorAll(".kb-result-item[data-id]").forEach((el) => {
          el.addEventListener("click", () => {
            selectLibraryItem(el.dataset.id);
          });
        });
      }

      async function initLibrary() {
        try {
          const res = await fetch("../assets/library_index.json", { cache: "no-store" });
          LIBRARY_DATA = await res.json();
        } catch (e) {
          LIBRARY_DATA = { studies: [], passages: [], book_order: [] };
        }

        const params = new URLSearchParams(window.location.search);
        activeType = "passages";
        const requestedView = params.get("view");
        navView = requestedView === "az" ? "alpha" : (requestedView || (activeType === "passages" ? "book" : "alpha"));
        syncViewOptions();
        syncNavFilterPlaceholder();
        syncNavActionVisibility();
        syncPassageGuideVisibility();
        activeId = getCurrentItems().some((item) => item.id === params.get("passage")) && activeType === "passages"
          ? params.get("passage")
          : (getCurrentItems()[0] ? getCurrentItems()[0].id : "");
        collapseAllGroups();
        syncQuery();
        renderArticle(activeId);
        renderNav();

        viewSelectEl.addEventListener("change", () => {
          navView = viewSelectEl.value;
          collapsedGroups.clear();
          syncNavFilterPlaceholder();
          syncNavActionVisibility();
          syncPassageGuideVisibility();
          syncQuery();
          collapseAllGroups();
          renderNav();
        });

        navSearchEl.addEventListener("input", (e) => {
          navFilter = e.target.value || "";
          renderNav();
        });

        browseBtnEl.addEventListener("click", () => {
          if (document.body.classList.contains("kb-nav-open")) closeDrawer();
          else openDrawer();
        });

        closeBtnEl.addEventListener("click", closeDrawer);
        navDrawerEl.addEventListener("close", finishClosingDrawer);
        navDrawerEl.addEventListener("click", (event) => {
          if (event.target !== navDrawerEl) return;
          const bounds = navDrawerEl.getBoundingClientRect();
          if (event.clientX < bounds.left || event.clientX > bounds.right
            || event.clientY < bounds.top || event.clientY > bounds.bottom) closeDrawer();
        });

        bookSelectEl.addEventListener("change", () => {
          const destination = (LIBRARY_DATA.passages || []).find((item) => item.book === bookSelectEl.value);
          if (destination) navigatePassage(destination.id);
        });
        chapterSelectEl.addEventListener("change", () => {
          const destination = (LIBRARY_DATA.passages || []).find((item) =>
            item.book === bookSelectEl.value && parseCitation(item.citation).startChapter === Number(chapterSelectEl.value)
          );
          if (destination) navigatePassage(destination.id);
        });
        passageSelectEl.addEventListener("change", () => navigatePassage(passageSelectEl.value));

        expandAllEl.addEventListener("click", () => {
          collapsedGroups.clear();
          renderNav();
        });

        collapseAllEl.addEventListener("click", () => {
          collapseAllGroups();
          renderNav();
        });

        searchEl.addEventListener("input", (e) => renderResults(e.target.value));
      }

      initLibrary();
    </script>
  </body>
</html>
"""


def library_index_data(
    studies: list[Study],
    reference_map: dict[PassageReference, list[Study]],
    grouped_references: dict[str, list[PassageReference]],
) -> str:
    studies_payload = [
        {
            "id": study.slug,
            "title": study.title,
            "subtitle": study.subtitle,
            "summary": study.summary,
            "topic": STUDY_TOPIC_MAP.get(study.source_name, "Other Studies"),
            "translation": study.translation,
            "href": f"../studies/{study.slug}.html",
        }
        for study in studies
    ]

    ordered_books = sorted(
        grouped_references.keys(),
        key=lambda book: (BOOK_ORDER.index(book) if book in BOOK_ORDER else 10_000, sort_key_without_numeric_prefix(book)),
    )

    passages_payload = []
    for book in ordered_books:
        refs = sorted(grouped_references[book], key=passage_sort_key)
        for ref in refs:
            passages_payload.append(passage_payload(ref, reference_map.get(ref, [])))

    payload = {
        "studies": studies_payload,
        "passages": passages_payload,
        "book_order": ordered_books,
        "study_topic_order": STUDY_TOPIC_ORDER,
    }
    return json.dumps(payload, ensure_ascii=True, indent=2)


def studies_redirect_html() -> str:
    return """<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta http-equiv="refresh" content="0; url=../library/index.html" />
    <title>Redirecting...</title>
  </head>
  <body>
    <p><a href="../library/index.html">Go to the library.</a></p>
  </body>
</html>
"""


def refresh_reviewed_passages(slugs: list[str]) -> None:
    """Publish reviewed sources, admitting new groups without rewriting other prose."""
    index_path = WEB_DIR / "assets" / "library_index.json"
    data = json.loads(index_path.read_text(encoding="utf-8"))
    passages = data["passages"]
    by_slug = {item["id"]: index for index, item in enumerate(passages)}
    if len(by_slug) != len(passages):
        raise ValueError("Duplicate published passage IDs")
    old_navigation = {
        item["id"]: render_passage_navigation(
            passages[i - 1] if i else None,
            passages[i + 1] if i + 1 < len(passages) else None,
        )
        for i, item in enumerate(passages)
    }
    KNOWN_PASSAGE_REFERENCES.clear()
    KNOWN_PASSAGE_REFERENCES.update(PassageReference(item["book"], item["citation"]) for item in passages)
    STUDY_LINKS.clear()
    STUDY_LINKS.update({item["title"]: item["id"] for item in data["studies"]})
    selected = []
    for slug in dict.fromkeys(slugs):
        is_new = slug not in by_slug
        if is_new:
            if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", slug):
                raise ValueError(f"Invalid passage ID: {slug}")
            source_path = PASSAGE_SOURCE_DIR / f"{slug}.json"
            if not source_path.is_file():
                raise ValueError(f"Passage source is missing: {slug}")
            raw_reference = json.loads(source_path.read_text(encoding="utf-8")).get("reference", {})
            reference = PassageReference(raw_reference.get("book", ""), raw_reference.get("citation", ""))
            if reference.book not in BOOK_ORDER or reference.slug != slug:
                raise ValueError(f"Source reference does not match a canonical passage ID: {slug}")
            passage_sort_key(reference)  # Reject malformed ranges before preparing output.
        else:
            item = passages[by_slug[slug]]
            reference = PassageReference(item["book"], item["citation"])
        content = load_passage_source_content(reference)
        if not content or content.editorial_review.get("standard") != "passage-v1":
            raise ValueError(f"Reviewed passage-v1 source is required: {slug}")
        if [version.label for version in content.verses] != ["BSB"]:
            raise ValueError(f"Only a verified BSB source may be published: {slug}")
        path = PASSAGES_DIR / f"{slug}.html"
        if not is_new and not path.exists():
            raise ValueError(f"Published page is missing: {slug}")
        selected.append((path, reference))
        if is_new:
            by_slug[slug] = len(passages)
            passages.append({"id": slug, "book": reference.book, "citation": reference.citation})
            KNOWN_PASSAGE_REFERENCES.add(reference)
    # Prepare every reference before rendering so links and neighbor descriptions
    # are independent of input order, including when the batch adds a new book.
    for _, reference in selected:
        position = by_slug[reference.slug]
        passages[position] = {**passages[position], **passage_payload(reference, [])}
    additions = set(by_slug) - set(old_navigation)
    if additions:
        passages.sort(key=lambda item: passage_sort_key(PassageReference(item["book"], item["citation"])))
        books = set(data.get("book_order", [])) | {item["book"] for item in passages}
        data["book_order"] = sorted(books, key=lambda book: (
            BOOK_ORDER.index(book) if book in BOOK_ORDER else len(BOOK_ORDER), book,
        ))
        by_slug = {item["id"]: position for position, item in enumerate(passages)}
    # Neighbor descriptions must come from the complete updated batch, even
    # when a neighbor is selected later in the input order.
    updates = []
    for path, reference in selected:
        position = by_slug[reference.slug]
        page = passage_page_html(reference, [])
        navigation = render_passage_navigation(
            passages[position - 1] if position else None,
            passages[position + 1] if position + 1 < len(passages) else None,
        )
        updates.append((path, insert_passage_navigation(page, navigation)))
    selected_ids = {reference.slug for _, reference in selected}
    for position, item in enumerate(passages):
        slug = item["id"]
        if slug in selected_ids or slug not in old_navigation:
            continue
        navigation = render_passage_navigation(
            passages[position - 1] if position else None,
            passages[position + 1] if position + 1 < len(passages) else None,
        )
        if navigation == old_navigation[slug]:
            continue
        path = PASSAGES_DIR / f"{slug}.html"
        # Existing neighbors receive navigation only, for changed destinations
        # or descriptions. A missing/malformed neighbor fails preparation before
        # any published file is written, even for a batch without new groups.
        updates.append((path, insert_passage_navigation(path.read_text(encoding="utf-8"), navigation)))
    updates.append((index_path, json.dumps(data, ensure_ascii=True, indent=2)))
    updates.append((LIBRARY_DIR / "passages.html", passages_page_html()))
    # Prepare the complete batch first; failures above leave published files intact.
    for path, text in updates:
        path.write_text(text, encoding="utf-8")


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    LIBRARY_DIR.mkdir(parents=True, exist_ok=True)
    PASSAGES_DIR.mkdir(parents=True, exist_ok=True)
    PASSAGE_SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    studies = []
    for path in sorted(SOURCE_DIR.glob("*.md")):
        studies.append(parse_study(path))

    guided_rank = {slug: index for index, (slug, _) in enumerate(GUIDED_STUDY_STEPS)}
    source_slugs = {study.slug for study in studies}
    if len(guided_rank) != len(GUIDED_STUDY_STEPS) or source_slugs != set(guided_rank):
        raise ValueError(
            "Guided study order must cover every source study exactly once; "
            f"missing={sorted(source_slugs - set(guided_rank))}, "
            f"unknown={sorted(set(guided_rank) - source_slugs)}"
        )
    studies.sort(key=lambda study: guided_rank[study.slug])

    reference_map: dict[PassageReference, list[Study]] = defaultdict(list)
    grouped_references: dict[str, list[PassageReference]] = defaultdict(list)
    for study in studies:
        for reference in study.references:
            reference_map[reference].append(study)
            if reference not in grouped_references[reference.book]:
                grouped_references[reference.book].append(reference)

    source_references = set(standalone_passage_references())
    for reference in source_references:
        if reference not in grouped_references[reference.book]:
            grouped_references[reference.book].append(reference)
        reference_map.setdefault(reference, [])

    alias_map: dict[PassageReference, PassageReference] = {}
    for reference in list(reference_map.keys()):
        alias_target = resolve_alias_reference(reference, source_references)
        if not alias_target:
            continue
        alias_map[reference] = alias_target
        linked_studies = reference_map.pop(reference)
        for study in linked_studies:
            if study not in reference_map[alias_target]:
                reference_map[alias_target].append(study)
        if reference in grouped_references.get(reference.book, []):
            grouped_references[reference.book] = [
                item for item in grouped_references[reference.book] if item != reference
            ]

    KNOWN_PASSAGE_REFERENCES.clear()
    KNOWN_PASSAGE_REFERENCES.update(reference_map.keys())
    KNOWN_PASSAGE_REFERENCES.update(alias_map.keys())
    STUDY_LINKS.clear()
    STUDY_LINKS.update({study.title: study.slug for study in studies})

    ensure_passage_source_files(reference_map)
    write_passage_source_audit(reference_map)

    for study in studies:
        study.intro_html = render_blocks(
            study.intro_lines,
            enable_reference_links=True,
            current_study_slug=study.slug,
        )
        study.body_html = render_blocks(
            study.body_lines,
            enable_reference_links=True,
            current_study_slug=study.slug,
        )

    for study in studies:
        output_path = OUTPUT_DIR / f"{study.slug}.html"
        output_path.write_text(study_page_html(study), encoding="utf-8")

    active_passage_slugs = {reference.slug for reference in reference_map}
    active_passage_slugs.update(reference.slug for reference in alias_map)
    for path in PASSAGES_DIR.glob("*.html"):
        if path.stem not in active_passage_slugs:
            path.unlink()

    for reference, linked_studies in reference_map.items():
        output_path = PASSAGES_DIR / f"{reference.slug}.html"
        output_path.write_text(
            passage_page_html(reference, linked_studies),
            encoding="utf-8",
        )

    for reference, target in alias_map.items():
        output_path = PASSAGES_DIR / f"{reference.slug}.html"
        output_path.write_text(
            passage_redirect_html(reference, target),
            encoding="utf-8",
        )

    (LIBRARY_DIR / "index.html").write_text(library_index_html(studies), encoding="utf-8")
    (LIBRARY_DIR / "studies-all.html").write_text(studies_all_html(studies), encoding="utf-8")
    (LIBRARY_DIR / "passages.html").write_text(passages_page_html(), encoding="utf-8")
    (LIBRARY_DIR / "passages-by-book.html").write_text(
        passages_by_book_html(grouped_references),
        encoding="utf-8",
    )
    (WEB_DIR / "assets" / "library_index.json").write_text(
        library_index_data(studies, reference_map, grouped_references),
        encoding="utf-8",
    )
    (OUTPUT_DIR / "index.html").write_text(studies_redirect_html(), encoding="utf-8")
    refresh_passage_navigation()
    refresh_guided_study()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate study and passage pages")
    parser.add_argument(
        "--navigation-only", action="store_true",
        help="Refresh passage navigation, library ordering and the passage reader without regenerating content",
    )
    parser.add_argument(
        "--guided-only", action="store_true",
        help="Refresh guided study pages and navigation without regenerating content",
    )
    parser.add_argument(
        "--passages-only", nargs="+", metavar="SLUG",
        help="Refresh only named, reviewed passage-v1 sources and the reader",
    )
    args = parser.parse_args()
    if sum(bool(value) for value in (args.navigation_only, args.guided_only, args.passages_only)) > 1:
        parser.error("Choose only one focused refresh")
    if args.passages_only:
        refresh_reviewed_passages(args.passages_only)
    elif args.guided_only:
        refresh_guided_study()
    elif args.navigation_only:
        refresh_passage_navigation()
    else:
        main()
