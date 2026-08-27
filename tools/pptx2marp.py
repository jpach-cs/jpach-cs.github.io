#!/usr/bin/env python3
'''
Convert PowerPoint (.pptx) decks into Marp-flavored Markdown, using only the Python
standard library - a .pptx is a zip of OOXML parts, read here with `zipfile` and
`xml.etree.ElementTree` (no pip installs, no LibreOffice, no pandoc).

Usage:
    python3 tools/pptx2marp.py path/to/deck.pptx --out out/deck
    python3 tools/pptx2marp.py path/to/decks/ --out out/decks [--dry-run] [--theme gaia]

For a single file, the output directory holds `index.md` and an `assets/` folder. For a
directory, every `.pptx` found recursively converts into its own subdirectory under
--out, mirroring the input tree (extension stripped).
'''

from __future__ import annotations

import argparse
import logging
import posixpath
import re
import sys
import zipfile
from dataclasses import dataclass, field
from pathlib import Path
from xml.etree import ElementTree as ET

import pptx2marp_images
from pptx2marp_text import (
    DEFAULT_SLIDE_HEIGHT_EMU,
    DEFAULT_SLIDE_WIDTH_EMU,
    escape_and_wrap_urls,
    escape_text,
    is_code_shape,
    is_monospace_typeface,
    join_body_blocks,
    normalize_list_indentation,
    protect_leading_marker,
    render_code_fence,
    safe_comment_text,
    strip_title_punctuation,
    strip_trailing_whitespace,
    wrap_emphasis,
    yaml_scalar,
)

LOG = logging.getLogger('pptx2marp')

NS = {
    'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
    'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
    'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
    'mc': 'http://schemas.openxmlformats.org/markup-compatibility/2006',
    'dgm': 'http://schemas.openxmlformats.org/drawingml/2006/diagram',
}


def qn(prefix: str, tag: str) -> str:
    '''
    Build a Clark-notation qualified tag name, e.g. qn('a', 't') -> '{drawingml-ns}t'.
    '''
    return '{%s}%s' % (NS[prefix], tag)


def _qns(prefix: str, tags: str) -> list:
    '''Build several Clark-notation names at once from a whitespace-separated tag list.'''
    return [qn(prefix, tag) for tag in tags.split()]


# Frequently used qualified names.
(P_SP, P_PIC, P_GRAPHICFRAME, P_CXNSP, P_GRPSP, P_NVSPPR, P_NVPR, P_PH, P_TXBODY,
 P_CSLD, P_SPTREE, P_SLDIDLST, P_XFRM) = _qns(
    'p', 'sp pic graphicFrame cxnSp grpSp nvSpPr nvPr ph txBody cSld spTree sldIdLst xfrm')

MC_ALTERNATECONTENT, MC_FALLBACK, MC_CHOICE = _qns('mc', 'AlternateContent Fallback Choice')

(A_P, A_R, A_T, A_BR, A_FLD, A_RPR, A_PPR, A_BUNONE, A_HLINKCLICK, A_TBL, A_TR, A_TC, A_TXBODY,
 A_GRAPHIC, A_GRAPHICDATA, A_LATIN) = _qns(
    'a', 'p r t br fld rPr pPr buNone hlinkClick tbl tr tc txBody graphic graphicData latin')

(DGM_RELIDS,) = _qns('dgm', 'relIds')
R_ID, R_DM = _qns('r', 'id dm')

# Placeholder types that carry metadata (page number, footer, date, the thumbnail
# preview shown on the notes page) rather than slide content. These are always
# auto-generated fields, so skipping them never drops author-written content.
SKIP_PLACEHOLDER_TYPES = {'sldNum', 'ftr', 'dt', 'sldImg'}

IMAGE_EXTS = {'.png', '.gif', '.svg', '.jpg', '.jpeg'}

SLIDE_NUM_RE = re.compile(r'(\d+)')


def raw_paragraph_text(paragraph) -> str:
    '''Extract a paragraph's plain text with no escaping, for use outside the Markdown body.'''
    parts = []
    for child in paragraph:
        if child.tag in (A_R, A_FLD):
            text_el = child.find(A_T)
            if text_el is not None and text_el.text:
                parts.append(text_el.text)
        elif child.tag == A_BR:
            parts.append(' ')
    return ''.join(parts)


def slide_number(name: str) -> int:
    '''Extract the numeric part of a slide part name, for numeric (not lexicographic) sort.'''
    match = SLIDE_NUM_RE.search(posixpath.basename(name))
    return int(match.group(1)) if match else -1


