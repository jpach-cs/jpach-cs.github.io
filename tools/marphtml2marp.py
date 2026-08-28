#!/usr/bin/env python3
'''
Recover Marp Markdown from a deck that was committed only as marp-cli's rendered
`index.html`, using only the Python standard library.

marp-cli's bespoke HTML keeps everything the source carried: each `<section>` holds
the slide's rendered Markdown, its `data-*` attributes hold the directives that
applied to it (`class`, `paginate`, `footer`, `backgroundColor`), and the speaker
notes sit in `bespoke-marp-note` blocks indexed by slide. This tool walks that
markup back into `slides.md` so the deck can live in the source tree like every
other deck and be rendered by the build instead of committed.

Usage:
    python3 tools/marphtml2marp.py teaching/csci-112/lectures/lecture02/index.html
    python3 tools/marphtml2marp.py teaching/csci-112/lectures/lecture02/index.html --theme pach

Writes `slides.md` next to the given `index.html` (or to `--out`). The deck's inline
`style:` block is dropped in favour of `--theme`; the shared theme already carries
those rules, and `class: invert` is dropped for the same reason. Math rendered by
MathJax cannot be walked back to TeX from its glyph outlines: the tool emits the
characters it can recover inside `$...$` and warns, so those slides get a hand pass.
'''

from __future__ import annotations

import argparse
import html
import logging
import re
import sys
from dataclasses import dataclass, field
from html.parser import HTMLParser
from pathlib import Path

from pptx2marp_text import (
    protect_leading_marker,
    render_code_fence,
    safe_comment_text,
    strip_trailing_whitespace,
    yaml_scalar,
)

LOG = logging.getLogger('marphtml2marp')

VOID_TAGS = frozenset({'br', 'img', 'hr', 'path', 'use', 'rect', 'circle', 'line', 'input', 'source'})
BLOCK_TAGS = frozenset({
    'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'ul', 'ol', 'pre', 'table', 'div', 'blockquote', 'hr', 'footer',
})
# Classes the shared theme applies on its own, so a recovered deck does not restate them.
THEME_OWNED_CLASSES = frozenset({'invert'})
INLINE_ESCAPES = str.maketrans({'*': '\\*', '_': '\\_', '`': '\\`', '<': '\\<', '[': '\\[', ']': '\\]'})


@dataclass
class Node:
    '''One element of the parsed HTML tree; `children` mixes Nodes and text strings.'''

    tag: str
    attrs: dict = field(default_factory=dict)
    children: list = field(default_factory=list)

    def classes(self) -> list:
        '''The element's class names, in source order.'''
        return self.attrs.get('class', '').split()

    def text(self) -> str:
        '''All descendant text, in document order, with no markup.'''
        return ''.join(child if isinstance(child, str) else child.text() for child in self.children)

    def walk(self):
        '''Every descendant element, in document order.'''
        for child in self.children:
            if isinstance(child, Node):
                yield child
                yield from child.walk()

    def find_all(self, tag: str):
        '''Every descendant with the given tag, in document order.'''
        return (node for node in self.walk() if node.tag == tag)


class TreeBuilder(HTMLParser):
    '''Build a Node tree from HTML; tolerant of the unclosed void tags marp-cli emits.'''

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.root = Node('root')
        self.stack = [self.root]

    def handle_starttag(self, tag, attrs):
        node = Node(tag, {name: value or '' for name, value in attrs})
        self.stack[-1].children.append(node)
        if tag not in VOID_TAGS:
            self.stack.append(node)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID_TAGS:
            self.stack.pop()

    def handle_endtag(self, tag):
        for depth in range(len(self.stack) - 1, 0, -1):
            if self.stack[depth].tag == tag:
                del self.stack[depth:]
                return

    def handle_data(self, data):
        self.stack[-1].children.append(data)


def parse_html(markup: str) -> Node:
    '''Parse `markup` into a Node tree rooted at a synthetic `root` element.'''
    builder = TreeBuilder()
    builder.feed(markup)
    builder.close()
    return builder.root


