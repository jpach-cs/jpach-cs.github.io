'''
Unit tests for tools/pptx2marp.py.

Every deck used here is assembled in memory by pptx_builder from hand-written OOXML,
so each test states exactly which structure it is exercising. Nothing on disk,
nothing binary, no PowerPoint.
'''

from __future__ import annotations

import contextlib
import io
import logging
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

import pytest

import pptx2marp
import pptx2marp_images
from pptx_builder import (
    XMLNS,
    build_pptx,
    diagram,
    graphic_frame,
    notes_xml,
    para,
    pic,
    pic_without_blip,
    presentation_xml,
    rels_xml,
    run,
    shape_xml,
    simple_deck,
    slide_xml,
    table,
    write_pptx,
)

PNG = b'\x89PNG\r\n\x1a\n' + b'\x00' * 8


def parse(xml: str):
    '''Parse a fragment that uses the a:/p:/r: prefixes into an Element.'''
    return ET.fromstring(f'<root {XMLNS}>{xml}</root>')[0]


OPEN_ZIPS = contextlib.ExitStack()


@pytest.fixture(autouse=True, scope='module')
def close_open_zips():
    '''Close every archive opened through open_deck once the module is done.'''
    yield
    OPEN_ZIPS.close()


def open_deck(data: bytes):
    '''
    Open in-memory deck bytes as (ZipFile, names). The archive stays open for the
    life of the module so tests can hand it around freely.
    '''
    archive = OPEN_ZIPS.enter_context(zipfile.ZipFile(io.BytesIO(data)))
    return archive, set(archive.namelist())


def convert(tmp_path: Path, data: bytes, name: str = 'deck.pptx', **kwargs) -> pptx2marp.DeckResult:
    '''Write deck bytes to tmp_path and convert them.'''
    return pptx2marp.convert_deck(write_pptx(tmp_path / name, data), **kwargs)


# --- pure text helpers -----------------------------------------------------------------


def test_qn_builds_clark_notation():
    '''Qn builds clark notation.'''
    assert pptx2marp.qn('a', 't') == '{http://schemas.openxmlformats.org/drawingml/2006/main}t'


def test_escape_text_escapes_html_significant_characters():
    '''Escape text escapes html significant characters.'''
    assert pptx2marp.escape_text('a < b && c > d') == 'a &lt; b &amp;&amp; c &gt; d'


def test_escape_text_escapes_markdown_significant_characters_and_tabs():
    '''Escape text escapes markdown significant characters and tabs.'''
    assert pptx2marp.escape_text('[a]\t`b`\t__c__ /* d */') == \
        '\\[a\\]    \\`b\\`    \\_\\_c\\_\\_ /\\* d \\*/'


@pytest.mark.parametrize('text, expected', [
    ('See https://example.com/docs for more.', 'See <https://example.com/docs> for more.'),
    ('Read https://example.com/page.', 'Read <https://example.com/page>.'),
    ('Visit www.example.com today', 'Visit <www.example.com> today'),
    ('Email me at jane@example.com', 'Email me at <jane@example.com>'),
    ('(https://example.com)', '(<https://example.com>)'),
    ('a_b@example.com', '<a_b@example.com>'),
    ('no links here', 'no links here'),
    ('[a] https://example.com', '\\[a\\] <https://example.com>'),
])
def test_escape_and_wrap_urls(text, expected):
    '''Escape and wrap urls.'''
    assert pptx2marp.escape_and_wrap_urls(text) == expected


@pytest.mark.parametrize('text, bold, italic, expected', [
    ('x', True, False, '**x**'),
    (' text ', True, False, ' **text** '),
    ('  ', True, False, '  '),
    (' word', False, True, ' *word*'),
    ('word ', True, True, '***word*** '),
])
def test_wrap_emphasis_moves_whitespace_outside_markers(text, bold, italic, expected):
    '''Wrap emphasis moves whitespace outside markers.'''
    assert pptx2marp.wrap_emphasis(text, bold, italic) == expected


@pytest.mark.parametrize('line, expected', [
    ('# not a heading', '\\# not a heading'),
    ('  > quoted', '  \\> quoted'),
    ('- dash item', '\\- dash item'),
    ('* star item', '\\* star item'),
    ('+ plus item', '\\+ plus item'),
    ('1. numbered', '1\\. numbered'),
    ('-', '\\-'),
    ('---', '\\---'),
    ('  ***  ', '  \\***  '),
    ('-notadash', '-notadash'),
    ('1.5 is a float', '1.5 is a float'),
    ('plain text', 'plain text'),
])
def test_protect_leading_marker(line, expected):
    '''Protect leading marker.'''
    assert pptx2marp.protect_leading_marker(line) == expected


@pytest.mark.parametrize('text, expected', [
    ('plain', '"plain"'),
    ('has "quotes"', '"has \\"quotes\\""'),
    ('back\\slash', '"back\\\\slash"'),
    ('multi\nline\rtext', '"multi line text"'),
    ('colon: yes', '"colon: yes"'),
])
def test_yaml_scalar(text, expected):
    '''Yaml scalar.'''
    assert pptx2marp.yaml_scalar(text) == expected


def test_raw_paragraph_text_joins_runs_fields_and_breaks():
    '''Raw paragraph text joins runs fields and breaks.'''
    paragraph_el = parse(para(run('a'), '<a:br/>', run('b'), '<a:fld><a:t>3</a:t></a:fld>', '<a:r/>'))
    assert pptx2marp.raw_paragraph_text(paragraph_el) == 'a b3'


