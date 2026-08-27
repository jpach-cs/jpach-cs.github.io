'''
Unit tests for the five OOXML->Marp fidelity defects fixed on top of tools/pptx2marp.py:
pasted code rendered as bullets, images at native pixel size, duplicate/cropped picture
references, dropped OLE object previews, and titles PowerPoint split across two
placeholders. Split out of test_pptx2marp.py to keep that module under its line cap - see
its module docstring.

Every deck used here is assembled in memory by pptx_builder from hand-written OOXML, so
each test states exactly which structure it is exercising. Nothing on disk, nothing
binary, no PowerPoint.
'''

from __future__ import annotations

import contextlib
import io
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

import pytest

import pptx2marp
import pptx2marp_images
import pptx2marp_text
from pptx_builder import (
    XMLNS,
    build_pptx,
    graphic_frame,
    ole_graphic_frame,
    para,
    pic,
    pic_without_blip,
    presentation_xml,
    rels_xml,
    run,
    shape_xml,
    simple_deck,
    slide_xml,
    write_pptx,
)

PNG = b'\x89PNG\r\n\x1a\n' + b'\x00' * 8

OPEN_ZIPS = contextlib.ExitStack()


@pytest.fixture(autouse=True, scope='module')
def close_open_zips():
    '''Close every archive opened through open_deck once the module is done.'''
    yield
    OPEN_ZIPS.close()


def parse(xml: str):
    '''Parse a fragment that uses the a:/p:/r: prefixes into an Element.'''
    return ET.fromstring(f'<root {XMLNS}>{xml}</root>')[0]


def open_deck(data: bytes):
    '''
    Open in-memory deck bytes as (ZipFile, names). The archive stays open for the
    life of the module so tests can hand it around freely.
    '''
    archive = OPEN_ZIPS.enter_context(zipfile.ZipFile(io.BytesIO(data)))
    return archive, set(archive.namelist())


def make_ctx(data: bytes, relationships: dict, slide_index: int = 1, **deck_overrides) -> pptx2marp.SlideContext:
    '''
    Build a SlideContext over in-memory deck bytes. `deck_overrides` may set any of
    DeckContext's own keyword fields (code_lang, slide_width_emu, slide_height_emu).
    '''
    archive, names = open_deck(data)
    deck = pptx2marp.DeckContext(archive=archive, names=names, registry=pptx2marp.MediaRegistry(),
                                 warnings=[], **deck_overrides)
    return deck.for_slide(relationships, slide_index)


def convert(tmp_path: Path, data: bytes, name: str = 'deck.pptx', **kwargs) -> pptx2marp.DeckResult:
    '''Write deck bytes to tmp_path and convert them.'''
    return pptx2marp.convert_deck(write_pptx(tmp_path / name, data), **kwargs)


@pytest.fixture(name='keep_caplog')
def fixture_keep_caplog(monkeypatch):
    '''
    main() calls logging.basicConfig(force=True), which would evict caplog's handler
    from the root logger. Tests that inspect main()'s log output stub it out;
    configure_logging itself is tested directly.
    '''
    monkeypatch.setattr(pptx2marp, 'configure_logging', lambda *_: None)


# --- defect 1: pasted-code detection and fencing (pptx2marp_text + handle_sp) -----------


@pytest.mark.parametrize('typeface, expected', [
    ('Consolas', True), ('CASCADIA MONO', True), ('Cascadia Code', True),
    ('Courier New', True), ('courier', True), ('Menlo', True), ('Monaco', True),
    ('Lucida Console', True), ('source code pro', True), ('  Consolas  ', True),
    ('Calibri', False), ('', False),
])
def test_is_monospace_typeface(typeface, expected):
    '''Is monospace typeface.'''
    assert pptx2marp_text.is_monospace_typeface(typeface) is expected