def paragraph_lines(text: str) -> str:
    '''
    A paragraph's inline run as source lines. Marp renders with `breaks: true`, so
    each newline here renders as one line break; every line is protected against
    being misread as a block marker.
    '''
    return '\n'.join(protect_leading_marker(line.strip()) for line in text.strip().split('\n'))


def escape_inline(text: str) -> str:
    '''
    Escape prose so Markdown does not read emphasis, code, links, or HTML tags into it.
    Whitespace runs collapse to one space, as HTML rendering does: a newline in the
    source markup is formatting, not a break - `<br>` alone produces a break.
    '''
    return re.sub(r'\s+', ' ', text).translate(INLINE_ESCAPES)


def code_span(text: str) -> str:
    '''Wrap `text` in a backtick run longer than any run it contains; padding spaces are dropped (MD038).'''
    text = text.strip()
    longest = max((len(run) for run in re.findall(r'`+', text)), default=0)
    fence = '`' * (longest + 1)
    padding = ' ' if text.startswith('`') or text.endswith('`') else ''
    return f'{fence}{padding}{text}{padding}{fence}'


def image_markdown(node: Node) -> str:
    '''An `<img>` back to Marp image syntax, with the size keyword its inline style encoded.'''
    if 'emoji' in node.classes():
        return node.attrs.get('alt', '')
    alt = node.attrs.get('alt', '')
    keywords = re.findall(r'(width|height):\s*(\d+)px', node.attrs.get('style', ''))
    sizes = ' '.join(f'{name[0]}:{value}' for name, value in keywords)
    label = ' '.join(part for part in (alt, sizes) if part)
    return f'![{label}]({node.attrs.get("src", "")})'


def math_markdown(node: Node) -> str:
    '''
    The characters a MathJax SVG block can give back, wrapped in `$...$`. The TeX itself
    is gone, so the caller warns and the slide needs a hand pass.
    '''
    codepoints = []
    for glyph in node.walk():
        href = glyph.attrs.get('xlink:href', glyph.attrs.get('href', ''))
        match = re.search(r'-([0-9A-F]+)$', href)
        codepoints.append(match.group(1) if match else glyph.attrs.get('data-c', ''))
    recovered = ''.join(chr(int(code, 16)) for code in codepoints if code)
    return f'${recovered}$'