@pytest.mark.parametrize('text, expected', [
    ('a -- b', 'a - -  b'),
    ('a --- b', 'a - - -  b'),
    ('  a - b  ', 'a - b'),
])
def test_safe_comment_text(text, expected):
    '''Safe comment text.'''
    assert pptx2marp.safe_comment_text(text) == expected


@pytest.mark.parametrize('name, expected', [
    ('ppt/slides/slide10.xml', 10),
    ('ppt/slides/slide2.xml', 2),
    ('ppt/slides/slide.xml', -1),
])
def test_slide_number(name, expected):
    '''Slide number.'''
    assert pptx2marp.slide_number(name) == expected


# --- relationships and slide order -----------------------------------------------------


def test_parse_rels_resolves_internal_and_external_targets():
    '''Parse rels resolves internal and external targets.'''
    rels_part = rels_xml(
        [('rId1', 'image', '../media/a.png'), ('rId2', 'hyperlink', 'https://x.test/')],
        external={'rId2'},
    )
    archive, names = open_deck(build_pptx({'ppt/slides/_rels/slide1.xml.rels': rels_part}))
    relationships = pptx2marp.parse_rels(archive, 'ppt/slides/slide1.xml', names)
    assert relationships['rId1'][1] == 'ppt/media/a.png'
    assert relationships['rId1'][0].endswith('/image')
    assert relationships['rId2'] == (relationships['rId2'][0], 'https://x.test/')


def test_parse_rels_missing_or_malformed_returns_empty():
    '''Parse rels missing or malformed returns empty.'''
    archive, names = open_deck(build_pptx({'ppt/slides/_rels/slide2.xml.rels': '<not xml'}))
    assert not pptx2marp.parse_rels(archive, 'ppt/slides/slide1.xml', names)
    assert not pptx2marp.parse_rels(archive, 'ppt/slides/slide2.xml', names)


def test_get_slide_order_follows_sldidlst_not_filenames():
    '''Get slide order follows sldidlst not filenames.'''
    parts = {
        'ppt/slides/slide1.xml': slide_xml(),
        'ppt/slides/slide2.xml': slide_xml(),
        'ppt/slides/slide10.xml': slide_xml(),
        'ppt/presentation.xml': presentation_xml(['rId10', 'rId1', 'rId2', 'rIdMissing']),
        'ppt/_rels/presentation.xml.rels': rels_xml([
            ('rId1', 'slide', 'slides/slide1.xml'),
            ('rId2', 'slide', 'slides/slide2.xml'),
            ('rId10', 'slide', 'slides/slide10.xml'),
            ('rIdMissing', 'slide', 'slides/slide99.xml'),
        ]),
    }
    archive, names = open_deck(build_pptx(parts))
    assert pptx2marp.get_slide_order(archive, names) == [
        'ppt/slides/slide10.xml', 'ppt/slides/slide1.xml', 'ppt/slides/slide2.xml',
    ]


def test_get_slide_order_falls_back_to_numeric_sort():
    '''Get slide order falls back to numeric sort.'''
    parts = {
        'ppt/slides/slide10.xml': slide_xml(),
        'ppt/slides/slide2.xml': slide_xml(),
        'ppt/slides/slide1.xml': slide_xml(),
        'ppt/slides/_rels/slide1.xml.rels': rels_xml([]),
    }
    archive, names = open_deck(build_pptx(parts))  # no presentation.xml -> KeyError path
    assert pptx2marp.get_slide_order(archive, names) == [
        'ppt/slides/slide1.xml', 'ppt/slides/slide2.xml', 'ppt/slides/slide10.xml',
    ]

    parts['ppt/presentation.xml'] = '<broken'
    archive, names = open_deck(build_pptx(parts))  # ParseError path
    assert len(pptx2marp.get_slide_order(archive, names)) == 3

    parts['ppt/presentation.xml'] = presentation_xml([])
    archive, names = open_deck(build_pptx(parts))  # empty sldIdLst -> fallback
    assert len(pptx2marp.get_slide_order(archive, names)) == 3


# --- run and paragraph rendering -------------------------------------------------------


@pytest.mark.parametrize('kwargs, expected', [
    ({}, 'x'),
    ({'bold': True}, '**x**'),
    ({'italic': True}, '*x*'),
    ({'bold': True, 'italic': True}, '***x***'),
])
def test_render_run_text_formatting(kwargs, expected):
    '''Render run text formatting.'''
    assert pptx2marp.render_run_text(parse(run('x', **kwargs)), {}) == expected


def test_render_run_text_hyperlink_and_escaping():
    '''Render run text hyperlink and escaping.'''
    relationships = {'rId1': ('hyperlink', 'https://x.test/')}
    assert pptx2marp.render_run_text(
        parse(run('<b>', link_rel_id='rId1')), relationships
    ) == '[&lt;b&gt;](https://x.test/)'
    assert pptx2marp.render_run_text(parse(run('t', link_rel_id='rId9')), relationships) == 't'
    assert pptx2marp.render_run_text(
        parse(run('t', link_rel_id='rId1')), {'rId1': ('hyperlink', '')}
    ) == 't'


def test_render_run_text_empty():
    '''Render run text empty.'''
    assert pptx2marp.render_run_text(parse('<a:r><a:t></a:t></a:r>'), {}) == ''
    assert pptx2marp.render_run_text(parse('<a:r/>'), {}) == ''