def parse_rels(archive: zipfile.ZipFile, part_name: str, names: set) -> dict:
    '''
    Parse the .rels part for `part_name` into {rId: (type, target)}; external targets
    (hyperlinks) are verbatim, internal ones resolved to a package-root-relative path.
    '''
    rels_path = posixpath.join(
        posixpath.dirname(part_name), '_rels', posixpath.basename(part_name) + '.rels'
    )
    if rels_path not in names:
        return {}
    try:
        root = ET.fromstring(archive.read(rels_path))
    except ET.ParseError:
        return {}
    base_dir = posixpath.dirname(part_name)
    relationships = {}
    for rel in root:
        rel_id = rel.get('Id')
        rtype = rel.get('Type', '')
        target = rel.get('Target', '')
        mode = rel.get('TargetMode', 'Internal')
        if mode == 'External':
            resolved = target
        else:
            resolved = posixpath.normpath(posixpath.join(base_dir, target))
        relationships[rel_id] = (rtype, resolved)
    return relationships


def get_slide_order(archive: zipfile.ZipFile, names: set) -> list:
    '''
    Determine the true, visual slide order from ppt/presentation.xml's <p:sldIdLst>
    (resolved through ppt/_rels/presentation.xml.rels), which is correct even when slide
    part filenames do not match display order. Falling back, on any failure, to a
    NUMERIC sort of the slideN.xml parts present - never lexicographic, which would put
    slide10.xml before slide2.xml and silently scramble the deck.
    '''
    try:
        pres = ET.fromstring(archive.read('ppt/presentation.xml'))
        presentation_rels = parse_rels(archive, 'ppt/presentation.xml', names)
        sld_id_lst = pres.find(P_SLDIDLST)
        order = []
        if sld_id_lst is not None:
            for sld_id in sld_id_lst:
                rel_id = sld_id.get(R_ID)
                entry = presentation_rels.get(rel_id)
                if entry and entry[1] in names:
                    order.append(entry[1])
        if order:
            return order
    except (ET.ParseError, KeyError):
        pass

    fallback = [name for name in names if re.match(r'ppt/slides/slide\d+\.xml$', name)]
    return sorted(fallback, key=slide_number)


def _extract_run_content(run_el, relationships: dict):
    '''
    Return (escaped_text, bold, italic, link_url) for one <a:r>/<a:fld>, or None if it
    has no text. A hyperlink run's visible text stays plain escaped text (it becomes a
    link's label); a non-hyperlink run also gets its bare URLs/e-mails autolinked.
    '''
    text_el = run_el.find(A_T)
    text = text_el.text if text_el is not None and text_el.text else ''
    if not text:
        return None
    run_props = run_el.find(A_RPR)
    bold = italic = False
    link = None
    if run_props is not None:
        bold = run_props.get('b') == '1'
        italic = run_props.get('i') == '1'
        hyperlink = run_props.find(A_HLINKCLICK)
        if hyperlink is not None:
            rel_id = hyperlink.get(R_ID)
            entry = relationships.get(rel_id) if rel_id else None
            if entry and entry[1]:
                link = entry[1]
    content = escape_text(text) if link else escape_and_wrap_urls(text)
    return content, bold, italic, link


def render_formatted_text(content: str, bold: bool, italic: bool, link: str | None) -> str:
    '''
    Apply bold/italic and hyperlink markup around already-escaped run content.
    '''
    if bold or italic:
        content = wrap_emphasis(content, bold, italic)
    if link:
        content = f'[{content}]({link})'
    return content


def render_run_text(run_el, relationships: dict) -> str:
    '''
    Render the <a:t> text of a single <a:r> or <a:fld> element, applying bold/italic
    and hyperlink markup carried on its <a:rPr>.
    '''
    parsed = _extract_run_content(run_el, relationships)
    if parsed is None:
        return ''
    content, bold, italic, link = parsed
    return render_formatted_text(content, bold, italic, link)


def render_paragraph(paragraph, relationships: dict) -> str:
    '''
    Render one <a:p> paragraph's runs, breaks, and fields into a Markdown text fragment
    (no leading bullet marker - the caller adds that). Adjacent runs/fields sharing the
    same bold/italic/hyperlink formatting are merged first, so `**a****b**` becomes
    `**ab**` instead of two back-to-back emphasis spans.
    '''
    groups: list = []  # (bold, italic, link) -> merged text, or (None, None) for <br>
    for child in paragraph:
        if child.tag in (A_R, A_FLD):
            parsed = _extract_run_content(child, relationships)
            if parsed is None:
                continue
            content, bold, italic, link = parsed
            key = (bold, italic, link)
            if groups and groups[-1][0] == key:
                groups[-1] = (key, groups[-1][1] + content)
            else:
                groups.append((key, content))
        elif child.tag == A_BR:
            groups.append((None, None))
    parts = []
    for key, content in groups:
        if key is None:
            parts.append('<br>')
        else:
            bold, italic, link = key
            parts.append(render_formatted_text(content, bold, italic, link))
    return ''.join(parts)