@pytest.mark.parametrize('run_texts, monospace_flags, paragraph_count, expected', [
    ([], [], 0, False),
    (['int x = 1;'], [True], 1, False),  # short, one paragraph: an annotation, not code
    (['for (int i = 0; i < 10; i++) {'], [True], 1, True),  # long enough on its own
    (['a', 'b'], [True, True], 2, True),  # short but multi-paragraph
    (['a', 'b'], [True, False], 2, False),  # only 50% monospace runs
    (['Hello world!'], [True], 1, False),  # the annotation callout from the task brief
])
def test_is_code_shape_thresholds(run_texts, monospace_flags, paragraph_count, expected):
    '''Is code shape thresholds.'''
    assert pptx2marp_text.is_code_shape(run_texts, monospace_flags, paragraph_count) is expected


def test_render_code_fence_joins_paragraphs_with_newlines_and_lang_hint():
    '''Render code fence joins paragraphs with newlines and lang hint.'''
    assert pptx2marp_text.render_code_fence(['def f():', '    return 1'], 'python') == \
        '```python\ndef f():\n    return 1\n```'
    assert pptx2marp_text.render_code_fence(['x'], '') == '```\nx\n```'


def test_render_code_fence_uses_four_backtick_fence_when_content_has_triple_backtick():
    '''Render code fence uses four backtick fence when content has triple backtick.'''
    fence = pptx2marp_text.render_code_fence(['```', 'code', '```'], '')
    assert fence == '````\n```\ncode\n```\n````'


def test_handle_sp_code_shape_renders_fenced_block_preserving_whitespace_and_breaks():
    '''Handle sp code shape renders fenced block preserving whitespace and breaks.'''
    shape = shape_xml(
        para(run('def f():', typeface='Consolas')),
        para(run('\treturn 1  ', typeface='Consolas'), '<a:br/>', run('# done', typeface='Consolas')),
        has_placeholder=False, tx_box=True,
    )
    assert pptx2marp.handle_sp(parse(shape), {}, code_lang='python') == (
        'body', ['```python\ndef f():\n\treturn 1  \n# done\n```'], None, None,
    )


def test_handle_sp_code_shape_no_lang_hint_and_no_escaping():
    '''Handle sp code shape no lang hint and no escaping.'''
    shape = shape_xml(
        para(run('vector<int> v = {1, 2};', typeface='Cascadia Code')),
        para(run('int* p = &v[0];', typeface='Cascadia Code')),
        has_placeholder=False, tx_box=True,
    )
    assert pptx2marp.handle_sp(parse(shape), {}) == (
        'body', ['```\nvector<int> v = {1, 2};\nint* p = &v[0];\n```'], None, None,
    )


def test_handle_sp_short_monospace_annotation_stays_plain_text():
    '''Handle sp short monospace annotation stays plain text.'''
    shape = shape_xml(para(run('Hello world!', typeface='Consolas')), has_placeholder=False, tx_box=True)
    assert pptx2marp.handle_sp(parse(shape), {}) == ('body', ['- Hello world!'], None, None)


def test_handle_sp_prose_about_pointers_is_not_mistaken_for_code():
    '''Handle sp prose about pointers is not mistaken for code.'''
    shape = shape_xml(
        para(run('A pointer int* p = &x; stores an address.')),
        para(run('Dereferencing *p reads the value at that address, in the C language.')),
    )
    assert pptx2marp.handle_sp(parse(shape), {}) == (
        'body',
        ['- A pointer int\\* p = &amp;x; stores an address.',
         '- Dereferencing \\*p reads the value at that address, in the C language.'],
        'body', None,
    )


def test_render_shape_threads_code_lang_from_context_to_handle_sp():
    '''Render shape threads code lang from context to handle sp.'''
    context = make_ctx(build_pptx({}), {}, code_lang='python')
    blocks = []
    shape = shape_xml(
        para(run('a = 1', typeface='Consolas')), para(run('b = 2', typeface='Consolas')),
        has_placeholder=False,
    )
    assert pptx2marp.render_shape(parse(shape), context, blocks) is None
    assert blocks == ['```python\na = 1\nb = 2\n```']


