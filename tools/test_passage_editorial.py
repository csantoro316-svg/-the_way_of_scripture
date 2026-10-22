"""Focused regression checks for reviewed passage publication."""
import json
from contextlib import ExitStack
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

import generate_study_pages as generator
from verify_bsb_passages import biblehub_verses, quotation_matches
from validate_passages import validate_editorial_review


class EditorialTests(unittest.TestCase):
    def content(self, **changes):
        values = dict(verses=[], context_lines=["First paragraph.", "", "Second paragraph."],
                      common_interpretation_lines=["A reading."],
                      current_position_lines=[generator.NO_PASSAGE_POSITION], deeper_study=[],
                      editorial_review={"standard": "passage-v1"})
        values.update(changes)
        return generator.PassageContent(**values)

    def test_citations_do_not_nest_auto_links_and_escape_html(self):
        reference = generator.PassageReference("Genesis", "1:1-31")
        rendered = generator.render_passage_lines([
            '[Genesis 2:1-3 <check>](https://example.com/source?a=1&b=2)',
            '', '[Unsafe](javascript:alert)'
        ], reference)
        self.assertEqual(rendered.count('<a '), 1)
        self.assertIn('Genesis 2:1-3 &lt;check&gt;</a>', rendered)
        self.assertIn('a=1&amp;b=2', rendered)
        self.assertNotIn('href="javascript:', rendered)

    def test_plan_is_optional_and_in_order(self):
        ref = generator.PassageReference("Genesis", "1:1-31")
        with patch.object(generator, 'build_passage_content', return_value=self.content()):
            rendered = generator.render_passage_body_sections(ref, [])
        self.assertNotIn("God&#x27;s plan?", rendered)
        with patch.object(generator, 'build_passage_content', return_value=self.content(god_plan_lines=['A documented connection.'])):
            rendered = generator.render_passage_body_sections(ref, [])
        self.assertLess(rendered.index('commonly understood?'), rendered.index('God&#x27;s plan?'))
        self.assertLess(rendered.index('God&#x27;s plan?'), rendered.index('our position?'))
        self.assertEqual(rendered.count('<h2>'), 5)

    def test_source_round_trip_keeps_paragraphs_and_review(self):
        ref = generator.PassageReference("Genesis", "1:1-31")
        original = self.content(god_plan_lines=['First connection.', '', 'Second connection.'])
        with TemporaryDirectory() as directory, patch.object(generator, 'PASSAGE_SOURCE_DIR', Path(directory)):
            generator.passage_source_path(ref).write_text(generator.serialize_passage_content(ref, original))
            loaded = generator.load_passage_source_content(ref)
        self.assertEqual(loaded.context_lines, original.context_lines)
        self.assertEqual(loaded.god_plan_lines, original.god_plan_lines)
        self.assertEqual(loaded.editorial_review, original.editorial_review)
        self.assertEqual(generator.render_passage_lines(loaded.context_lines, ref).count('<p>'), 2)

    def test_biblehub_parser_excludes_headings_footnotes_and_commentary(self):
        raw = '<p class="hdg">Heading<p class="reg"><span class="reftext"><a href="/x"><b>1</b></a></span>First verse.<span class="fn"><a href="#fn">a</a></span><p class="subhdg">Next heading<p class="reg"><span class="reftext"><a href="/y"><b>2</b></a></span>Second verse.<A name="fn"></a>Footnotes and commentary'
        self.assertEqual(biblehub_verses(raw), {1: 'First verse.', 2: 'Second verse.'})
        # Chapters without footnotes reach the copyright box immediately after
        # their final verse. That footer and later summaries are not Scripture.
        no_footnotes = '<span class="reftext"><a href="/x"><b>23</b></a></span>Final verse.</p><p><div id="botbox">Copyright</div><a name="summary">Study notes'
        self.assertEqual(biblehub_verses(no_footnotes), {23: 'Final verse.'})
        with self.assertRaises(ValueError):
            biblehub_verses('Unrecognized page')

    def test_quotation_check_preserves_numbers_within_the_biblical_text(self):
        verses = {3: 'When Adam was 130 years old.', 4: 'Adam lived 800 years.'}
        self.assertTrue(quotation_matches('3 When Adam was 130 years old. 4 Adam lived 800 years.', verses, 3, 4))
        self.assertTrue(quotation_matches('When Adam was 130 years old. Adam lived 800 years.', verses, 3, 4))
        self.assertFalse(quotation_matches('3 When Adam was years old. 4 Adam lived years.', verses, 3, 4))
        self.assertFalse(quotation_matches('3 When Adam was 131 years old. 4 Adam lived 800 years.', verses, 3, 4))
        self.assertFalse(quotation_matches('3 When Adam was 130 years old. 5 Adam lived 800 years.', verses, 3, 4))

    def test_review_validation_rejects_originated_position_and_unsupported_plan(self):
        with TemporaryDirectory() as directory:
            evidence = Path(directory) / 'evidence.md'; evidence.write_text('Evidence')
            payload = {
                'versions': [{'label': 'BSB'}],
                'current_position_lines': ['An invented position.'],
                'god_plan_lines': ['An unsupported connection.'],
                'editorial_review': {'standard':'passage-v1', 'reviewed_on':'2026-10-18',
                    'quote_source':'https://biblehub.com/bsb/genesis/1.htm',
                    'evidence_file':str(evidence), 'position_source':'none', 'plan_basis':[]}
            }
            issues = []
            validate_editorial_review(payload, Path(directory) / 'passage.json', issues)
            self.assertTrue(any('exact approved' in issue.message for issue in issues))
            self.assertTrue(any('inclusion basis' in issue.message for issue in issues))

    def test_focused_publication_adds_reviewed_groups_and_preserves_neighbor_prose(self):
        with TemporaryDirectory() as directory, ExitStack() as stack:
            root = Path(directory); web = root/'web'; sources = root/'sources'
            for path in (web/'assets', web/'passages', web/'library', sources): path.mkdir(parents=True)
            for name, value in {'WEB_DIR':web, 'PASSAGES_DIR':web/'passages', 'LIBRARY_DIR':web/'library', 'PASSAGE_SOURCE_DIR':sources,
                                'KNOWN_PASSAGE_REFERENCES':set(), 'STUDY_LINKS':{}}.items():
                stack.enter_context(patch.object(generator, name, value))
            old_refs = [generator.PassageReference(book, citation) for book, citation in
                        [('Genesis','1:1-31'), ('Genesis','3:1-7'), ('Exodus','1:1-7'), ('Exodus','2:1-10'), ('Didache','1:1-6')]]
            items = [{'id':r.slug, 'title':r.label, 'book':r.book, 'citation':r.citation,
                      'href':f'../passages/{r.slug}.html', 'note':'Retain this metadata'} for r in old_refs]
            index_path = web/'assets'/'library_index.json'
            index_path.write_text(json.dumps({'studies':[], 'passages':items, 'book_order':['Genesis','Exodus','Didache']}))
            for i, ref in enumerate(old_refs):
                page = f'<html><article><p>Keep the authored prose for {ref.label}.</p>\n          </article><footer>Keep footer</footer></html>'
                nav = generator.render_passage_navigation(items[i-1] if i else None, items[i+1] if i+1<len(items) else None)
                (web/'passages'/f'{ref.slug}.html').write_text(generator.insert_passage_navigation(page, nav))
            new_refs = [generator.PassageReference('Genesis','2:1-3'), generator.PassageReference('Genesis','2:4-25'),
                        generator.PassageReference('Matthew','1:1-17')]
            for ref in new_refs:
                content = self.content(verses=[generator.PassageVersion(label='BSB', text='Checked quotation')])
                if ref == new_refs[-1]: content.editorial_review.clear()
                (sources/f'{ref.slug}.json').write_text(generator.serialize_passage_content(ref, content))
            before = {p:p.read_bytes() for p in web.rglob('*') if p.is_file()}
            with self.assertRaises(ValueError): generator.refresh_reviewed_passages([r.slug for r in new_refs])
            self.assertEqual(before, {p:p.read_bytes() for p in web.rglob('*') if p.is_file()})
            approved = self.content(verses=[generator.PassageVersion(label='BSB', text='Checked quotation')])
            (sources/f'{new_refs[-1].slug}.json').write_text(generator.serialize_passage_content(new_refs[-1], approved))
            # A missing affected neighbor must also fail before adding any page
            # or changing the index, even after all new sources were approved.
            missing_neighbor = web/'passages'/f'{old_refs[1].slug}.html'
            original_neighbor = missing_neighbor.read_bytes()
            missing_neighbor.unlink()
            incomplete = {p:p.read_bytes() for p in web.rglob('*') if p.is_file()}
            with self.assertRaises(FileNotFoundError): generator.refresh_reviewed_passages([r.slug for r in new_refs])
            self.assertEqual(incomplete, {p:p.read_bytes() for p in web.rglob('*') if p.is_file()})
            missing_neighbor.write_bytes(original_neighbor)
            source_before = {p:p.read_bytes() for p in sources.glob('*.json')}
            generator.refresh_reviewed_passages([r.slug for r in reversed(new_refs)])
            result = json.loads(index_path.read_text())
            self.assertEqual([r['id'] for r in result['passages']], [r.slug for r in
                             [old_refs[0],new_refs[0],new_refs[1],old_refs[1],old_refs[2],old_refs[3],new_refs[2],old_refs[4]]])
            self.assertEqual(result['book_order'], ['Genesis','Exodus','Matthew','Didache'])
            for ref in old_refs:
                path = web/'passages'/f'{ref.slug}.html'
                self.assertEqual(generator.insert_passage_navigation(before[path].decode(), ''),
                                 generator.insert_passage_navigation(path.read_text(), ''))
            untouched = web/'passages'/f'{old_refs[2].slug}.html'
            self.assertEqual(untouched.read_bytes(), before[untouched])
            self.assertIn(new_refs[0].slug, (web/'passages'/f'{old_refs[0].slug}.html').read_text())
            self.assertIn(new_refs[1].slug, (web/'passages'/f'{old_refs[1].slug}.html').read_text())
            self.assertIn(new_refs[2].slug, (web/'passages'/f'{old_refs[-1].slug}.html').read_text())
            self.assertEqual(source_before, {p:p.read_bytes() for p in sources.glob('*.json')})
            for ref in new_refs: self.assertIn('Checked quotation', (web/'passages'/f'{ref.slug}.html').read_text())
            published = {p:p.read_bytes() for p in web.rglob('*') if p.is_file()}
            generator.refresh_reviewed_passages([r.slug for r in new_refs])
            self.assertEqual(published, {p:p.read_bytes() for p in web.rglob('*') if p.is_file()})

    def test_focused_refresh_preserves_others_and_prepares_batch_before_writes(self):
        with TemporaryDirectory() as directory, ExitStack() as stack:
            root = Path(directory); web = root/'web'; sources = root/'sources'
            for path in (web/'assets', web/'passages', web/'library', sources): path.mkdir(parents=True)
            for name, value in {'WEB_DIR':web, 'PASSAGES_DIR':web/'passages', 'LIBRARY_DIR':web/'library', 'PASSAGE_SOURCE_DIR':sources}.items():
                stack.enter_context(patch.object(generator, name, value))
            refs = [generator.PassageReference('Genesis', '1:1-31'), generator.PassageReference('Genesis', '2:1-3')]
            index = {'studies':[], 'passages':[{'id':ref.slug, 'title':ref.label, 'book':ref.book, 'citation':ref.citation, 'href':f'../passages/{ref.slug}.html'} for ref in refs]}
            index_path = web/'assets'/'library_index.json'
            index_path.write_text(json.dumps(index))
            for ref in refs: (web/'passages'/f'{ref.slug}.html').write_text('Existing published content')
            content = self.content(verses=[generator.PassageVersion(label='BSB', text='Verified text')])
            source_path = sources/f'{refs[0].slug}.json'
            source_path.write_text(generator.serialize_passage_content(refs[0], content))
            source_before = source_path.read_bytes(); index_before = index_path.read_bytes()
            with self.assertRaises(ValueError):
                generator.refresh_reviewed_passages([refs[0].slug, refs[1].slug])
            self.assertEqual(index_path.read_bytes(), index_before)
            self.assertEqual((web/'passages'/f'{refs[0].slug}.html').read_text(), 'Existing published content')
            generator.refresh_reviewed_passages([refs[0].slug])
            self.assertEqual((web/'passages'/f'{refs[1].slug}.html').read_text(), 'Existing published content')
            self.assertEqual(source_path.read_bytes(), source_before)
            self.assertEqual(json.loads(index_path.read_text())['passages'][1], index['passages'][1])
            self.assertIn('Next passage', (web/'passages'/f'{refs[0].slug}.html').read_text())
            self.assertTrue((web/'library'/'passages.html').is_file())
            # Adjacent pages must use a renamed destination in the first batch,
            # independent of the order in which the sources are selected.
            updated = self.content(verses=content.verses, section_title='Updated next description')
            (sources/f'{refs[1].slug}.json').write_text(generator.serialize_passage_content(refs[1], updated))
            first_page = web/'passages'/f'{refs[0].slug}.html'
            original_first = first_page.read_bytes()
            # A rename must refresh an unselected neighbor, and a missing
            # neighbor must fail before writing even without any new groups.
            first_page.unlink()
            incomplete = {path: path.read_bytes() for path in web.rglob('*') if path.is_file()}
            with self.assertRaises(FileNotFoundError):
                generator.refresh_reviewed_passages([refs[1].slug])
            self.assertEqual(incomplete, {path: path.read_bytes() for path in web.rglob('*') if path.is_file()})
            first_page.write_bytes(original_first)
            generator.refresh_reviewed_passages([refs[1].slug])
            self.assertIn('Updated next description', first_page.read_text())
            self.assertEqual(generator.insert_passage_navigation(original_first.decode(), ''),
                             generator.insert_passage_navigation(first_page.read_text(), ''))
            generator.refresh_reviewed_passages([ref.slug for ref in refs])
            published = {path: path.read_bytes() for path in web.rglob('*') if path.is_file()}
            generator.refresh_reviewed_passages([ref.slug for ref in reversed(refs)])
            self.assertEqual(published, {path: path.read_bytes() for path in web.rglob('*') if path.is_file()})


if __name__ == '__main__':
    unittest.main()