def get_placeholder_type(shape):
    '''Return a <p:sp>'s placeholder `type` ('body' if untyped), or None if freeform.'''
    placeholder = shape.find(f'{P_NVSPPR}/{P_NVPR}/{P_PH}')
    if placeholder is None:
        return None
    return placeholder.get('type', 'body')


def iter_shapes_with_group_flag(container, in_group: bool = False):
    '''
    Like `iter_shapes`, but also yields whether each shape is nested inside a <p:grpSp>
    group: a group has its own <a:xfrm> with a chOff/chExt child coordinate space, so a
    picture's own <a:xfrm> inside one is not directly in slide coordinates. Composing the
    group's transform chain (recursively, for nested groups, with rotation) is more than
    this converter attempts - callers instead use this flag to skip that picture's size
    and warn instead of emitting a wrong one.
    '''
    for child in container:
        tag = child.tag
        if tag == MC_ALTERNATECONTENT:
            branch = child.find(MC_FALLBACK)
            if branch is None:
                branch = child.find(MC_CHOICE)
            if branch is not None:
                yield from iter_shapes_with_group_flag(branch, in_group)
        elif tag == P_GRPSP:
            yield from iter_shapes_with_group_flag(child, True)
        elif tag in (P_SP, P_PIC, P_GRAPHICFRAME, P_CXNSP):
            yield child, in_group


def iter_shapes(container):
    '''
    Yield the content-bearing shapes (<p:sp>, <p:pic>, <p:graphicFrame>, <p:cxnSp>)
    inside `container` in document order, flattening <p:grpSp> groups and
    <mc:AlternateContent> (preferring Fallback, guaranteed schema-plain OOXML).
    '''
    for shape, _in_group in iter_shapes_with_group_flag(container):
        yield shape


def render_table(table_el, relationships: dict) -> str:
    '''
    Render an <a:tbl> as a GitHub-flavored Markdown pipe table, in the MD060 "tight"
    pipe style (no padding). A blank cell is just two adjacent pipes: neither "aligned"
    nor "compact" style can stay consistent once some cells are empty and others are
    not, since both require the same single space around content that isn't there.
    '''
    rows = []
    for row_el in table_el.findall(A_TR):
        cells = []
        for cell_el in row_el.findall(A_TC):
            texts = []
            txbody = cell_el.find(A_TXBODY)
            if txbody is not None:
                for paragraph_el in txbody.findall(A_P):
                    text = render_paragraph(paragraph_el, relationships)
                    if text.strip():
                        texts.append(text)
            cell = '<br>'.join(texts).replace('|', '\\|').strip()
            cells.append(cell)
        rows.append(cells)
    if not rows:
        return ''
    ncols = max(len(row) for row in rows)
    for row in rows:
        row.extend([''] * (ncols - len(row)))
    lines = ['|' + '|'.join(rows[0]) + '|', '|' + '|'.join(['---'] * ncols) + '|']
    for row in rows[1:]:
        lines.append('|' + '|'.join(row) + '|')
    return '\n'.join(lines)


def render_diagram(graphic_data, slide_rels: dict, archive: zipfile.ZipFile, names: set) -> list:
    '''
    SmartArt text lives in a separate ppt/diagrams/dataN.xml part (via <dgm:relIds>), not
    inline in the slide; pull it out so a SmartArt-only slide isn't rendered empty.
    '''
    rel_ids = graphic_data.find(DGM_RELIDS)
    if rel_ids is None:
        return []
    dm_rel_id = rel_ids.get(R_DM)
    entry = slide_rels.get(dm_rel_id) if dm_rel_id else None
    if not entry or entry[1] not in names:
        return []
    try:
        data_root = ET.fromstring(archive.read(entry[1]))
    except ET.ParseError:
        return []
    lines = []
    for text_el in data_root.iter(A_T):
        if text_el.text and text_el.text.strip():
            lines.append('- ' + protect_leading_marker(escape_text(text_el.text.strip())))
    return lines


def raw_code_paragraph_text(paragraph) -> str:
    '''
    Extract one code-shape paragraph's text verbatim (no escaping, tabs and leading
    whitespace preserved), with <a:br/> becoming a real newline within the paragraph -
    the caller joins paragraphs themselves with another newline.
    '''
    parts = []
    for child in paragraph:
        if child.tag in (A_R, A_FLD):
            text_el = child.find(A_T)
            if text_el is not None and text_el.text:
                parts.append(text_el.text)
        elif child.tag == A_BR:
            parts.append('\n')
    return ''.join(parts)


def _code_shape_run_stats(paragraphs: list) -> tuple:
    '''Collect (run_texts, monospace_flags) across every <a:r> in `paragraphs`.'''
    run_texts = []
    monospace_flags = []
    for paragraph_el in paragraphs:
        for run_el in paragraph_el.findall(A_R):
            text_el = run_el.find(A_T)
            text = text_el.text if text_el is not None and text_el.text else ''
            if not text:
                continue
            run_texts.append(text)
            run_props = run_el.find(A_RPR)
            latin = run_props.find(A_LATIN) if run_props is not None else None
            typeface = latin.get('typeface', '') if latin is not None else ''
            monospace_flags.append(is_monospace_typeface(typeface))
    return run_texts, monospace_flags