# --- defect 2: image sizing (pptx2marp_images + pptx2marp_text) ------------------------


def test_get_picture_extent_reads_xfrm_or_none():
    '''Get picture extent reads xfrm or none.'''
    assert pptx2marp_images.get_picture_extent(parse(pic(embed='rId1', ext=(2638874, 2969030)))) == \
        (2638874, 2969030)
    assert pptx2marp_images.get_picture_extent(parse(pic(embed='rId1'))) is None


def test_get_src_rect_reads_crop_or_none_when_absent_or_all_zero():
    '''Get src rect reads crop or none when absent or all zero.'''
    assert pptx2marp_images.get_src_rect(parse(pic(embed='rId1', src_rect=(10000, 0, 0, 0)))) == \
        (10000, 0, 0, 0)
    assert pptx2marp_images.get_src_rect(parse(pic(embed='rId1', src_rect=(0, 0, 0, 0)))) is None
    assert pptx2marp_images.get_src_rect(parse(pic(embed='rId1'))) is None


def test_get_picture_extent_and_get_src_rect_ignore_malformed_attributes():
    '''Get picture extent and get src rect ignore malformed attributes.'''
    xfrm = '<p:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="not-a-number" cy="1"/></a:xfrm></p:spPr>'
    shape = parse(f'<p:pic><p:blipFill><a:blip/></p:blipFill>{xfrm}</p:pic>')
    assert pptx2marp_images.get_picture_extent(shape) is None
    shape = parse('<p:pic><p:blipFill><a:blip/><a:srcRect l="not-a-number"/></p:blipFill></p:pic>')
    assert pptx2marp_images.get_src_rect(shape) is None


def test_get_slide_size_reads_sldsz_or_falls_back():
    '''Get slide size reads sldsz or falls back.'''
    archive, _ = open_deck(
        build_pptx({'ppt/presentation.xml': presentation_xml(['rId1'], sld_size=(9144000, 6858000))})
    )
    assert pptx2marp_images.get_slide_size(archive) == (9144000, 6858000)
    fallback = (pptx2marp_text.DEFAULT_SLIDE_WIDTH_EMU, pptx2marp_text.DEFAULT_SLIDE_HEIGHT_EMU)
    archive, _ = open_deck(build_pptx({'ppt/presentation.xml': presentation_xml(['rId1'])}))
    assert pptx2marp_images.get_slide_size(archive) == fallback
    archive, _ = open_deck(build_pptx({'ppt/presentation.xml': '<broken'}))
    assert pptx2marp_images.get_slide_size(archive) == fallback
    archive, _ = open_deck(build_pptx({}))
    assert pptx2marp_images.get_slide_size(archive) == fallback


@pytest.mark.parametrize('cx, cy, slide_w, slide_h, expected', [
    (2638874, 2969030, 12192000, 6858000, 'w:277px '),
    (12192000, 5829300, 12192000, 6858000, 'bg '),  # exactly the 85% boundary, inclusive
    (12192000, 5829299, 12192000, 6858000, 'w:1280px '),  # one EMU short of the boundary
    (100, 100, 0, 0, ''),  # degenerate slide size never divides by zero
])
def test_compute_image_size_prefix(cx, cy, slide_w, slide_h, expected):
    '''Compute image size prefix.'''
    assert pptx2marp_text.compute_image_size_prefix(cx, cy, slide_w, slide_h) == expected


def test_uncropped_extent_scales_back_out_cropped_edges():
    '''Uncropped extent scales back out cropped edges.'''
    assert pptx2marp_text.uncropped_extent(1000000, 1000000, (0, 0, 0, 66667)) == (1000000, 3000030)
    assert pptx2marp_text.uncropped_extent(1000000, 1000000, (0, 0, 0, 0)) == (1000000, 1000000)


