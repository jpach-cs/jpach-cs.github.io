#!/usr/bin/env python3
'''
Pure text/Markdown helpers for tools/pptx2marp.py: escaping, emphasis, list normalization,
and other string-only transforms that never touch an XML element. Split out of
pptx2marp.py to keep that module under its line cap - see its module docstring.
'''

from __future__ import annotations

import re

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

# IDE/editor fonts a pasted code screenshot or paste-as-text box is set in; compared
# case-insensitively against a run's <a:latin typeface="...">.
MONOSPACE_TYPEFACES = {
    'consolas', 'cascadia mono', 'cascadia code', 'courier new', 'courier',
    'menlo', 'monaco', 'lucida console', 'source code pro',
}
CODE_SHAPE_MONOSPACE_RUN_RATIO = 0.6
CODE_SHAPE_MIN_PARAGRAPHS = 2
CODE_SHAPE_MIN_CHARACTERS = 15

# A slide's real display size, and the fixed-width canvas Marp themes render onto.
DEFAULT_SLIDE_WIDTH_EMU = 12192000
DEFAULT_SLIDE_HEIGHT_EMU = 6858000
MARP_CANVAS_WIDTH_PX = 1280
BACKGROUND_IMAGE_AREA_RATIO = 0.85


def is_monospace_typeface(typeface: str) -> bool:
    '''True when `typeface` (an <a:latin typeface="..."> value) names a code editor font.'''
    return typeface.strip().lower() in MONOSPACE_TYPEFACES


def is_code_shape(run_texts: list, monospace_flags: list, paragraph_count: int) -> bool:
    '''
    Decide whether a text shape is pasted source code rather than prose, from the runs
    already pulled out of its paragraphs: `run_texts[i]` is one run's text and
    `monospace_flags[i]` is whether that run's font is a code-editor monospace face
    (parallel lists). True when at least 60% of its runs are monospace AND the shape has
    either >= 2 paragraphs or >= 15 characters of text - long enough, or multi-line enough,
    that a monospace annotation callout ("Hello world!") does not get swept in.
    '''
    if not run_texts:
        return False
    monospace_ratio = sum(monospace_flags) / len(run_texts)
    if monospace_ratio < CODE_SHAPE_MONOSPACE_RUN_RATIO:
        return False
    total_characters = sum(len(text) for text in run_texts)
    return paragraph_count >= CODE_SHAPE_MIN_PARAGRAPHS or total_characters >= CODE_SHAPE_MIN_CHARACTERS


def render_code_fence(paragraph_lines: list, code_lang: str) -> str:
    '''
    Wrap a code shape's paragraph lines (already newline-joined per <a:br/>) in a fenced
    code block, one fence per deck-level `code_lang` hint. Paragraphs join with real
    newlines, verbatim - no Markdown escaping, no emphasis, no bullet processing. A
    4-backtick outer fence is used when the code itself contains a ``` line (e.g. a
    Markdown-lecture slide whose own example is a fenced block), so the outer fence still
    closes correctly.
    '''
    content = '\n'.join(paragraph_lines)
    fence = '````' if '```' in content else '```'
    return f'{fence}{code_lang}\n{content}\n{fence}'


def compute_image_size_prefix(cx: int, cy: int, slide_width_emu: int, slide_height_emu: int) -> str:
    '''
    Build the Marp image-sizing prefix for a picture displayed at cx x cy EMU on a slide
    sized slide_width_emu x slide_height_emu EMU: "bg " when the picture covers at least
    85% of the slide's area, otherwise "w:NNNpx " with NNN scaled from the slide's real
    width to the fixed 1280px Marp canvas (`cx / slide_width_emu * 1280`).
    '''
    if slide_width_emu <= 0 or slide_height_emu <= 0:
        return ''
    area_ratio = (cx * cy) / (slide_width_emu * slide_height_emu)
    if area_ratio >= BACKGROUND_IMAGE_AREA_RATIO:
        return 'bg '
    width_px = round(cx / slide_width_emu * MARP_CANVAS_WIDTH_PX)
    return f'w:{width_px}px '


def uncropped_extent(cx: int, cy: int, src_rect: tuple[int, int, int, int]) -> tuple[int, int]:
    '''
    Estimate a picture's un-cropped source extent from its cropped displayed size cx x cy
    EMU and its <a:srcRect> crop (l, t, r, b - each a percentage in thousandths of a
    percent, e.g. 20000 = 20%): the cropped edges are scaled back out proportionally.
    '''
    left, top, right, bottom = src_rect
    width_fraction = max(1 - (left + right) / 100000, 0.01)
    height_fraction = max(1 - (top + bottom) / 100000, 0.01)
    return round(cx / width_fraction), round(cy / height_fraction)


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


def safe_comment_text(text: str) -> str:
    '''Break up any "--" run so `text` cannot prematurely close its HTML comment.'''
    return re.sub(r'-{2,}', lambda m: '- ' * len(m.group(0)), text).strip()
