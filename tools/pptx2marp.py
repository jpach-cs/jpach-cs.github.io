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
(P_SP, P_PIC, P_GRAPHICFRAME, P_CXNSP, P_GRPSP, P_NVSPPR, P_NVPICPR, P_NVPR, P_PH, P_TXBODY,
 P_BLIPFILL, P_CNVPR, P_CSLD, P_SPTREE, P_SLDIDLST) = _qns(
    'p', 'sp pic graphicFrame cxnSp grpSp nvSpPr nvPicPr nvPr ph txBody blipFill cNvPr cSld spTree sldIdLst')

MC_ALTERNATECONTENT, MC_FALLBACK, MC_CHOICE = _qns('mc', 'AlternateContent Fallback Choice')

(A_P, A_R, A_T, A_BR, A_FLD, A_RPR, A_PPR, A_BUNONE, A_HLINKCLICK, A_TBL, A_TR, A_TC, A_TXBODY,
 A_GRAPHIC, A_GRAPHICDATA, A_BLIP) = _qns(
    'a', 'p r t br fld rPr pPr buNone hlinkClick tbl tr tc txBody graphic graphicData blip')

(DGM_RELIDS,) = _qns('dgm', 'relIds')
R_EMBED, R_LINK, R_ID, R_DM = _qns('r', 'embed link id dm')

# Placeholder types that carry metadata (page number, footer, date, the thumbnail
# preview shown on the notes page) rather than slide content. These are always
# auto-generated fields, so skipping them never drops author-written content.
SKIP_PLACEHOLDER_TYPES = {'sldNum', 'ftr', 'dt', 'sldImg'}

IMAGE_EXTS = {'.png', '.gif', '.svg', '.jpg', '.jpeg'}

SLIDE_NUM_RE = re.compile(r'(\d+)')
LEADING_MARK_RE = re.compile(r'^(\s*)([#>]|[-*+](?=\s|$)|\d+\.(?=\s|$))')
THEMATIC_BREAK_RE = re.compile(r'^[-*_]{3,}$')
LIST_LINE_RE = re.compile(r'^\s*-\s')
LIST_ITEM_RE = re.compile(r'^( *)- (.*)$', re.DOTALL)

# Recognizes a bare URL/e-mail so it can be rewritten as a `<...>` autolink (MD034).
_BARE_URL_PATTERN = r'(?:https?://|www\.)[^\s<>\[\]()]+'
_BARE_EMAIL_PATTERN = r'[\w.+-]+@[\w-]+(?:\.[\w-]+)+'
BARE_URL_OR_EMAIL_RE = re.compile(f'{_BARE_URL_PATTERN}|{_BARE_EMAIL_PATTERN}')
_URL_TRAILING_PUNCTUATION = '.,;:!?"\')'

# Trailing chars stripped from a slide title (MD026); `?`/`!` are left as deliberate.
_TITLE_TRAILING_PUNCTUATION = ':;.,'
_HTML_ENTITY_SUFFIX_RE = re.compile(r'&(#x?[0-9a-fA-F]+|[a-zA-Z][a-zA-Z0-9]*);$')


def _escape_html(text: str) -> str:
    '''Escape only the characters HTML/Markdown would parse as markup.'''
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def escape_text(text: str) -> str:
    '''
    Escape characters that would be swallowed or misread as Markdown/HTML syntax - a CS
    course quotes things like `vector<int>`, `__FILE__`, `[width][.precision]` verbatim.
    Hard tabs are normalized to spaces here too, since they carry no meaning in Markdown.
    '''
    text = text.replace('\t', '    ')
    text = _escape_html(text)
    return (
        text.replace('[', '\\[').replace(']', '\\]')
        .replace('`', '\\`').replace('_', '\\_').replace('*', '\\*')
    )


def _split_trailing_punctuation(matched_text: str) -> tuple[str, str]:
    '''Split a regex match into (core, trailing punctuation) so `url.` keeps its dot out.'''
    core = matched_text
    trail = ''
    while core and core[-1] in _URL_TRAILING_PUNCTUATION:
        trail = core[-1] + trail
        core = core[:-1]
    return core, trail