def test_widest_extent_and_uncrop_pure_helpers():
    '''Widest extent and uncrop pure helpers.'''
    assert pptx2marp_images.widest_extent(None, (1, 2)) == (1, 2)
    assert pptx2marp_images.widest_extent((3, 1), None) == (3, 1)
    assert pptx2marp_images.widest_extent((3, 1), (1, 5)) == (3, 5)
    assert pptx2marp_images.uncrop(None, (0, 0, 0, 0)) is None
    assert pptx2marp_images.uncrop((10, 10), None) == (10, 10)
    assert pptx2marp_images.uncrop((10, 10), (0, 0, 0, 50000)) == (10, 20)


def test_render_image_shape_sizes_from_xfrm_scaled_to_marp_canvas():
    '''Render image shape sizes from xfrm scaled to marp canvas.'''
    data = build_pptx({'ppt/media/a.png': PNG})
    context = make_ctx(data, {'rId1': ('image', 'ppt/media/a.png')})
    shape = parse(pic(embed='rId1', ext=(2638874, 2969030)))
    assert pptx2marp_images.render_image_shape(shape, context) == '![w:277px Picture](assets/a.png)'


def test_render_image_shape_emits_bg_when_covering_85_percent_of_slide():
    '''Render image shape emits bg when covering 85 percent of slide.'''
    data = build_pptx({'ppt/media/a.png': PNG})
    context = make_ctx(data, {'rId1': ('image', 'ppt/media/a.png')})
    shape = parse(pic(embed='rId1', ext=(12192000, 5829300)))
    assert pptx2marp_images.render_image_shape(shape, context) == '![bg Picture](assets/a.png)'


def test_render_image_shape_no_size_when_nested_in_a_group_but_warns():
    '''Render image shape no size when nested in a group but warns.'''
    data = build_pptx({'ppt/media/a.png': PNG})
    context = make_ctx(data, {'rId1': ('image', 'ppt/media/a.png')})
    shape = parse(pic(embed='rId1', ext=(2638874, 2969030)))
    assert pptx2marp_images.render_image_shape(shape, context, in_group=True) == '![Picture](assets/a.png)'
    assert context.warnings == [
        'slide 1: image size ignored (nested inside a group; group transform not applied)'
    ]


def test_build_image_markdown_line_combines_size_prefix_and_format_warning():
    '''Build image markdown line combines size prefix and format warning.'''
    context = make_ctx(build_pptx({}), {})
    line = pptx2marp_images.build_image_markdown_line('Diagram', 'a.emf', 'w:100px ', context)
    assert line.startswith('![w:100px Diagram](assets/a.emf)\n<!-- pptx2marp: a.emf is a EMF')
    assert context.warnings == ['slide 1: non-web image format kept as-is: a.emf']


def test_iter_shapes_with_group_flag_marks_nested_shapes():
    '''Iter shapes with group flag marks nested shapes.'''
    xml = (
        f'<p:spTree {XMLNS}>'
        f'{shape_xml(ph_type="title")}'
        f'<p:grpSp>{pic(embed="rId1")}<p:grpSp>{pic(embed="rId2")}</p:grpSp></p:grpSp>'
        '</p:spTree>'
    )
    results = list(pptx2marp.iter_shapes_with_group_flag(ET.fromstring(xml)))
    assert [in_group for _, in_group in results] == [False, True, True]
    assert [shape.tag for shape, _ in results] == [pptx2marp.P_SP, pptx2marp.P_PIC, pptx2marp.P_PIC]


def test_render_shape_threads_in_group_to_render_picture():
    '''Render shape threads in group to render picture.'''
    data = build_pptx({'ppt/media/a.png': PNG})
    context = make_ctx(data, {'rId1': ('image', 'ppt/media/a.png')})
    blocks = []
    shape = parse(pic(embed='rId1', ext=(1000000, 1000000)))
    assert pptx2marp.render_shape(shape, context, blocks, in_group=True) is None
    assert blocks == ['![Picture](assets/a.png)']
    assert context.warnings == [
        'slide 1: image size ignored (nested inside a group; group transform not applied)'
    ]