class MarkdownEmitter:
    '''Turn the slide's Node tree back into Markdown, one slide at a time.'''

    def __init__(self, slide_number: int) -> None:
        self.slide_number = slide_number
        self.warnings: list = []

    def inline(self, children: list) -> str:
        '''Render inline content (text, emphasis, code, links, images, breaks) to Markdown.'''
        return ''.join(self.inline_one(child) for child in children)

    def inline_one(self, child) -> str:
        '''Render one inline child.'''
        if isinstance(child, str):
            return escape_inline(child)
        handler = {
            'strong': lambda n: f'**{self.inline(n.children)}**',
            'b': lambda n: f'**{self.inline(n.children)}**',
            'em': lambda n: f'*{self.inline(n.children)}*',
            'i': lambda n: f'*{self.inline(n.children)}*',
            'code': lambda n: code_span(n.text()),
            'a': lambda n: f'[{self.inline(n.children)}]({n.attrs.get("href", "")})',
            'br': lambda _: '\n',
            'img': image_markdown,
            'mjx-container': self.math,
            'span': lambda n: self.inline(n.children),
            'sup': lambda n: f'<sup>{self.inline(n.children)}</sup>',
            'sub': lambda n: f'<sub>{self.inline(n.children)}</sub>',
        }.get(child.tag)
        if handler is None:
            self.warnings.append(f'slide {self.slide_number}: inline <{child.tag}> flattened to its text')
            return self.inline(child.children)
        return handler(child)

    def math(self, node: Node) -> str:
        '''Inline math, with the warning that makes the hand pass findable.'''
        recovered = math_markdown(node)
        self.warnings.append(f'slide {self.slide_number}: MathJax block recovered only as {recovered}; restore its TeX')
        return recovered

    def blocks(self, children: list) -> list:
        '''Render a sequence of block-level children; stray inline runs become paragraphs.'''
        rendered: list = []
        run: list = []
        for child in children:
            if isinstance(child, Node) and (child.tag in BLOCK_TAGS or child.tag == 'footer'):
                self.flush_run(run, rendered)
                block = self.block(child)
                if block:
                    rendered.append(block)
            else:
                run.append(child)
        self.flush_run(run, rendered)
        return rendered

    def flush_run(self, run: list, rendered: list) -> None:
        '''Emit any pending inline run as a paragraph and clear it.'''
        text = self.inline(run).strip()
        run.clear()
        if text:
            rendered.append(paragraph_lines(text))

    def block(self, node: Node) -> str:
        '''Render one block element to Markdown.'''
        if node.tag[0] == 'h' and node.tag[1:].isdigit():
            # A heading is one source line, so a break inside it must stay literal.
            text = self.inline(node.children).strip().replace('\n', '<br>')
            return f'{"#" * int(node.tag[1:])} {text}'
        handler = {
            'footer': lambda _: '',
            'p': lambda n: paragraph_lines(self.inline(n.children)),
            'ul': self.list_block,
            'ol': self.list_block,
            'pre': self.code_block,
            'table': self.table,
            'hr': lambda _: '***',
            'blockquote': self.blockquote,
        }.get(node.tag, self.raw_html)
        return handler(node)

    def blockquote(self, node: Node) -> str:
        '''A `<blockquote>`, each inner line prefixed.'''
        inner = '\n\n'.join(self.blocks(node.children))
        return '\n'.join(f'> {line}'.rstrip() for line in inner.split('\n'))

    def raw_html(self, node: Node) -> str:
        '''A `<div>` (or other container) kept as raw HTML around Markdown content.'''
        attrs = ''.join(f' {name}="{html.escape(value, quote=True)}"' for name, value in node.attrs.items())
        inner = '\n\n'.join(self.blocks(node.children))
        if not inner:
            return f'<{node.tag}{attrs}></{node.tag}>'
        return f'<{node.tag}{attrs}>\n\n{inner}\n\n</{node.tag}>'

    def list_block(self, node: Node, indent: str = '') -> str:
        '''A `<ul>`/`<ol>` with its nesting; nested lists indent by the width of their parent marker.'''
        lines: list = []
        number = 1
        for item in node.children:
            if not isinstance(item, Node) or item.tag != 'li':
                continue
            marker = f'{number}.' if node.tag == 'ol' else '-'
            number += 1
            lines.append('\n'.join(self.list_item(item, marker, indent)))
        loose = any(child.tag == 'p' for item in node.children if isinstance(item, Node)
                    for child in item.children if isinstance(child, Node))
        return ('\n\n' if loose else '\n').join(lines)

    def list_item(self, item: Node, marker: str, indent: str) -> list:
        '''One `<li>`: its own inline text, then any nested lists or blocks beneath it.'''
        inner = indent + ' ' * (len(marker) + 1)
        lines: list = []
        run: list = []
        first = True
        for child in item.children:
            if isinstance(child, Node) and child.tag == 'p':
                run.extend(child.children)
            elif isinstance(child, Node) and child.tag in ('ul', 'ol'):
                lines.extend(self.item_line(run, f'{indent}{marker}' if first else inner))
                first = False
                lines.append(self.list_block(child, inner))
            elif isinstance(child, Node) and child.tag in BLOCK_TAGS:
                lines.extend(self.item_line(run, f'{indent}{marker}' if first else inner))
                first = False
                block = self.block(child)
                lines.append('')
                lines.append('\n'.join(f'{inner}{line}'.rstrip() for line in block.split('\n')))
            else:
                run.append(child)
        lines.extend(self.item_line(run, f'{indent}{marker}' if first else inner))
        return lines

    def item_line(self, run: list, lead: str) -> list:
        '''
        Flush the item's pending inline run onto one line. `lead` is the indented marker
        for the item's first line, or the continuation indent after a nested block; a
        continuation with no text is dropped, a marker line is kept even when empty.
        '''
        cont = '\n' + ' ' * (len(lead) + (0 if lead.endswith(' ') else 1))
        text = cont.join(line.strip() for line in self.inline(run).strip().split('\n'))
        run.clear()
        if lead.endswith(' '):
            return [f'{lead}{text}'] if text else []
        return [f'{lead} {text}'.rstrip()]

    def code_block(self, node: Node) -> str:
        '''A `<pre><code class="language-x">` back to a fenced block; highlighting spans drop away.'''
        code = next(iter(node.find_all('code')), node)
        language = ''
        for name in code.classes():
            if name.startswith('language-'):
                language = name[len('language-'):]
        content = code.text()
        if content.endswith('\n'):
            content = content[:-1]
        return render_code_fence(content.split('\n'), language)

    def table(self, node: Node) -> str:
        '''A `<table>` to a GFM pipe table; the first row is the header.'''
        rows = [
            [self.inline(cell.children).strip().replace('|', '\\|').replace('\n', '<br>') for cell in row.children
             if isinstance(cell, Node) and cell.tag in ('th', 'td')]
            for row in node.find_all('tr')
        ]
        if not rows:
            return ''
        width = max(len(row) for row in rows)
        rows = [row + [''] * (width - len(row)) for row in rows]
        lines = ['| ' + ' | '.join(rows[0]) + ' |', '|' + ' --- |' * width]
        lines.extend('| ' + ' | '.join(row) + ' |' for row in rows[1:])
        return '\n'.join(lines)