def _render_body_paragraph_lines(paragraphs: list, slide_rels: dict) -> list:
    '''
    Render each body paragraph into its Markdown line: a bulleted list item at its nesting
    level, or a plain paragraph when <a:buNone/> is set. Blank paragraphs are dropped, and
    a leading tab/space is stripped from each (MD030/MD046).
    '''
    lines = []
    for paragraph_el in paragraphs:
        text = render_paragraph(paragraph_el, slide_rels).lstrip(' \t')
        if not text.strip():
            continue
        para_props = paragraph_el.find(A_PPR)
        level = 0
        bullet = True
        if para_props is not None:
            try:
                level = int(para_props.get('lvl', '0'))
            except ValueError:
                level = 0
            if para_props.find(A_BUNONE) is not None:
                bullet = False
        text = protect_leading_marker(text)
        lines.append(('  ' * level) + '- ' + text if bullet else text)
    return lines


def handle_sp(shape, slide_rels: dict, code_lang: str = ''):
    '''
    Render one <p:sp> into (kind, payload, ph_type, raw_title_or_none) - kind is 'title',
    'subtitle', or 'body' - or None if the shape is metadata-only or carries no text.
    A freeform or `body`-placeholder shape whose runs are mostly set in a code-editor
    monospace font (Consolas, Cascadia Mono/Code, Courier (New), Menlo, Monaco, Lucida
    Console, Source Code Pro) is rendered as a single fenced code block instead of bullets
    - see `pptx2marp_text.is_code_shape` for the exact threshold.
    '''
    ph_type = get_placeholder_type(shape)
    if ph_type in SKIP_PLACEHOLDER_TYPES:
        return None
    txbody = shape.find(P_TXBODY)
    if txbody is None:
        return None
    paragraphs = txbody.findall(A_P)

    if ph_type in ('title', 'ctrTitle'):
        text = ' '.join(render_paragraph(paragraph, slide_rels) for paragraph in paragraphs).strip()
        text = strip_title_punctuation(text)
        raw = ' '.join(raw_paragraph_text(paragraph) for paragraph in paragraphs).strip()
        return ('title', text, ph_type, raw) if text else None

    if ph_type == 'subTitle':
        text = ' '.join(render_paragraph(paragraph, slide_rels) for paragraph in paragraphs).strip()
        return ('subtitle', text, ph_type, None) if text else None

    run_texts, monospace_flags = _code_shape_run_stats(paragraphs)
    if is_code_shape(run_texts, monospace_flags, len(paragraphs)):
        code_lines = [raw_code_paragraph_text(paragraph) for paragraph in paragraphs]
        fence = render_code_fence(code_lines, code_lang)
        return ('body', [fence], ph_type, None) if fence.strip() else None

    lines = _render_body_paragraph_lines(paragraphs, slide_rels)
    return ('body', lines, ph_type, None) if lines else None


@dataclass
class DeckStats:
    '''
    Counters for one converted deck. text_chars is the length of all extracted slide
    text, used to flag decks that "converted" without producing any content.
    '''
    slides: int = 0
    images: int = 0
    text_chars: int = 0

    @property
    def suspicious(self) -> bool:
        '''True when the deck produced zero slides or zero text - probably a bad convert.'''
        return self.slides == 0 or self.text_chars == 0


@dataclass
class DeckResult:
    '''The outcome of converting one .pptx: an error (ok=False), or Markdown plus media.'''
    ok: bool = True
    error: str = ''
    source: Path | None = None
    stats: DeckStats = field(default_factory=DeckStats)
    warnings: list = field(default_factory=list)
    markdown: str = ''
    media: dict = field(default_factory=dict)  # assets-relative name -> bytes


@dataclass
class MediaRegistry:
    '''Tracks media already extracted from a deck's zip, so a shared picture is copied once.'''
    path_to_asset: dict = field(default_factory=dict)   # package media path -> assets/ basename
    bytes_by_asset: dict = field(default_factory=dict)  # assets/ basename -> file bytes

    def register(self, archive: zipfile.ZipFile, media_path: str, warnings: list, slide_index: int):
        '''
        Ensure `media_path` has been extracted, returning its assets/ basename, or None
        if the referenced media part does not actually exist in the archive.
        '''
        if media_path in self.path_to_asset:
            return self.path_to_asset[media_path]
        basename = posixpath.basename(media_path)
        if basename in self.bytes_by_asset:
            stem, ext = posixpath.splitext(basename)
            basename = f'{stem}-{len(self.bytes_by_asset)}{ext}'
        try:
            data = archive.read(media_path)
        except KeyError:
            warnings.append(f'slide {slide_index}: media part missing: {media_path}')
            return None
        self.path_to_asset[media_path] = basename
        self.bytes_by_asset[basename] = data
        return basename