def test_convert_deck_default_slide_size_scales_image(tmp_path):
    '''Convert deck default slide size scales image.'''
    slides = [slide_xml(pic(embed='rId1', ext=(6096000, 3429000)))]
    extra: dict[str, str | bytes] = {'ppt/media/img.png': PNG}
    slide_rels = {1: rels_xml([('rId1', 'image', '../media/img.png')])}
    result = convert(tmp_path, simple_deck(slides, extra, slide_rels))
    assert '![w:640px Picture](assets/img.png)' in result.markdown


# --- defect 3: duplicate/cropped picture references (render_picture) -------------------


def test_render_picture_dedupes_exact_repeat_with_no_crop():
    '''Render picture dedupes exact repeat with no crop.'''
    data = build_pptx({'ppt/media/a.png': PNG})
    context = make_ctx(data, {'rId1': ('image', 'ppt/media/a.png')})
    body_blocks = []
    pptx2marp_images.render_picture(parse(pic(embed='rId1')), context, False, body_blocks)
    pptx2marp_images.render_picture(parse(pic(embed='rId1')), context, False, body_blocks)
    assert body_blocks == ['![Picture](assets/a.png)']
    assert not context.warnings


def test_render_picture_dedupes_exact_repeat_with_same_crop():
    '''Render picture dedupes exact repeat with same crop.'''
    data = build_pptx({'ppt/media/a.png': PNG})
    context = make_ctx(data, {'rId1': ('image', 'ppt/media/a.png')})
    body_blocks = []
    shape = pic(embed='rId1', src_rect=(10000, 0, 0, 0))
    pptx2marp_images.render_picture(parse(shape), context, False, body_blocks)
    pptx2marp_images.render_picture(parse(shape), context, False, body_blocks)
    assert len(body_blocks) == 1
    assert not context.warnings


def test_render_picture_widens_extent_and_warns_once_on_differing_crop():
    '''Render picture widens extent and warns once on differing crop.'''
    data = build_pptx({'ppt/media/a.png': PNG})
    context = make_ctx(data, {'rId1': ('image', 'ppt/media/a.png')},
                       slide_width_emu=12192000, slide_height_emu=6858000)
    body_blocks = []
    # Three vertical thirds of one tall diagram, as in CSCI232Lecture13Fall25 slide 38.
    top = pic(embed='rId1', ext=(1000000, 1000000), src_rect=(0, 0, 0, 66667))
    middle = pic(embed='rId1', ext=(1000000, 1000000), src_rect=(0, 33333, 0, 33334))
    bottom = pic(embed='rId1', ext=(1000000, 1000000), src_rect=(0, 66667, 0, 0))
    pptx2marp_images.render_picture(parse(top), context, False, body_blocks)
    pptx2marp_images.render_picture(parse(middle), context, False, body_blocks)
    pptx2marp_images.render_picture(parse(bottom), context, False, body_blocks)
    assert len(body_blocks) == 1
    assert body_blocks[0].startswith('![w:')
    assert context.warnings == [
        'slide 1: image a.png is cropped in the source (srcRect); shown uncropped'
    ]


def test_render_picture_crop_duplicate_without_extent_keeps_no_size_but_still_warns():
    '''Render picture crop duplicate without extent keeps no size but still warns.'''
    data = build_pptx({'ppt/media/a.png': PNG})
    context = make_ctx(data, {'rId1': ('image', 'ppt/media/a.png')})
    body_blocks = []
    pptx2marp_images.render_picture(
        parse(pic(embed='rId1', src_rect=(10000, 0, 0, 0))), context, False, body_blocks
    )
    pptx2marp_images.render_picture(
        parse(pic(embed='rId1', src_rect=(20000, 0, 0, 0))), context, False, body_blocks
    )
    assert body_blocks == ['![Picture](assets/a.png)']
    assert context.warnings == [
        'slide 1: image a.png is cropped in the source (srcRect); shown uncropped'
    ]