def test_render_run_text_hyperlink_visible_text_is_not_autolinked():
    '''Render run text hyperlink visible text is not autolinked.'''
    relationships = {'rId1': ('hyperlink', 'https://x.test/')}
    assert pptx2marp.render_run_text(parse(run('https://y.test/', link_rel_id='rId1')), relationships) == \
        '[https://y.test/](https://x.test/)'


def test_render_paragraph_breaks_and_fields():
    '''Render paragraph breaks and fields.'''
    paragraph_el = parse(para(run('a'), '<a:br/>', '<a:fld><a:t>2</a:t></a:fld>', '<a:r/>'))
    assert pptx2marp.render_paragraph(paragraph_el, {}) == 'a<br>2'


def test_render_paragraph_merges_adjacent_runs_with_identical_formatting():
    '''Render paragraph merges adjacent runs with identical formatting.'''
    paragraph_el = parse(para(run('a', bold=True), run('b', bold=True), run('c')))
    assert pptx2marp.render_paragraph(paragraph_el, {}) == '**ab**c'


def test_render_paragraph_does_not_merge_across_breaks_or_differing_formatting():
    '''Render paragraph does not merge across breaks or differing formatting.'''
    paragraph_el = parse(para(
        run('Label: ', bold=True), run('Value', bold=True, italic=True), '<a:br/>', run('x', bold=True),
    ))
    assert pptx2marp.render_paragraph(paragraph_el, {}) == '**Label:** ***Value***<br>**x**'


def test_get_placeholder_type():
    '''Get placeholder type.'''
    assert pptx2marp.get_placeholder_type(parse(shape_xml(ph_type='title'))) == 'title'
    assert pptx2marp.get_placeholder_type(parse(shape_xml())) == 'body'
    assert pptx2marp.get_placeholder_type(parse(shape_xml(has_placeholder=False))) is None


# --- shape iteration -------------------------------------------------------------------


def test_iter_shapes_flattens_groups_and_alternate_content():
    '''Iter shapes flattens groups and alternate content.'''
    xml = (
        f'<p:spTree {XMLNS}>'
        f'<p:grpSp>{shape_xml(ph_type="title")}<p:grpSp>{pic(embed="rId1")}</p:grpSp></p:grpSp>'
        f'<mc:AlternateContent><mc:Choice>{shape_xml()}</mc:Choice>'
        f'<mc:Fallback><p:cxnSp/></mc:Fallback></mc:AlternateContent>'
        f'<mc:AlternateContent><mc:Choice><p:graphicFrame/></mc:Choice></mc:AlternateContent>'
        f'<mc:AlternateContent/>'
        '<p:nvGrpSpPr/>'
        '</p:spTree>'
    )
    tags = [shape.tag for shape in pptx2marp.iter_shapes(ET.fromstring(xml))]
    assert tags == [pptx2marp.P_SP, pptx2marp.P_PIC, pptx2marp.P_CXNSP, pptx2marp.P_GRAPHICFRAME]


# --- tables and diagrams ---------------------------------------------------------------


def test_render_table_pads_ragged_rows_and_escapes_pipes():
    '''Render table pads ragged rows and escapes pipes.'''
    table_el = parse(table([['h1', 'h|2'], ['a'], ['', 'b']])).find(
        f'{pptx2marp.A_GRAPHIC}/{pptx2marp.A_GRAPHICDATA}/{pptx2marp.A_TBL}'
    )
    assert pptx2marp.render_table(table_el, {}).split('\n') == [
        '|h1|h\\|2|',
        '|---|---|',
        '|a||',
        '||b|',
    ]


def test_render_table_empty():
    '''Render table empty.'''
    assert pptx2marp.render_table(parse('<a:tbl/>'), {}) == ''


def test_render_diagram_reads_data_part():
    '''Render diagram reads data part.'''
    data = f'<dgm:dataModel {XMLNS}><dgm:pt><dgm:t><a:p><a:r><a:t># Step</a:t></a:r></a:p></dgm:t></dgm:pt>' \
           f'<dgm:pt><dgm:t><a:p><a:r><a:t>  </a:t></a:r></a:p></dgm:t></dgm:pt></dgm:dataModel>'
    archive, names = open_deck(build_pptx({'ppt/diagrams/data1.xml': data, 'ppt/diagrams/bad.xml': '<x'}))
    graphic_data = parse(diagram('rId5')).find(f'{pptx2marp.A_GRAPHIC}/{pptx2marp.A_GRAPHICDATA}')
    relationships = {'rId5': ('diagramData', 'ppt/diagrams/data1.xml')}
    assert pptx2marp.render_diagram(graphic_data, relationships, archive, names) == ['- \\# Step']
    assert not pptx2marp.render_diagram(
        graphic_data, {'rId5': ('diagramData', 'ppt/diagrams/bad.xml')}, archive, names
    )
    assert not pptx2marp.render_diagram(
        graphic_data, {'rId5': ('diagramData', 'ppt/diagrams/none.xml')}, archive, names
    )
    assert not pptx2marp.render_diagram(graphic_data, {}, archive, names)
    no_relids = parse(graphic_frame('diagram')).find(f'{pptx2marp.A_GRAPHIC}/{pptx2marp.A_GRAPHICDATA}')
    assert not pptx2marp.render_diagram(no_relids, relationships, archive, names)


# --- <p:sp> handling -------------------------------------------------------------------


@pytest.mark.parametrize('title, expected', [
    ('Introduction:', 'Introduction'),
    ('Wrap-up...', 'Wrap-up'),
    ('Section 1, Part 2,', 'Section 1, Part 2'),
    ('Still Interested?', 'Still Interested?'),
    ('Great job!', 'Great job!'),
    (':;.,', ':;.,'),
])
def test_strip_title_punctuation(title, expected):
    '''Strip title punctuation.'''
    assert pptx2marp.strip_title_punctuation(title) == expected