@dataclass
class SlideContext:
    '''
    The values every shape/picture/table renderer for one slide needs. Deck-wide values
    (the open archive, its part names, the media registry and warning log, the code-lang
    hint, the slide size) live on `deck` and are exposed here as read-through properties,
    so this class's own per-slide state stays small: which slide, its relationships, and
    which pictures have already been rendered on it (for dedup, see render_picture).
    '''
    deck: 'DeckContext'
    relationships: dict
    slide_index: int
    seen_pictures: dict = field(default_factory=dict)  # media path -> dedup state, see render_picture

    @property
    def archive(self) -> zipfile.ZipFile:
        '''The deck's open .pptx archive.'''
        return self.deck.archive

    @property
    def names(self) -> set:
        '''The deck's package part names.'''
        return self.deck.names

    @property
    def registry(self) -> MediaRegistry:
        '''The deck-wide media registry, shared so a picture reused across slides is copied once.'''
        return self.deck.registry

    @property
    def warnings(self) -> list:
        '''The deck-wide warning log every slide appends onto.'''
        return self.deck.warnings

    @property
    def code_lang(self) -> str:
        '''The --code-lang hint written after a detected code block's opening fence.'''
        return self.deck.code_lang

    @property
    def slide_width_emu(self) -> int:
        '''The deck's real slide width in EMU, for scaling a picture onto the Marp canvas.'''
        return self.deck.slide_width_emu

    @property
    def slide_height_emu(self) -> int:
        '''The deck's real slide height in EMU, for scaling a picture onto the Marp canvas.'''
        return self.deck.slide_height_emu


def render_graphic_frame(shape, context: SlideContext):
    '''
    Render a <p:graphicFrame> shape (table, SmartArt diagram, OLE object preview, or
    something else OOXML can embed there) into a list of Markdown blocks to append to the
    slide body.
    '''
    graphic_data = shape.find(f'{A_GRAPHIC}/{A_GRAPHICDATA}')
    if graphic_data is None:
        return []
    uri = graphic_data.get('uri', '')
    table_el = graphic_data.find(A_TBL)
    if table_el is not None:
        table_md = render_table(table_el, context.relationships)
        return [table_md] if table_md else []
    if 'diagram' in uri:
        diagram_lines = render_diagram(graphic_data, context.relationships, context.archive, context.names)
        if not diagram_lines:
            context.warnings.append(f'slide {context.slide_index}: SmartArt diagram had no extractable text')
        return diagram_lines
    if 'ole' in uri:
        ole_line = pptx2marp_images.render_ole_preview(graphic_data, shape.find(P_XFRM), context)
        if ole_line is not None:
            return [ole_line]
    context.warnings.append(f'slide {context.slide_index}: unsupported graphic content ({uri or "unknown"})')
    return [
        f'<!-- pptx2marp: unsupported embedded object on slide {context.slide_index} ({uri or "unknown"}) -->'
    ]


def render_shape(shape, context: SlideContext, body_blocks: list, in_group: bool = False):
    '''
    Dispatch one flattened shape (see iter_shapes_with_group_flag) to its renderer. Body
    content (images, tables, diagrams, bullet/paragraph text) is appended directly to
    `body_blocks`; a title or subtitle shape is instead returned to the caller, which
    keeps only the first of each per slide.
    '''
    tag = shape.tag
    if tag == P_SP:
        handled = handle_sp(shape, context.relationships, context.code_lang)
        if handled is None:
            return None
        kind, payload, ph_kind, raw = handled
        if kind == 'body':
            body_blocks.extend(payload)
            return None
        return (kind, payload, ph_kind, raw)
    if tag == P_PIC:
        pptx2marp_images.render_picture(shape, context, in_group, body_blocks)
    elif tag == P_GRAPHICFRAME:
        body_blocks.extend(render_graphic_frame(shape, context))
    # p:cxnSp (connectors) cannot carry text per the OOXML schema - decorative, skip.
    return None