def test_render_picture_first_occurrence_unresolvable_media_does_nothing(monkeypatch):
    '''Render picture first occurrence unresolvable media does nothing.'''
    context = make_ctx(build_pptx({'ppt/media/a.png': PNG}), {'rId1': ('image', 'ppt/media/a.png')})
    monkeypatch.setattr(context.registry, 'register', lambda *_: None)
    body_blocks = []
    pptx2marp_images.render_picture(parse(pic(embed='rId1')), context, False, body_blocks)
    assert not body_blocks
    assert not context.seen_pictures


def test_render_picture_unresolved_picture_does_nothing():
    '''Render picture unresolved picture does nothing.'''
    context = make_ctx(build_pptx({}), {})
    body_blocks = []
    pptx2marp_images.render_picture(parse(pic()), context, False, body_blocks)
    assert not body_blocks
    assert not context.seen_pictures


def test_convert_deck_dedupes_duplicate_image_with_no_crop(tmp_path):
    '''Convert deck dedupes duplicate image with no crop.'''
    # CSSI112lec_01 slide 24: the same image referenced twice with no crop.
    slides = [slide_xml(pic(embed='rId1'), pic(embed='rId1'))]
    extra: dict[str, str | bytes] = {'ppt/media/img.png': PNG}
    slide_rels = {1: rels_xml([('rId1', 'image', '../media/img.png')])}
    result = convert(tmp_path, simple_deck(slides, extra, slide_rels))
    assert result.markdown.count('assets/img.png') == 1


# --- defect 4: OLE object previews (render_graphic_frame) -------------------------------


def test_render_graphic_frame_ole_renders_preview_picture_sized_from_frame_xfrm():
    '''Render graphic frame ole renders preview picture sized from frame xfrm.'''
    data = build_pptx({'ppt/media/a.png': PNG})
    context = make_ctx(data, {'rId1': ('image', 'ppt/media/a.png')},
                       slide_width_emu=12192000, slide_height_emu=6858000)
    frame = ole_graphic_frame(pic(embed='rId1'), ext=(2638874, 2969030))
    assert pptx2marp.render_graphic_frame(parse(frame), context) == ['![w:277px Picture](assets/a.png)']


def test_render_graphic_frame_ole_ignores_preview_pics_own_xfrm():
    '''Render graphic frame ole ignores preview pics own xfrm.'''
    data = build_pptx({'ppt/media/a.png': PNG})
    context = make_ctx(data, {'rId1': ('image', 'ppt/media/a.png')},
                       slide_width_emu=12192000, slide_height_emu=6858000)
    preview = pic(embed='rId1', ext=(500000, 500000))  # irrelevant: the frame's own xfrm wins
    frame = ole_graphic_frame(preview, ext=(2638874, 2969030))
    assert pptx2marp.render_graphic_frame(parse(frame), context) == ['![w:277px Picture](assets/a.png)']


def test_render_graphic_frame_ole_without_frame_xfrm_gives_no_size():
    '''Render graphic frame ole without frame xfrm gives no size.'''
    data = build_pptx({'ppt/media/a.png': PNG})
    context = make_ctx(data, {'rId1': ('image', 'ppt/media/a.png')})
    frame = ole_graphic_frame(pic(embed='rId1'))
    assert pptx2marp.render_graphic_frame(parse(frame), context) == ['![Picture](assets/a.png)']