def test_strip_title_punctuation_preserves_html_entity_semicolons():
    '''Strip title punctuation preserves html entity semicolons.'''
    assert pptx2marp.strip_title_punctuation('Salt &amp;') == 'Salt &amp;'


def test_handle_sp_title_subtitle_and_metadata():
    '''Handle sp title subtitle and metadata.'''
    assert pptx2marp.handle_sp(parse(shape_xml(para(run('T <1>')), ph_type='ctrTitle')), {}) == \
        ('title', 'T &lt;1&gt;', 'ctrTitle', 'T <1>')
    assert pptx2marp.handle_sp(parse(shape_xml(para(run('Sub')), ph_type='subTitle')), {}) == \
        ('subtitle', 'Sub', 'subTitle', None)
    assert pptx2marp.handle_sp(parse(shape_xml(para(run('')), ph_type='title')), {}) is None
    assert pptx2marp.handle_sp(parse(shape_xml(para(run('')), ph_type='subTitle')), {}) is None
    assert pptx2marp.handle_sp(parse(shape_xml(para(run('3')), ph_type='sldNum')), {}) is None
    assert pptx2marp.handle_sp(parse(shape_xml(ph_type='body', txbody=False)), {}) is None


def test_handle_sp_body_levels_bullets_and_markers():
    '''Handle sp body levels bullets and markers.'''
    shape = shape_xml(
        para(run('top')),
        para(run('nested'), lvl=1),
        para(run('# no bullet'), bullet=False),
        para(run('   ')),
        para('<a:pPr lvl="x"/>', run('bad lvl')),
    )
    assert pptx2marp.handle_sp(parse(shape), {}) == (
        'body', ['- top', '  - nested', '\\# no bullet', '- bad lvl'], 'body', None,
    )
    assert pptx2marp.handle_sp(parse(shape_xml(para(run('  ')))), {}) is None


def test_handle_sp_strips_leading_whitespace_from_bullet_and_paragraph_text():
    '''Handle sp strips leading whitespace from bullet and paragraph text.'''
    shape = shape_xml(
        para(run('\tindented bullet')),
        para(run('   loose paragraph'), bullet=False),
    )
    assert pptx2marp.handle_sp(parse(shape), {}) == (
        'body', ['- indented bullet', 'loose paragraph'], 'body', None,
    )


def test_handle_sp_drops_whitespace_only_bold_placeholder_bullet():
    '''Handle sp drops whitespace only bold placeholder bullet.'''
    assert pptx2marp.handle_sp(parse(shape_xml(para(run(' ', bold=True)))), {}) is None


# --- pictures and media ----------------------------------------------------------------


def make_ctx(data: bytes, relationships: dict, slide_index: int = 1, **deck_overrides) -> pptx2marp.SlideContext:
    '''
    Build a SlideContext over in-memory deck bytes. `deck_overrides` may set any of
    DeckContext's own keyword fields (code_lang, slide_width_emu, slide_height_emu).
    '''
    archive, names = open_deck(data)
    deck = pptx2marp.DeckContext(archive=archive, names=names, registry=pptx2marp.MediaRegistry(),
                                 warnings=[], **deck_overrides)
    return deck.for_slide(relationships, slide_index)


def test_handle_pic_resolves_alt_and_media():
    '''Handle pic resolves alt and media.'''
    context = make_ctx(build_pptx({'ppt/media/a.png': PNG}), {'rId1': ('image', 'ppt/media/a.png')})
    assert pptx2marp_images.handle_pic(parse(pic(embed='rId1', descr='A [b] (c)')), context) == \
        ('A b c', 'ppt/media/a.png')
    assert pptx2marp_images.handle_pic(parse(pic(embed='rId1', name='')), context) == ('image', 'ppt/media/a.png')


def test_handle_pic_unresolved_linked_and_missing_blip():
    '''Handle pic unresolved linked and missing blip.'''
    context = make_ctx(build_pptx({}), {'rId2': ('image', 'https://x.test/a.png')})
    assert pptx2marp_images.handle_pic(parse(pic(embed='rId9')), context) is None
    assert pptx2marp_images.handle_pic(parse(pic(link='rId2')), context) is None
    assert pptx2marp_images.handle_pic(parse(pic(link='rId9')), context) is None
    assert pptx2marp_images.handle_pic(parse(pic()), context) is None
    assert pptx2marp_images.handle_pic(parse(pic_without_blip()), context) is None
    assert context.warnings == [
        'slide 1: image relationship rId9 could not be resolved',
        'slide 1: linked (non-embedded) image skipped: https://x.test/a.png',
        'slide 1: linked (non-embedded) image skipped: unknown',
    ]


def test_media_registry_dedups_and_disambiguates():
    '''Media registry dedups and disambiguates.'''
    archive, _ = open_deck(build_pptx({'ppt/media/a.png': PNG, 'ppt/other/a.png': b'2'}))
    registry = pptx2marp.MediaRegistry()
    warnings = []
    assert registry.register(archive, 'ppt/media/a.png', warnings, 1) == 'a.png'
    assert registry.register(archive, 'ppt/media/a.png', warnings, 2) == 'a.png'
    assert registry.register(archive, 'ppt/other/a.png', warnings, 3) == 'a-1.png'
    assert registry.register(archive, 'ppt/media/gone.png', warnings, 4) is None
    assert registry.bytes_by_asset == {'a.png': PNG, 'a-1.png': b'2'}
    assert warnings == ['slide 4: media part missing: ppt/media/gone.png']