@dataclass
class Slide:
    '''One recovered slide: its directives, Markdown body, note, and any warnings.'''

    classes: list
    paginate: str
    body: str
    note: str = ''
    style: str = ''
    warnings: list = field(default_factory=list)


@dataclass
class Deck:
    '''Everything recovered from one `index.html`.'''

    title: str
    footer: str
    background: str
    slides: list = field(default_factory=list)


def slide_sections(root: Node) -> list:
    '''The `<section>` elements that are slides: those carrying Marp's data attributes.'''
    return [section for section in root.find_all('section') if 'data-class' in section.attrs
            or 'data-paginate' in section.attrs or 'data-marpit-pagination' in section.attrs]


def scoped_style(markup: str, section: Node) -> str:
    '''
    The `<style scoped>` block a slide carried, walked back from Marpit's scoping.
    Marpit turns such a block into rules whose selectors carry the slide's unique
    `data-marpit-scope-*` attribute; stripping everything through that attribute
    gives back the author's selector. The `--marpit-root-font-size` helper rules
    Marpit derives from em font sizes are its own, not the author's, and are skipped.
    '''
    scope = next((name[len('data-marpit-scope-'):] for name in section.attrs if name.startswith('data-marpit-scope-')), '')
    if not scope:
        return ''
    # html.parser lowercases attribute names; the marker in the CSS keeps its case.
    match = re.search(re.escape(f'data-marpit-scope-{scope}'), markup, re.IGNORECASE)
    if match is None:
        return ''
    marker = f'[{match.group(0)}]'
    rules: list = []
    for selector_text, body in re.findall(r'([^{}]+)\{([^{}]*)\}', markup):
        if marker not in selector_text or '--marpit-root-font-size' in body:
            continue
        parts = [part.split(marker)[-1].strip() or 'section' for part in selector_text.split(',') if marker in part]
        declarations = '; '.join(part.strip() for part in body.split(';') if part.strip())
        rule = f'{", ".join(dict.fromkeys(parts))} {{ {declarations} }}'
        if rule not in rules:
            rules.append(rule)
    if not rules:
        return ''
    joined = '\n'.join(rules)
    return f'<style scoped>\n{joined}\n</style>'