def escape_and_wrap_urls(raw_text: str) -> str:
    '''
    Escape one run's raw text like `escape_text`, but first pull out any bare URL or
    e-mail address and wrap it in `<...>` (MD034) without corrupting it with the
    bracket/backtick/underscore escaping applied to the surrounding plain text.
    '''
    pieces = []
    cursor = 0
    for match in BARE_URL_OR_EMAIL_RE.finditer(raw_text):
        start, end = match.span()
        pieces.append(escape_text(raw_text[cursor:start]))
        # core is never empty: every match starts with a letter or ends in "@domain".
        core, trail = _split_trailing_punctuation(match.group(0))
        pieces.append(f'<{_escape_html(core)}>')
        pieces.append(escape_text(trail))
        cursor = end
    pieces.append(escape_text(raw_text[cursor:]))
    return ''.join(pieces)


def wrap_emphasis(text: str, bold: bool, italic: bool) -> str:
    '''
    Wrap `text` in bold/italic markers, moving leading/trailing whitespace outside them
    (MD037 forbids `** text **`); an all-whitespace run is left unmarked entirely.
    '''
    stripped = text.strip()
    if not stripped:
        return text
    lead = text[:len(text) - len(text.lstrip())]
    trail = text[len(text.rstrip()):]
    marker = '***' if bold and italic else ('**' if bold else '*')
    return f'{lead}{marker}{stripped}{marker}{trail}'


def strip_title_punctuation(text: str) -> str:
    '''
    Strip trailing `:;.,` from a slide title (MD026), leaving a deliberate `?`/`!`
    alone. Never touches an HTML entity's trailing `;` (e.g. `&amp;`), or empties a title.
    '''
    if _HTML_ENTITY_SUFFIX_RE.search(text):
        return text
    stripped = text.rstrip(_TITLE_TRAILING_PUNCTUATION).rstrip()
    return stripped or text


def strip_trailing_whitespace(markdown: str) -> str:
    '''Remove trailing spaces/tabs/non-breaking-spaces from every line (MD009).'''
    return '\n'.join(line.rstrip(' \t\xa0') for line in markdown.split('\n'))


def is_list_block(block: str) -> bool:
    '''True when `block` (as produced by handle_sp/render_diagram) is a list-item line.'''
    return bool(LIST_LINE_RE.match(block.split('\n', 1)[0]))


def join_body_blocks(blocks: list) -> str:
    '''
    Join a slide's body blocks: consecutive list-item lines join tightly (one newline,
    staying a single Markdown list); anything else - list next to non-list, or two
    non-list blocks - gets a blank line between them.
    '''
    if not blocks:
        return ''
    pieces = [blocks[0]]
    for previous, current in zip(blocks, blocks[1:]):
        separator = '\n' if is_list_block(previous) and is_list_block(current) else '\n\n'
        pieces.append(separator)
        pieces.append(current)
    return ''.join(pieces)


def normalize_list_indentation(blocks: list) -> list:
    '''
    Re-derive each list item's depth from its position in a run of list items, rather
    than the raw PPTX `lvl` it was indented with: a bullet run can open straight at
    `lvl="1"` with no `lvl="0"` parent, which Markdown cannot express (MD007/MD005).
    '''
    normalized = []
    level_stack: list = []
    for block in blocks:
        match = LIST_ITEM_RE.match(block)
        if match is None:
            level_stack = []
            normalized.append(block)
            continue
        raw_level = len(match.group(1)) // 2
        while level_stack and level_stack[-1] > raw_level:
            level_stack.pop()
        if not level_stack or level_stack[-1] < raw_level:
            level_stack.append(raw_level)
        normalized.append(('  ' * (len(level_stack) - 1)) + '- ' + match.group(2))
    return normalized


def protect_leading_marker(line: str) -> str:
    '''Escape a leading char sequence Markdown would parse as a block marker, but isn't one.'''
    match = LEADING_MARK_RE.match(line)
    if match:
        lead_ws, marker = match.group(1), match.group(2)
        rest = line[match.end():]
        if marker.endswith('.'):
            line = f'{lead_ws}{marker[:-1]}\\.{rest}'
        else:
            line = f'{lead_ws}\\{marker}{rest}'
    stripped = line.strip()
    if THEMATIC_BREAK_RE.match(stripped):
        line = line.replace(stripped, '\\' + stripped, 1)
    return line