def test_render_image_shape_flags_non_web_formats():
    '''Render image shape flags non web formats.'''
    data = build_pptx({'ppt/media/a.emf': b'emf', 'ppt/media/b.png': PNG})
    context = make_ctx(data, {'rId1': ('image', 'ppt/media/a.emf'), 'rId2': ('image', 'ppt/media/b.png'),
                              'rId3': ('image', 'ppt/media/missing.png')})
    emf = pptx2marp_images.render_image_shape(parse(pic(embed='rId1')), context)
    assert emf is not None
    assert emf.startswith('![Picture](assets/a.emf)\n<!-- pptx2marp: a.emf is a EMF file')
    assert pptx2marp_images.render_image_shape(parse(pic(embed='rId2')), context) == '![Picture](assets/b.png)'
    assert pptx2marp_images.render_image_shape(parse(pic(embed='rId3')), context) is None
    assert pptx2marp_images.render_image_shape(parse(pic()), context) is None
    assert 'slide 1: non-web image format kept as-is: a.emf' in context.warnings


# --- graphic frames and dispatch -------------------------------------------------------


def test_render_graphic_frame_variants():
    '''Render graphic frame variants.'''
    data = build_pptx({'ppt/diagrams/data1.xml': f'<dgm:dataModel {XMLNS}/>'})
    context = make_ctx(data, {'rId5': ('diagramData', 'ppt/diagrams/data1.xml')})
    assert pptx2marp.render_graphic_frame(parse(table([['a']])), context) == ['|a|\n|---|']
    assert not pptx2marp.render_graphic_frame(parse(table([])), context)
    assert not pptx2marp.render_graphic_frame(parse(diagram('rId5')), context)
    assert not pptx2marp.render_graphic_frame(parse('<p:graphicFrame/>'), context)
    assert pptx2marp.render_graphic_frame(parse(graphic_frame('ole')), context) == [
        '<!-- pptx2marp: unsupported embedded object on slide 1 (ole) -->',
    ]
    assert pptx2marp.render_graphic_frame(parse(graphic_frame('')), context)[0].endswith('(unknown) -->')
    assert context.warnings == [
        'slide 1: SmartArt diagram had no extractable text',
        'slide 1: unsupported graphic content (ole)',
        'slide 1: unsupported graphic content (unknown)',
    ]


def test_render_shape_dispatch():
    '''Render shape dispatch.'''
    context = make_ctx(build_pptx({'ppt/media/a.png': PNG}), {'rId1': ('image', 'ppt/media/a.png')})
    blocks = []
    assert pptx2marp.render_shape(parse(shape_xml(para(run('T')), ph_type='title')), context, blocks) == \
        ('title', 'T', 'title', 'T')
    assert pptx2marp.render_shape(parse(shape_xml(para(run('b')))), context, blocks) is None
    assert pptx2marp.render_shape(parse(shape_xml(ph_type='ftr')), context, blocks) is None
    assert pptx2marp.render_shape(parse(pic(embed='rId1')), context, blocks) is None
    assert pptx2marp.render_shape(parse(pic()), context, blocks) is None
    assert pptx2marp.render_shape(parse(table([['c']])), context, blocks) is None
    assert pptx2marp.render_shape(parse('<p:cxnSp/>'), context, blocks) is None
    assert blocks == ['- b', '![Picture](assets/a.png)', '|c|\n|---|']


def test_join_body_blocks_keeps_consecutive_list_lines_tight():
    '''Join body blocks keeps consecutive list lines tight.'''
    assert pptx2marp.join_body_blocks(['- a', '  - b', '- c']) == '- a\n  - b\n- c'


def test_join_body_blocks_separates_list_from_other_blocks():
    '''Join body blocks separates list from other blocks.'''
    assert pptx2marp.join_body_blocks(['- a', '![x](y)', '- b']) == '- a\n\n![x](y)\n\n- b'
    assert pptx2marp.join_body_blocks(['para one', 'para two']) == 'para one\n\npara two'
    assert pptx2marp.join_body_blocks(['solo']) == 'solo'
    assert not pptx2marp.join_body_blocks([])


def test_strip_trailing_whitespace_removes_trailing_spaces_and_tabs():
    '''Strip trailing whitespace removes trailing spaces and tabs.'''
    assert pptx2marp.strip_trailing_whitespace('a \nb\t\nc \xa0') == 'a\nb\nc'


def test_normalize_list_indentation_rebases_a_run_that_opens_at_a_nested_level():
    '''Normalize list indentation rebases a run that opens at a nested level.'''
    assert pptx2marp.normalize_list_indentation(['  - a', '  - b', '- c', '  - d']) == [
        '- a', '- b', '- c', '  - d',
    ]


def test_normalize_list_indentation_resets_at_non_list_blocks():
    '''Normalize list indentation resets at non list blocks.'''
    assert pptx2marp.normalize_list_indentation(['  - a', '![x](y)', '    - b']) == [
        '- a', '![x](y)', '- b',
    ]