def notes_by_index(root: Node) -> dict:
    '''Speaker notes keyed by 0-based slide index, as plain text.'''
    notes = {}
    for div in root.find_all('div'):
        if 'bespoke-marp-note' in div.classes():
            text = '\n'.join(part.strip() for part in div.text().split('\n')).strip()
            if text:
                notes[int(div.attrs.get('data-index', '0'))] = text
    return notes


def recover_deck(markup: str) -> Deck:
    '''Walk marp-cli's HTML back into a Deck of slides.'''
    root = parse_html(markup)
    title = next((node.text().strip() for node in root.find_all('title')), '')
    sections = slide_sections(root)
    notes = notes_by_index(root)
    first = sections[0].attrs if sections else {}
    deck = Deck(title, html.unescape(first.get('data-footer', '')), first.get('data-background-color', ''))
    for index, section in enumerate(sections):
        emitter = MarkdownEmitter(index + 1)
        body = '\n\n'.join(emitter.blocks(section.children))
        classes = [name for name in section.attrs.get('data-class', '').split() if name not in THEME_OWNED_CLASSES]
        deck.slides.append(Slide(classes, section.attrs.get('data-paginate', ''), body, notes.get(index, ''),
                                 scoped_style(markup, section), emitter.warnings))
    return deck


def front_matter(deck: Deck, theme: str) -> str:
    '''The YAML front matter: theme and pagination, plus the footer and background the deck carried.'''
    lines = ['---', 'marp: true', f'theme: {theme}', 'paginate: true']
    if deck.footer:
        lines.append(f'footer: {yaml_scalar(deck.footer)}')
    if deck.background:
        lines.append(f'backgroundColor: {yaml_scalar(deck.background)}')
    lines.append(f'title: {yaml_scalar(deck.title)}')
    lines.append('---')
    return '\n'.join(lines)


def render_slide(slide: Slide) -> str:
    '''One slide's Markdown: per-slide directives, body, then the note as a comment.'''
    parts = []
    if slide.classes:
        parts.append(f'<!-- _class: {" ".join(slide.classes)} -->')
    if slide.paginate == 'skip':
        parts.append('<!-- _paginate: skip -->')
    if slide.style:
        parts.append(slide.style)
    if slide.body:
        parts.append(slide.body)
    if slide.note:
        parts.append(f'<!--\n{safe_comment_text(slide.note)}\n-->')
    if not parts:
        parts.append('<!-- blank slide in the source -->')
    return '\n\n'.join(parts)


def render_deck(deck: Deck, theme: str) -> str:
    '''The whole `slides.md`.'''
    slides = '\n\n---\n\n'.join(render_slide(slide) for slide in deck.slides)
    return strip_trailing_whitespace(f'{front_matter(deck, theme)}\n\n{slides}\n')


def convert(source: Path, target: Path, theme: str) -> int:
    '''Recover `source` into `target`; returns the number of warnings logged.'''
    deck = recover_deck(source.read_text(encoding='utf-8'))
    warnings = [warning for slide in deck.slides for warning in slide.warnings]
    for warning in warnings:
        LOG.warning('%s: %s', source, warning)
    target.write_text(render_deck(deck, theme), encoding='utf-8')
    LOG.info('%s: %d slides -> %s', source, len(deck.slides), target)
    return len(warnings)


def main(argv=None) -> int:
    '''Command-line entry point.'''
    parser = argparse.ArgumentParser(description='Recover Marp Markdown from a marp-cli HTML render.')
    parser.add_argument('source', type=Path, help='the rendered index.html')
    parser.add_argument('--out', type=Path, help='where to write slides.md (default: beside the source)')
    parser.add_argument('--theme', default='pach', help='theme name for the front matter (default: pach)')
    parser.add_argument('-q', '--quiet', action='store_true', help='only report warnings')
    args = parser.parse_args(argv)
    logging.basicConfig(level=logging.WARNING if args.quiet else logging.INFO, format='%(levelname)s: %(message)s')
    target = args.out if args.out else args.source.with_name('slides.md')
    convert(args.source, target, args.theme)
    return 0


if __name__ == '__main__':
    sys.exit(main())