def yaml_scalar(text: str) -> str:
    '''Quote `text` for safe use as a YAML front-matter scalar value.'''
    escaped = text.replace('\\', '\\\\').replace('"', '\\"')
    escaped = escaped.replace('\n', ' ').replace('\r', ' ')
    return f'"{escaped}"'


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


def safe_comment_text(text: str) -> str:
    '''Break up any "--" run so `text` cannot prematurely close its HTML comment.'''
    return re.sub(r'-{2,}', lambda m: '- ' * len(m.group(0)), text).strip()


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


def iter_shapes(container):
    '''
    Yield the content-bearing shapes (<p:sp>, <p:pic>, <p:graphicFrame>, <p:cxnSp>)
    inside `container` in document order, flattening <p:grpSp> groups and
    <mc:AlternateContent> (preferring Fallback, guaranteed schema-plain OOXML).
    '''
    for child in container:
        tag = child.tag
        if tag == MC_ALTERNATECONTENT:
            branch = child.find(MC_FALLBACK)
            if branch is None:
                branch = child.find(MC_CHOICE)
            if branch is not None:
                yield from iter_shapes(branch)
        elif tag == P_GRPSP:
            yield from iter_shapes(child)
        elif tag in (P_SP, P_PIC, P_GRAPHICFRAME, P_CXNSP):
            yield child


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


def handle_sp(shape, slide_rels: dict):
    '''
    Render one <p:sp> into (kind, payload, ph_type, raw_title_or_none) - kind is 'title',
    'subtitle', or 'body' - or None if the shape is metadata-only or carries no text.
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

    lines = []
    for paragraph_el in paragraphs:
        # A leading tab/space carries no meaning once the paragraph is its own Markdown
        # block; left in place it breaks the bullet-marker spacing (MD030) or turns an
        # ordinary paragraph into an accidental indented code block (MD046).
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
        if bullet:
            lines.append(('  ' * level) + '- ' + text)
        else:
            lines.append(text)
    return ('body', lines, ph_type, None) if lines else None


def handle_pic(picture_el, context: 'SlideContext'):
    '''
    Render one <p:pic> shape into an image reference, returning
    (alt_text, package_media_path) or None if it could not be resolved.
    '''
    blip = picture_el.find(f'{P_BLIPFILL}/{A_BLIP}')
    cnv_pr = picture_el.find(f'{P_NVPICPR}/{P_CNVPR}')
    alt = ''
    if cnv_pr is not None:
        alt = cnv_pr.get('descr') or cnv_pr.get('name') or ''
    alt = re.sub(r'[\[\]()]', '', alt).strip() or 'image'
    if blip is None:
        return None
    embed = blip.get(R_EMBED)
    if embed:
        entry = context.relationships.get(embed)
        if not entry or entry[1] not in context.names:
            context.warnings.append(
                f'slide {context.slide_index}: image relationship {embed} could not be resolved'
            )
            return None
        return (alt, entry[1])
    link = blip.get(R_LINK)
    if link:
        entry = context.relationships.get(link)
        url = entry[1] if entry else 'unknown'
        context.warnings.append(f'slide {context.slide_index}: linked (non-embedded) image skipped: {url}')
        return None
    return None


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
    '''The values every shape/picture/table renderer for one slide needs, bundled together.'''
    archive: zipfile.ZipFile
    names: set
    relationships: dict
    registry: MediaRegistry
    warnings: list
    slide_index: int


def render_image_shape(shape, context: SlideContext) -> str | None:
    '''
    Render a <p:pic> shape into a Markdown image line (with a format-warning comment
    appended for non-web formats like EMF), or None if it could not be resolved.
    '''
    picture = handle_pic(shape, context)
    if picture is None:
        return None
    alt, media_path = picture
    asset_name = context.registry.register(context.archive, media_path, context.warnings, context.slide_index)
    if asset_name is None:
        return None
    ext = posixpath.splitext(asset_name)[1].lower()
    img_line = f'![{alt}](assets/{asset_name})'
    if ext not in IMAGE_EXTS:
        img_line += (
            f'\n<!-- pptx2marp: {asset_name} is a {ext.lstrip(".").upper()} file; many '
            'browsers cannot render it inline. Re-export from PowerPoint as PNG/SVG if '
            'this slide looks blank. -->'
        )
        context.warnings.append(f'slide {context.slide_index}: non-web image format kept as-is: {asset_name}')
    return img_line


def render_graphic_frame(shape, context: SlideContext):
    '''
    Render a <p:graphicFrame> shape (table, SmartArt diagram, or something else OOXML
    can embed there) into a list of Markdown blocks to append to the slide body.
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
    context.warnings.append(f'slide {context.slide_index}: unsupported graphic content ({uri or "unknown"})')
    return [
        f'<!-- pptx2marp: unsupported embedded object on slide {context.slide_index} ({uri or "unknown"}) -->'
    ]