def test_render_ole_preview_returns_none_for_unresolvable_or_malformed_inputs():
    '''Render ole preview returns none for unresolvable or malformed inputs.'''
    data = build_pptx({'ppt/media/a.png': PNG})
    context = make_ctx(data, {'rId1': ('image', 'ppt/media/a.png')})
    graphic_data = parse(f'<a:graphicData uri="ole">{pic_without_blip()}</a:graphicData>')
    assert pptx2marp_images.render_ole_preview(graphic_data, None, context) is None

    context = make_ctx(build_pptx({}), {'rId1': ('image', 'ppt/media/missing.png')})
    graphic_data = parse(f'<a:graphicData uri="ole">{pic(embed="rId1")}</a:graphicData>')
    assert pptx2marp_images.render_ole_preview(graphic_data, None, context) is None

    context = make_ctx(data, {'rId1': ('image', 'ppt/media/a.png')})
    graphic_data = parse(f'<a:graphicData uri="ole">{pic(embed="rId1")}</a:graphicData>')
    bad_xfrm = parse('<p:xfrm><a:off x="0" y="0"/><a:ext cx="not-a-number" cy="1"/></p:xfrm>')
    assert pptx2marp_images.render_ole_preview(graphic_data, bad_xfrm, context) == \
        '![Picture](assets/a.png)'


def test_render_ole_preview_media_missing_from_archive_returns_none(monkeypatch):
    '''Render ole preview media missing from archive returns none.'''
    context = make_ctx(build_pptx({'ppt/media/a.png': PNG}), {'rId1': ('image', 'ppt/media/a.png')})
    monkeypatch.setattr(context.registry, 'register', lambda *_: None)
    graphic_data = parse(f'<a:graphicData uri="ole">{pic(embed="rId1")}</a:graphicData>')
    assert pptx2marp_images.render_ole_preview(graphic_data, None, context) is None


def test_render_ole_preview_frame_xfrm_without_ext_gives_no_size():
    '''Render ole preview frame xfrm without ext gives no size.'''
    data = build_pptx({'ppt/media/a.png': PNG})
    context = make_ctx(data, {'rId1': ('image', 'ppt/media/a.png')})
    graphic_data = parse(f'<a:graphicData uri="ole">{pic(embed="rId1")}</a:graphicData>')
    xfrm_without_ext = parse('<p:xfrm><a:off x="0" y="0"/></p:xfrm>')
    assert pptx2marp_images.render_ole_preview(graphic_data, xfrm_without_ext, context) == \
        '![Picture](assets/a.png)'


def test_render_graphic_frame_ole_without_preview_picture_falls_back_to_comment():
    '''Render graphic frame ole without preview picture falls back to comment.'''
    context = make_ctx(build_pptx({}), {})
    frame = graphic_frame(
        'http://schemas.openxmlformats.org/presentationml/2006/ole', '<mc:AlternateContent/>'
    )
    result = pptx2marp.render_graphic_frame(parse(frame), context)
    assert result[0].startswith('<!-- pptx2marp: unsupported embedded object')
    assert 'ole' in context.warnings[0]


# --- defect 5: split titles (try_merge_split_title / collect_slide_content) ------------


def test_try_merge_split_title_folds_lowercase_continuation():
    '''Try merge split title folds lowercase continuation.'''
    shape = parse(shape_xml(para(run('continues the sentence.'), bullet=False), ph_type='body'))
    assert pptx2marp.try_merge_split_title(shape, 'Introduction', {}) == \
        'Introduction continues the sentence.'


def test_try_merge_split_title_folds_when_title_lacks_terminal_punctuation():
    '''Try merge split title folds when title lacks terminal punctuation.'''
    shape = parse(shape_xml(para(run('Continued Title'), bullet=False), ph_type='body'))
    assert pptx2marp.try_merge_split_title(shape, 'Part One', {}) == 'Part One Continued Title'


def test_try_merge_split_title_returns_none_for_wrong_placeholder_or_no_title():
    '''Try merge split title returns none for wrong placeholder or no title.'''
    wrong_type = parse(shape_xml(para(run('text'), bullet=False), ph_type='title'))
    assert pptx2marp.try_merge_split_title(wrong_type, 'Intro', {}) is None
    body = parse(shape_xml(para(run('text'), bullet=False), ph_type='body'))
    assert pptx2marp.try_merge_split_title(body, None, {}) is None