def test_assemble_slide():
    '''Assemble slide.'''
    markdown, char_count, empty = pptx2marp.assemble_slide(1, ('Title', 'ctrTitle'), 'Sub', ['- a'], 'note')
    assert markdown == "<!-- _class: lead -->\n\n# Title\n\n## Sub\n\n- a\n\n<!-- note -->"
    assert char_count == (
        len('<!-- _class: lead -->') + len('# Title') + len('## Sub') + len('- a') + len('<!-- note -->')
    )
    assert not empty
    # Every slide title is an h1; only the deck's opening slide takes the lead class.
    markdown, _, empty = pptx2marp.assemble_slide(2, ('Title', 'title'), None, [], None)
    assert markdown == '# Title' and not empty
    markdown, _, _ = pptx2marp.assemble_slide(2, ('Title', 'ctrTitle'), None, [], None)
    assert markdown == '# Title'
    markdown, _, empty = pptx2marp.assemble_slide(3, (None, None), None, [], None)
    assert markdown == '<!-- pptx2marp: slide 3 has no extractable text or images -->'
    assert empty
    markdown, _, _ = pptx2marp.assemble_slide(
        4, (None, None), None, ['- a', '- b', '![x](y)'], None,
    )
    assert markdown == '- a\n- b\n\n![x](y)'


def test_front_matter():
    '''Front matter.'''
    assert pptx2marp.front_matter('A: b', 'gaia') == \
        '---\nmarp: true\ntheme: gaia\npaginate: true\ntitle: "A: b"\n---'


# --- notes -----------------------------------------------------------------------------


def notes_deck(notes: str | None, notes_rels: str | None = None, rels_target: str = 'notes1.xml') -> tuple:
    '''A one-slide deck with an optional notesSlide, returning (archive, names, slide_rels).'''
    parts = {}
    if notes is not None:
        parts['ppt/notesSlides/notes1.xml'] = notes
    if notes_rels is not None:
        parts['ppt/notesSlides/_rels/notes1.xml.rels'] = notes_rels
    archive, names = open_deck(build_pptx(parts))
    slide_rels = {'rId1': ('http://x/notesSlide', f'ppt/notesSlides/{rels_target}'),
                  'rId2': ('http://x/slideLayout', 'ppt/slideLayouts/l1.xml')}
    return archive, names, slide_rels


def test_get_notes_renders_body_text_with_links():
    '''Get notes renders body text with links.'''
    notes = notes_xml(para(run('see', link_rel_id='rId7')), para(run('a -- b')), para(run(' ')))
    notes_rels = rels_xml([('rId7', 'hyperlink', 'https://x.test/')], external={'rId7'})
    archive, names, slide_rels = notes_deck(notes, notes_rels)
    assert pptx2marp.get_notes(archive, slide_rels, names) == '[see](https://x.test/)\na - -  b'


@pytest.mark.parametrize('notes, target', [
    (None, 'notes1.xml'),
    ('<broken', 'notes1.xml'),
    (notes_xml(para(run('x')), body=False), 'notes1.xml'),
    (notes_xml(txbody=False), 'notes1.xml'),
    (notes_xml(para(run('  '))), 'notes1.xml'),
    (notes_xml(para(run('x'))), 'elsewhere.xml'),
])
def test_get_notes_returns_none_when_unusable(notes, target):
    '''Get notes returns none when unusable.'''
    archive, names, slide_rels = notes_deck(notes, rels_target=target)
    assert pptx2marp.get_notes(archive, slide_rels, names) is None


def test_get_notes_without_notes_relationship():
    '''Get notes without notes relationship.'''
    archive, names, _ = notes_deck(notes_xml(para(run('x'))))
    assert pptx2marp.get_notes(archive, {}, names) is None


# --- whole-deck conversion -------------------------------------------------------------


def test_convert_deck_end_to_end(tmp_path):
    '''Convert deck end to end.'''
    slides = [
        slide_xml(shape_xml(para(run('Deck: "Title"')), ph_type='ctrTitle'),
                  shape_xml(para(run('Author')), ph_type='subTitle')),
        slide_xml(shape_xml(para(run('Second')), ph_type='title'), shape_xml(para(run('point'))),
                  pic(embed='rId1'), pic(embed='rId1')),
    ]
    extra = {'ppt/media/img.png': PNG, 'ppt/notesSlides/notes2.xml': notes_xml(para(run('hint')))}
    slide_rels = {2: rels_xml([('rId1', 'image', '../media/img.png'),
                               ('rId2', 'notesSlide', '../notesSlides/notes2.xml')])}
    result = convert(tmp_path, simple_deck(slides, extra, slide_rels), theme='pach')

    assert result.ok and result.error == ''
    assert result.stats.slides == 2
    assert result.stats.images == 1
    assert result.media == {'img.png': PNG}
    assert not result.warnings
    assert result.stats.text_chars > 0
    assert result.markdown == (
        '---\nmarp: true\ntheme: pach\npaginate: true\ntitle: "Deck: \\"Title\\""\n---\n\n'
        '<!-- _class: lead -->\n\n# Deck: "Title"\n\n## Author\n\n---\n\n'
        '# Second\n\n- point\n\n![Picture](assets/img.png)\n\n'
        '<!-- hint -->\n'
    )


def test_convert_deck_title_falls_back_to_filename(tmp_path):
    '''Convert deck title falls back to filename.'''
    slides = [slide_xml(shape_xml(para(run('body only')))),
              slide_xml(shape_xml(para(run('Late')), ph_type='title'))]
    result = convert(tmp_path, simple_deck(slides), name='my_deck-01.pptx')
    assert 'title: "my deck 01"' in result.markdown
    assert '# Late' in result.markdown