def assemble_slide(slide_index, title, subtitle, body_blocks, notes_text):
    '''
    Join one slide's title, subtitle, body blocks, and speaker notes into its final
    Markdown text, returning (markdown, character_count, is_empty); is_empty is True
    when only a placeholder comment was emitted.
    '''
    title_text, title_kind = title
    pieces = []
    if title_text:
        # In the shared theme, h1 *is* the slide-title style: an absolutely
        # positioned title bar with the accent rule drawn by `h1::before`. h2 is
        # an inline subheading within the slide body. So a slide's title is an h1
        # whichever placeholder it came from - matching the hand-authored deck at
        # teaching/csci-232/lectures/lecture01-intro/, which uses h1 on every
        # slide. What the deck's opening slide additionally gets is the theme's
        # `lead` class, which recentres the title instead of parking it in the bar.
        if title_kind == 'ctrTitle' and slide_index == 1:
            pieces.append('<!-- _class: lead -->')
        pieces.append(f'# {title_text}')
    if subtitle:
        # A PowerPoint subtitle placeholder is a heading, not emphasised body
        # text: the theme has a `section.lead h2` rule sized for exactly this,
        # and the hand-authored reference deck's title slide is an h1 over an h2.
        pieces.append(f'## {subtitle}')
    if body_blocks:
        pieces.append(join_body_blocks(normalize_list_indentation(body_blocks)))
    is_empty = not pieces
    if is_empty:
        pieces.append(f'<!-- pptx2marp: slide {slide_index} has no extractable text or images -->')
    if notes_text:
        pieces.append(f'<!-- {notes_text} -->')
    markdown = '\n\n'.join(pieces)
    return markdown, sum(len(piece) for piece in pieces), is_empty


@dataclass
class DeckContext:
    '''
    The values that stay constant across every slide of one deck: the open archive,
    its part names, the media registry and warning log shared by all slides, the
    --code-lang hint for fenced code blocks, and the deck's real slide size in EMU.
    '''
    archive: zipfile.ZipFile
    names: set
    registry: MediaRegistry
    warnings: list
    code_lang: str = ''
    slide_width_emu: int = DEFAULT_SLIDE_WIDTH_EMU
    slide_height_emu: int = DEFAULT_SLIDE_HEIGHT_EMU

    def for_slide(self, relationships: dict, slide_index: int) -> SlideContext:
        '''Build the per-slide SlideContext for slide `slide_index` from this deck context.'''
        return SlideContext(deck=self, relationships=relationships, slide_index=slide_index)


def render_slide(deck: DeckContext, slide_part: str, slide_index: int):
    '''
    Render one slide part, returning (markdown, raw_title, char_count): raw_title guesses
    the deck-level title; char_count feeds the batch report's "no text" suspicion check.
    '''
    try:
        slide_root = ET.fromstring(deck.archive.read(slide_part))
    except (ET.ParseError, KeyError) as exc:
        deck.warnings.append(f'slide {slide_index} ({slide_part}): failed to parse ({exc})')
        text = f'<!-- pptx2marp: slide {slide_index} could not be parsed -->'
        return text, None, len(text)
    slide_rels = parse_rels(deck.archive, slide_part, deck.names)
    shape_tree = slide_root.find(f'{P_CSLD}/{P_SPTREE}')
    if shape_tree is None:
        text = f'<!-- pptx2marp: slide {slide_index} has no content tree -->'
        return text, None, len(text)
    title, subtitle, body_blocks = collect_slide_content(shape_tree, deck.for_slide(slide_rels, slide_index))
    notes_text = get_notes(deck.archive, slide_rels, deck.names)
    markdown, char_count, is_empty = assemble_slide(
        slide_index, title[:2], subtitle, body_blocks, notes_text
    )
    if is_empty:
        deck.warnings.append(f'slide {slide_index}: no extractable text or images')
    return markdown, title[2], char_count


def _single_unbulleted_paragraph_text(shape, relationships: dict) -> str | None:
    '''
    Return a `body` placeholder's text when it holds exactly one unbulleted paragraph -
    a candidate for folding onto a preceding title, see `try_merge_split_title` - or None
    when the shape does not have that shape (wrong placeholder type, more than one
    paragraph, a bullet, or no text).
    '''
    if get_placeholder_type(shape) != 'body':
        return None
    txbody = shape.find(P_TXBODY)
    if txbody is None:
        return None
    paragraphs = txbody.findall(A_P)
    if len(paragraphs) != 1:
        return None
    para_props = paragraphs[0].find(A_PPR)
    if para_props is None or para_props.find(A_BUNONE) is None:
        return None
    body_text = render_paragraph(paragraphs[0], relationships).strip()
    if not body_text:
        return None
    return body_text


def try_merge_split_title(shape, title_text, relationships: dict):
    '''
    Fold a `body` placeholder's text onto the preceding title text when PowerPoint looks
    to have split one title across two adjacent placeholders: the body holds exactly one
    unbulleted paragraph, and either that paragraph starts lowercase or the title itself
    ends without terminal punctuation - so joining the two reads as one sentence rather
    than accidentally merging an unrelated body paragraph into the title. Returns the
    combined title text, or None to leave both shapes alone.
    '''
    if title_text is None:
        return None
    body_text = _single_unbulleted_paragraph_text(shape, relationships)
    if body_text is None:
        return None
    title_unpunctuated = not title_text.rstrip().endswith((':', ';', '.', ',', '?', '!'))
    if not (body_text[0].islower() or title_unpunctuated):
        return None
    return f'{title_text} {body_text}'