def render_shape(shape, context: SlideContext, body_blocks: list):
    '''
    Dispatch one flattened shape (see iter_shapes) to its renderer. Body content
    (images, tables, diagrams, bullet/paragraph text) is appended directly to
    `body_blocks`; a title or subtitle shape is instead returned to the caller, which
    keeps only the first of each per slide.
    '''
    tag = shape.tag
    if tag == P_SP:
        handled = handle_sp(shape, context.relationships)
        if handled is None:
            return None
        kind, payload, ph_kind, raw = handled
        if kind == 'body':
            body_blocks.extend(payload)
            return None
        return (kind, payload, ph_kind, raw)
    if tag == P_PIC:
        img_line = render_image_shape(shape, context)
        if img_line:
            body_blocks.append(img_line)
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
        heading = '#' if title_kind == 'ctrTitle' else '##'
        pieces.append(f'{heading} {title_text}')
    if subtitle:
        pieces.append(f'*{subtitle}*')
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
    its part names, and the media registry and warning log shared by all slides.
    '''
    archive: zipfile.ZipFile
    names: set
    registry: MediaRegistry
    warnings: list

    def for_slide(self, relationships: dict, slide_index: int) -> SlideContext:
        '''Build the per-slide SlideContext for slide `slide_index` from this deck context.'''
        return SlideContext(
            archive=self.archive, names=self.names, relationships=relationships,
            registry=self.registry, warnings=self.warnings, slide_index=slide_index,
        )


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


def collect_slide_content(shape_tree, context: SlideContext):
    '''
    Walk a slide's shape tree once, returning ((title_text, title_kind, title_raw),
    subtitle_text, body_blocks); only the first title/subtitle are kept.
    '''
    title = (None, None, None)
    subtitle = None
    body_blocks = []
    for shape in iter_shapes(shape_tree):
        outcome = render_shape(shape, context, body_blocks)
        if outcome is None:
            continue
        kind, payload, ph_kind, raw = outcome
        if kind == 'title' and title[0] is None:
            title = (payload, ph_kind, raw)
        elif kind == 'subtitle' and subtitle is None:
            subtitle = payload
    return title, subtitle, body_blocks


def convert_deck(pptx_path: Path, theme: str = 'default') -> DeckResult:
    '''
    Convert a single .pptx file into a DeckResult holding its Markdown and deduplicated
    media bytes. Never raises - failures are captured so a batch run can continue.
    '''
    result = DeckResult(source=pptx_path)
    try:
        with zipfile.ZipFile(pptx_path) as archive:
            names = set(archive.namelist())
            deck = DeckContext(
                archive=archive, names=names, registry=MediaRegistry(), warnings=result.warnings
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
        result = convert_deck(pptx_path, theme=args.theme)
        if result.ok and not args.dry_run:
            write_deck(result, target_dir)
        summary.append((pptx_path, target_dir, result))
    log_report(summary, dry_run=args.dry_run)
    return 0 if all(r.ok for _, _, r in summary) else 1


if __name__ == '__main__':
    sys.exit(main())