def test_convert_deck_only_first_title_and_subtitle_per_slide(tmp_path):
    '''Convert deck only first title and subtitle per slide.'''
    slides = [slide_xml(
        shape_xml(para(run('First')), ph_type='title'), shape_xml(para(run('Second')), ph_type='title'),
        shape_xml(para(run('S1')), ph_type='subTitle'), shape_xml(para(run('S2')), ph_type='subTitle'),
    )]
    result = convert(tmp_path, simple_deck(slides))
    assert '# First' in result.markdown
    assert 'Second' not in result.markdown
    assert '## S1' in result.markdown and 'S2' not in result.markdown


def test_convert_deck_handles_broken_slides(tmp_path):
    '''Convert deck handles broken slides.'''
    parts = {
        'ppt/slides/slide1.xml': '<broken',
        'ppt/slides/slide2.xml': slide_xml(sptree=False),
        'ppt/slides/slide3.xml': slide_xml(),
    }
    result = convert(tmp_path, build_pptx(parts))
    assert result.ok and result.stats.slides == 3
    assert '<!-- pptx2marp: slide 1 could not be parsed -->' in result.markdown
    assert '<!-- pptx2marp: slide 2 has no content tree -->' in result.markdown
    assert '<!-- pptx2marp: slide 3 has no extractable text or images -->' in result.markdown
    assert result.warnings[0].startswith('slide 1 (ppt/slides/slide1.xml): failed to parse')
    assert 'slide 3: no extractable text or images' in result.warnings


def test_convert_deck_empty_archive(tmp_path):
    '''Convert deck empty archive.'''
    result = convert(tmp_path, build_pptx({'x.txt': 'nothing'}))
    assert result.ok and result.stats.slides == 0
    assert result.warnings == ['no slides found in this deck']
    assert result.markdown.endswith('---\n\n\n')


def test_convert_deck_not_a_zip(tmp_path):
    '''Convert deck not a zip.'''
    path = tmp_path / 'bad.pptx'
    path.write_bytes(b'not a zip')
    result = pptx2marp.convert_deck(path)
    assert not result.ok and result.error.startswith('could not open as a zip archive')
    result = pptx2marp.convert_deck(tmp_path / 'missing.pptx')
    assert not result.ok and 'could not open' in result.error


def test_convert_deck_unexpected_error(tmp_path, monkeypatch):
    '''Convert deck unexpected error.'''
    def boom(*_args, **_kwargs):
        raise RuntimeError('kaboom')
    monkeypatch.setattr(pptx2marp, 'get_slide_order', boom)
    result = convert(tmp_path, simple_deck([slide_xml()]))
    assert not result.ok and result.error == 'unexpected error: kaboom'


# --- filesystem and CLI ----------------------------------------------------------------


@pytest.fixture(name='keep_caplog')
def fixture_keep_caplog(monkeypatch):
    '''
    main() calls logging.basicConfig(force=True), which would evict caplog's handler
    from the root logger. Tests that inspect main()'s log output stub it out;
    configure_logging itself is tested directly.
    '''
    monkeypatch.setattr(pptx2marp, 'configure_logging', lambda *_: None)


def test_write_deck(tmp_path):
    '''Write deck.'''
    result = pptx2marp.DeckResult(markdown='# hi\n', media={'a.png': PNG})
    pptx2marp.write_deck(result, tmp_path / 'out')
    assert (tmp_path / 'out' / 'index.md').read_text() == '# hi\n'
    assert (tmp_path / 'out' / 'assets' / 'a.png').read_bytes() == PNG
    pptx2marp.write_deck(pptx2marp.DeckResult(markdown='x'), tmp_path / 'noassets')
    assert not (tmp_path / 'noassets' / 'assets').exists()


def test_discover_jobs(tmp_path):
    '''Discover jobs.'''
    src = tmp_path / 'src'
    for name in ('b/two.pptx', 'a/one.pptx', 'a/~$one.pptx', 'a/notes.txt'):
        write_pptx(src / name, b'')
    jobs = pptx2marp.discover_jobs(src, tmp_path / 'out')
    assert jobs == [
        (src / 'a/one.pptx', tmp_path / 'out/a/one'),
        (src / 'b/two.pptx', tmp_path / 'out/b/two'),
    ]
    assert pptx2marp.discover_jobs(src / 'a/one.pptx', tmp_path / 'out') == [
        (src / 'a/one.pptx', tmp_path / 'out')
    ]


def test_log_report_totals_and_levels(caplog):
    '''Log report totals and levels.'''
    ok = pptx2marp.DeckResult(stats=pptx2marp.DeckStats(slides=3, images=2, text_chars=10), warnings=['w1'])
    empty = pptx2marp.DeckResult()
    failed = pptx2marp.DeckResult(ok=False, error='bad')
    summary = [(Path('a.pptx'), Path('a'), ok), (Path('b.pptx'), Path('b'), empty),
               (Path('c.pptx'), Path('c'), failed)]
    with caplog.at_level(logging.INFO, logger='pptx2marp'):
        totals = pptx2marp.log_report(summary, dry_run=True)
    assert totals == {'decks': 3, 'failed': 1, 'suspicious': 1, 'slides': 3, 'images': 2}
    by_level = {(r.levelname, r.getMessage()) for r in caplog.records}
    assert ('INFO', '[OK] a.pptx -> a (3 slides, 2 images, would write)') in by_level
    assert ('INFO', '[OK] b.pptx -> b (0 slides, 0 images, would write)'
            '  <-- SUSPICIOUS (zero slides or no text)') in by_level
    assert ('WARNING', 'a.pptx: w1') in by_level
    assert ('ERROR', '[FAIL] c.pptx: bad') in by_level
    assert ('INFO', 'total failed: 1') in by_level