def collect_slide_content(shape_tree, context: SlideContext):
    '''
    Walk a slide's shape tree once, returning ((title_text, title_kind, title_raw),
    subtitle_text, body_blocks); only the first title/subtitle are kept. A `body`
    placeholder immediately following the title, holding a single unbulleted paragraph
    that plausibly continues it, is folded onto the title instead - see
    `try_merge_split_title`.
    '''
    title = (None, None, None)
    subtitle = None
    body_blocks = []
    title_just_set = False
    for shape, in_group in iter_shapes_with_group_flag(shape_tree):
        if title_just_set and shape.tag == P_SP:
            merged = try_merge_split_title(shape, title[0], context.relationships)
            if merged is not None:
                title = (merged, title[1], title[2])
                title_just_set = False
                continue
        title_just_set = False
        outcome = render_shape(shape, context, body_blocks, in_group)
        if outcome is None:
            continue
        kind, payload, ph_kind, raw = outcome
        if kind == 'title' and title[0] is None:
            title = (payload, ph_kind, raw)
            title_just_set = True
        elif kind == 'subtitle' and subtitle is None:
            subtitle = payload
    return title, subtitle, body_blocks


def convert_deck(pptx_path: Path, theme: str = 'default', code_lang: str = '') -> DeckResult:
    '''
    Convert a single .pptx file into a DeckResult holding its Markdown and deduplicated
    media bytes. Never raises - failures are captured so a batch run can continue.
    `code_lang` is the language hint written after the opening fence of every code block
    detected in this deck (see `handle_sp`); pass '' for no hint.
    '''
    result = DeckResult(source=pptx_path)
    try:
        with zipfile.ZipFile(pptx_path) as archive:
            names = set(archive.namelist())
            slide_width_emu, slide_height_emu = pptx2marp_images.get_slide_size(archive)
            deck = DeckContext(
                archive=archive, names=names, registry=MediaRegistry(), warnings=result.warnings,
                code_lang=code_lang, slide_width_emu=slide_width_emu, slide_height_emu=slide_height_emu,
            )
            slide_blocks, deck_title = render_all_slides(deck, get_slide_order(archive, names), result)
            result.media = deck.registry.bytes_by_asset
            result.stats.images = len(result.media)
        if deck_title is None:
            deck_title = pptx_path.stem.replace('_', ' ').replace('-', ' ')
        body = '\n\n---\n\n'.join(slide_blocks)
        markdown = f'{front_matter(deck_title, theme)}\n\n{body}\n'
        result.markdown = strip_trailing_whitespace(markdown)
        return result
    except (zipfile.BadZipFile, OSError) as exc:
        result.ok = False
        result.error = f'could not open as a zip archive: {exc}'
        return result
    except Exception as exc:  # pylint: disable=broad-exception-caught
        # A batch run must survive any single malformed or unexpected deck.
        result.ok = False
        result.error = f'unexpected error: {exc}'
        return result


def render_all_slides(deck: DeckContext, slide_parts: list, result: DeckResult):
    '''
    Render every slide part in order onto `result.stats`, returning
    (slide_markdown_blocks, deck_title) - deck_title is slide 1's raw title, or None.
    '''
    result.stats.slides = len(slide_parts)
    if not slide_parts:
        deck.warnings.append('no slides found in this deck')
    deck_title = None
    slide_blocks = []
    for slide_index, slide_part in enumerate(slide_parts, start=1):
        markdown, title_raw, char_count = render_slide(deck, slide_part, slide_index)
        slide_blocks.append(markdown)
        result.stats.text_chars += char_count
        if slide_index == 1 and title_raw:
            deck_title = title_raw
    return slide_blocks, deck_title


def front_matter(title: str, theme: str) -> str:
    '''The Marp YAML front-matter block for a deck.'''
    return (
        '---\n'
        'marp: true\n'
        f'theme: {theme}\n'
        'paginate: true\n'
        f'title: {yaml_scalar(title)}\n'
        '---'
    )


def get_notes(archive: zipfile.ZipFile, slide_rels: dict, names: set):
    '''Look up and render this slide's speaker notes via its own .rels notesSlide entry.'''
    notes_entry = next(
        (entry for entry in slide_rels.values() if entry[0].endswith('/notesSlide')), None
    )
    if not notes_entry or notes_entry[1] not in names:
        return None
    try:
        notes_root = ET.fromstring(archive.read(notes_entry[1]))
    except ET.ParseError:
        return None
    notes_rels = parse_rels(archive, notes_entry[1], names)
    body_shape = None
    for shape in notes_root.iter(P_SP):
        placeholder = shape.find(f'{P_NVSPPR}/{P_NVPR}/{P_PH}')
        if placeholder is not None and placeholder.get('type') == 'body':
            body_shape = shape
            break
    if body_shape is None:
        return None
    txbody = body_shape.find(P_TXBODY)
    if txbody is None:
        return None
    lines = []
    for paragraph_el in txbody.findall(A_P):
        text = render_paragraph(paragraph_el, notes_rels)
        if text.strip():
            lines.append(text.strip())
    if not lines:
        return None
    return safe_comment_text('\n'.join(lines))