def test_try_merge_split_title_returns_none_for_bulleted_or_multi_paragraph_body():
    '''Try merge split title returns none for bulleted or multi paragraph body.'''
    bulleted = parse(shape_xml(para(run('word')), ph_type='body'))
    assert pptx2marp.try_merge_split_title(bulleted, 'Title:', {}) is None
    multi = parse(shape_xml(para(run('a'), bullet=False), para(run('b'), bullet=False), ph_type='body'))
    assert pptx2marp.try_merge_split_title(multi, 'Title', {}) is None
    no_txbody = parse(shape_xml(ph_type='body', txbody=False))
    assert pptx2marp.try_merge_split_title(no_txbody, 'Title', {}) is None
    empty_body = parse(shape_xml(para(run(' '), bullet=False), ph_type='body'))
    assert pptx2marp.try_merge_split_title(empty_body, 'Title', {}) is None


def test_try_merge_split_title_returns_none_when_uppercase_continuation_meets_punctuated_title():
    '''Try merge split title returns none when uppercase continuation meets punctuated title.'''
    shape = parse(shape_xml(para(run('Uppercase Continuation'), bullet=False), ph_type='body'))
    assert pptx2marp.try_merge_split_title(shape, 'Title:', {}) is None


def test_collect_slide_content_merges_split_title_into_preceding_title():
    '''Collect slide content merges split title into preceding title.'''
    shape_tree = ET.fromstring(
        f'<p:spTree {XMLNS}>'
        f'{shape_xml(para(run("Part One")), ph_type="title")}'
        f'{shape_xml(para(run("continues the sentence."), bullet=False), ph_type="body")}'
        '</p:spTree>'
    )
    context = make_ctx(build_pptx({}), {})
    title, subtitle, body_blocks = pptx2marp.collect_slide_content(shape_tree, context)
    assert title[0] == 'Part One continues the sentence.'
    assert subtitle is None
    assert not body_blocks


def test_collect_slide_content_does_not_merge_a_bulleted_body():
    '''Collect slide content does not merge a bulleted body.'''
    shape_tree = ET.fromstring(
        f'<p:spTree {XMLNS}>'
        f'{shape_xml(para(run("Overview")), ph_type="title")}'
        f'{shape_xml(para(run("point one")), ph_type="body")}'
        '</p:spTree>'
    )
    context = make_ctx(build_pptx({}), {})
    title, _, body_blocks = pptx2marp.collect_slide_content(shape_tree, context)
    assert title[0] == 'Overview'
    assert body_blocks == ['- point one']


def test_collect_slide_content_does_not_merge_a_non_adjacent_body():
    '''Collect slide content does not merge a non adjacent body.'''
    data = build_pptx({'ppt/media/a.png': PNG})
    shape_tree = ET.fromstring(
        f'<p:spTree {XMLNS}>'
        f'{shape_xml(para(run("Overview")), ph_type="title")}'
        f'{pic(embed="rId1")}'
        f'{shape_xml(para(run("not a title continuation"), bullet=False), ph_type="body")}'
        '</p:spTree>'
    )
    context = make_ctx(data, {'rId1': ('image', 'ppt/media/a.png')})
    title, _, body_blocks = pptx2marp.collect_slide_content(shape_tree, context)
    assert title[0] == 'Overview'
    assert 'not a title continuation' in body_blocks[-1]


# --- end-to-end: --code-lang CLI option --------------------------------------------------


@pytest.mark.usefixtures('keep_caplog')
def test_main_code_lang_option_threads_to_convert_deck(tmp_path):
    '''Main code lang option threads to convert deck.'''
    slides = [slide_xml(shape_xml(
        para(run('x = 1', typeface='Consolas')), para(run('y = 2', typeface='Consolas')),
        has_placeholder=False,
    ))]
    src = write_pptx(tmp_path / 'in/deck.pptx', simple_deck(slides))
    out = tmp_path / 'out'
    assert pptx2marp.main([str(src), '--out', str(out), '--code-lang', 'python']) == 0
    assert '```python\nx = 1\ny = 2\n```' in (out / 'index.md').read_text()