@pytest.mark.parametrize('verbose, quiet, level', [
    (False, False, logging.INFO), (True, False, logging.DEBUG), (False, True, logging.WARNING),
])
def test_configure_logging(verbose, quiet, level):
    '''Configure logging.'''
    pptx2marp.configure_logging(verbose, quiet)
    assert logging.getLogger().level == level


@pytest.mark.usefixtures('keep_caplog')
def test_main_writes_output_and_exits_zero(tmp_path, caplog):
    '''Main writes output and exits zero.'''
    src = write_pptx(tmp_path / 'in/deck.pptx',
                     simple_deck([slide_xml(shape_xml(para(run('T')), ph_type='ctrTitle'))]))
    out = tmp_path / 'out'
    with caplog.at_level(logging.DEBUG, logger='pptx2marp'):
        assert pptx2marp.main([str(src.parent), '--out', str(out), '--verbose']) == 0
    assert (out / 'deck' / 'index.md').read_text().startswith('---\nmarp: true')
    assert any(r.levelno == logging.DEBUG and 'converting' in r.getMessage() for r in caplog.records)


def test_main_dry_run_writes_nothing(tmp_path):
    '''Main dry run writes nothing.'''
    src = write_pptx(tmp_path / 'deck.pptx', simple_deck([slide_xml()]))
    out = tmp_path / 'out'
    assert pptx2marp.main([str(src), '--out', str(out), '--dry-run', '--quiet']) == 0
    assert not out.exists()


def test_main_returns_one_when_a_deck_fails(tmp_path):
    '''Main returns one when a deck fails.'''
    write_pptx(tmp_path / 'in/good.pptx', simple_deck([slide_xml()]))
    write_pptx(tmp_path / 'in/bad.pptx', b'garbage')
    assert pptx2marp.main([str(tmp_path / 'in'), '--out', str(tmp_path / 'out')]) == 1
    assert (tmp_path / 'out/good/index.md').exists()
    assert not (tmp_path / 'out/bad').exists()


@pytest.mark.usefixtures('keep_caplog')
def test_main_usage_errors(tmp_path, caplog):
    '''Main usage errors.'''
    with caplog.at_level(logging.ERROR, logger='pptx2marp'):
        assert pptx2marp.main([str(tmp_path / 'nope'), '--out', str(tmp_path / 'o')]) == 2
        assert pptx2marp.main([str(tmp_path), '--out', str(tmp_path / 'o')]) == 2
    messages = [r.getMessage() for r in caplog.records]
    assert messages[0].startswith('input path does not exist')
    assert messages[1].startswith('no .pptx files found under')
    with pytest.raises(SystemExit):
        pptx2marp.main([str(tmp_path), '--out', 'o', '--verbose', '--quiet'])


# --- edge cases found by the coverage report -------------------------------------------


def test_raw_paragraph_text_skips_empty_run():
    '''Raw paragraph text skips empty run.'''
    assert pptx2marp.raw_paragraph_text(parse(para('<a:r><a:t></a:t></a:r>', run('x')))) == 'x'


def test_handle_pic_without_cnvpr_uses_default_alt():
    '''Handle pic without cnvpr uses default alt.'''
    context = make_ctx(build_pptx({'ppt/media/a.png': PNG}), {'rId1': ('image', 'ppt/media/a.png')})
    shape = parse('<p:pic><p:blipFill><a:blip r:embed="rId1"/></p:blipFill></p:pic>')
    assert pptx2marp_images.handle_pic(shape, context) == ('image', 'ppt/media/a.png')


def test_render_image_shape_when_registry_cannot_read(monkeypatch):
    '''Render image shape when registry cannot read.'''
    context = make_ctx(build_pptx({'ppt/media/a.png': PNG}), {'rId1': ('image', 'ppt/media/a.png')})
    monkeypatch.setattr(context.registry, 'register', lambda *_: None)
    assert pptx2marp_images.render_image_shape(parse(pic(embed='rId1')), context) is None


def test_render_graphic_frame_diagram_with_text():
    '''Render graphic frame diagram with text.'''
    data = f'<dgm:dataModel {XMLNS}><dgm:t><a:t>Node</a:t></dgm:t></dgm:dataModel>'
    context = make_ctx(build_pptx({'ppt/diagrams/data1.xml': data}),
                       {'rId5': ('diagramData', 'ppt/diagrams/data1.xml')})
    assert pptx2marp.render_graphic_frame(parse(diagram('rId5')), context) == ['- Node']
    assert not context.warnings


def test_render_table_skips_blank_paragraphs():
    '''Render table skips blank paragraphs.'''
    table_el = parse(
        f'<a:tbl><a:tr><a:tc><a:txBody>{para(run(" "))}{para(run("v"))}</a:txBody></a:tc></a:tr></a:tbl>'
    )
    assert pptx2marp.render_table(table_el, {}) == '|v|\n|---|'


def test_get_slide_order_skips_unknown_rids():
    '''Get slide order skips unknown rids.'''
    parts = {
        'ppt/slides/slide1.xml': slide_xml(),
        'ppt/presentation.xml': presentation_xml(['rIdX', 'rId1']),
        'ppt/_rels/presentation.xml.rels': rels_xml([('rId1', 'slide', 'slides/slide1.xml')]),
    }
    archive, names = open_deck(build_pptx(parts))
    assert pptx2marp.get_slide_order(archive, names) == ['ppt/slides/slide1.xml']