def write_deck(result: DeckResult, target_dir: Path) -> None:
    '''Write a converted deck's index.md and assets/ folder to disk.'''
    target_dir.mkdir(parents=True, exist_ok=True)
    (target_dir / 'index.md').write_text(result.markdown, encoding='utf-8')
    if result.media:
        assets_dir = target_dir / 'assets'
        assets_dir.mkdir(parents=True, exist_ok=True)
        for name, data in result.media.items():
            (assets_dir / name).write_bytes(data)


def discover_jobs(input_path: Path, out_root: Path):
    '''Build (pptx_path, target_dir) conversion jobs for a single file or a directory tree.'''
    if input_path.is_file():
        return [(input_path, out_root)]
    pptx_files = sorted(
        path for path in input_path.rglob('*.pptx') if not path.name.startswith('~$')
    )
    jobs = []
    for pptx_file in pptx_files:
        rel = pptx_file.relative_to(input_path).with_suffix('')
        jobs.append((pptx_file, out_root / rel))
    return jobs


def log_report(summary, dry_run: bool) -> dict:
    '''
    Log a per-deck line (or failure) plus batch totals, and return those totals as a
    dict (decks, failed, suspicious, slides, images) for the CLI's exit-code check.
    '''
    totals = {'decks': len(summary), 'failed': 0, 'suspicious': 0, 'slides': 0, 'images': 0}
    for pptx_path, target_dir, result in summary:
        if not result.ok:
            totals['failed'] += 1
            LOG.error('[FAIL] %s: %s', pptx_path, result.error)
            continue
        totals['slides'] += result.stats.slides
        totals['images'] += result.stats.images
        flag = ''
        if result.stats.suspicious:
            flag = '  <-- SUSPICIOUS (zero slides or no text)'
            totals['suspicious'] += 1
        action = 'would write' if dry_run else 'wrote'
        LOG.info(
            '[OK] %s -> %s (%d slides, %d images, %s)%s',
            pptx_path, target_dir, result.stats.slides, result.stats.images, action, flag,
        )
        for warning in result.warnings:
            LOG.warning('%s: %s', pptx_path, warning)
    LOG.info('---')
    for key in ('decks', 'failed', 'suspicious', 'slides', 'images'):
        LOG.info('total %s: %d', key, totals[key])
    return totals


def configure_logging(verbose: bool, quiet: bool) -> None:
    '''Point the root logger at stderr: DEBUG with --verbose, WARNING with --quiet, else INFO.'''
    level = logging.INFO
    if verbose:
        level = logging.DEBUG
    elif quiet:
        level = logging.WARNING
    logging.basicConfig(
        level=level, format='%(asctime)s %(levelname)s %(name)s: %(message)s', force=True
    )


def main(argv=None) -> int:
    '''CLI entry point: run every discovered job and return 0 if all decks converted cleanly.'''
    parser = argparse.ArgumentParser(
        prog='pptx2marp',
        description='Convert PowerPoint (.pptx) decks into Marp Markdown, stdlib only.',
    )
    parser.add_argument('input', help='A .pptx file, or a directory to search recursively')
    parser.add_argument('--out', required=True, help='Output directory')
    parser.add_argument(
        '--theme', default='default', help="Marp theme name for the front matter (default: default)"
    )
    parser.add_argument(
        '--dry-run', action='store_true', help='Report what would be produced without writing files'
    )
    parser.add_argument(
        '--code-lang', default='',
        help='Language hint written after the opening fence of every detected code block (default: none)'
    )
    verbosity = parser.add_mutually_exclusive_group()
    verbosity.add_argument('-v', '--verbose', action='store_true', help='Log at DEBUG level')
    verbosity.add_argument('-q', '--quiet', action='store_true', help='Log warnings and errors only')
    args = parser.parse_args(argv)
    configure_logging(args.verbose, args.quiet)
    input_path = Path(args.input)
    out_root = Path(args.out)
    if not input_path.exists():
        LOG.error('input path does not exist: %s', input_path)
        return 2
    jobs = discover_jobs(input_path, out_root)
    if not jobs:
        LOG.error('no .pptx files found under %s', input_path)
        return 2
    summary = []
    for pptx_path, target_dir in jobs:
        LOG.debug('converting %s', pptx_path)
        result = convert_deck(pptx_path, theme=args.theme, code_lang=args.code_lang)
        if result.ok and not args.dry_run:
            write_deck(result, target_dir)
        summary.append((pptx_path, target_dir, result))
    log_report(summary, dry_run=args.dry_run)
    return 0 if all(r.ok for _, _, r in summary) else 1


if __name__ == '__main__':
    sys.exit(main())
