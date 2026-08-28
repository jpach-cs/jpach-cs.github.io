'''
Unit tests for tools/marphtml2marp.py.

Every input is a hand-written fragment of the HTML marp-cli emits, so each test
states exactly which markup it walks back to Markdown. Nothing on disk except the
one round-trip through `main`.
'''

from __future__ import annotations

import logging
from pathlib import Path

import pytest

import marphtml2marp as m

STYLE = 'section { color: red }'


def section(body: str, classes: str = 'invert', paginate: str = 'true', **extra) -> str:
    '''One slide `<section>` carrying the data attributes marp-cli writes.'''
    attrs = ' '.join(f'{name.replace("_", "-")}="{value}"' for name, value in extra.items())
    return (
        f'<section id="1" data-class="{classes}" data-paginate="{paginate}" '
        f'data-background-color="#fdfaf3" data-footer="CSCI 112 | C |  J. L. Pach" '
        f'data-theme="default" data-style="{STYLE}" {attrs}>{body}'
        '<footer>CSCI 112 | C |  J. L. Pach</footer></section>'
    )


def document(*sections: str, notes: str = '') -> str:
    '''A minimal bespoke document: title, slides, and the notes container.'''
    return f'<html><head><title>CSCI 112</title></head><body>{"".join(sections)}{notes}</body></html>'


def note(index: int, text: str) -> str:
    '''A speaker-note block for the 0-based slide `index`.'''
    return f'<div class="bespoke-marp-note" data-index="{index}" tabindex="0"><p>{text}</p></div>'


def body_of(markup: str) -> str:
    '''The Markdown body of the first slide of `markup`, directives and all.'''
    deck = m.recover_deck(markup)
    return m.render_slide(deck.slides[0])


# --- parsing ---------------------------------------------------------------------------


def test_tree_builder_tolerates_unclosed_void_tags_and_stray_end_tags():
    '''Tree builder tolerates unclosed void tags and stray end tags.'''
    root = m.parse_html('<p>a<br>b<img src="x.png"></p></span><p>c</p>')
    paragraphs = list(root.find_all('p'))
    assert [p.text() for p in paragraphs] == ['ab', 'c']
    assert [child.tag for child in paragraphs[0].children if isinstance(child, m.Node)] == ['br', 'img']


def test_slide_sections_ignore_sections_without_marp_attributes():
    '''Slide sections ignore sections without marp attributes.'''
    root = m.parse_html('<section>nav</section>' + section('<h1>A</h1>'))
    assert len(m.slide_sections(root)) == 1


# --- inline markup ---------------------------------------------------------------------


def test_inline_markup_round_trips():
    '''Inline markup round trips.'''
    markup = section(
        '<p>Use <strong>bold</strong>, <em>it</em>, <b>b</b>, <i>i</i>, <code>x</code>, '
        '<a href="https://example.org/">link</a>, <sup>2</sup><sub>0</sub> and <span>span</span></p>'
    )
    assert body_of(markup) == (
        'Use **bold**, *it*, **b**, *i*, `x`, [link](https://example.org/), <sup>2</sup><sub>0</sub> and span'
    )


def test_breaks_render_as_newlines_since_marp_sets_breaks_true():
    '''A <br> in a paragraph or list item becomes a plain newline; each line is protected.'''
    assert body_of(section('<p>a<br />- b</p>')) == 'a\n\\- b'
    assert body_of(section('<ul><li>x<br />y line</li></ul>')) == '- x\n  y line'


def test_breaks_stay_literal_where_markdown_cannot_hold_a_newline():
    '''Headings and table cells keep a literal <br>.'''
    assert body_of(section('<h1>Bit<br />Byte</h1>')) == '# Bit<br>Byte'


def test_prose_is_escaped_so_markdown_does_not_reparse_it():
    '''Prose is escaped so markdown does not reparse it.'''
    assert body_of(section('<p>a * b _c_ `d` &lt;stdio.h&gt; [e]</p>')) == r'a \* b \_c\_ \`d\` \<stdio.h> \[e\]'


def test_source_markup_newlines_are_spaces_not_breaks():
    '''Source markup newlines are spaces, not breaks.'''
    assert body_of(section('<p>a\n   b<br />\nc</p>')) == 'a b\nc'
    assert body_of(section('<ul><li>x<br />\ny</li></ul>')) == '- x\n  y'


def test_code_span_uses_a_longer_fence_than_its_content_and_drops_padding():
    '''Code span uses a longer fence than its content and drops padding.'''
    assert m.code_span('a`b') == '``a`b``'
    assert m.code_span('`a') == '`` `a ``'
    assert m.code_span(' git branch ') == '`git branch`'


def test_image_size_keywords_come_from_inline_style_and_emoji_become_text():
    '''Image size keywords come from inline style and emoji become text.'''
    markup = section(
        '<p><img src="a.svg" alt="A" style="height:460px;" /><img src="b.png" alt="" style="width:500px;" />'
        '<img class="emoji" draggable="false" alt="✅" src="https://twemoji/2705.svg" data-marp-twemoji="" /></p>'
    )
    assert body_of(markup) == '![A h:460](a.svg)![w:500](b.png)✅'


def test_unknown_inline_tag_is_flattened_with_a_warning():
    '''Unknown inline tag is flattened with a warning.'''
    deck = m.recover_deck(document(section('<p>a <kbd>Ctrl</kbd> b</p>')))
    assert deck.slides[0].body == 'a Ctrl b'
    assert deck.slides[0].warnings == ['slide 1: inline <kbd> flattened to its text']


# --- math ------------------------------------------------------------------------------


def test_mathjax_glyphs_are_recovered_from_data_c_and_use_hrefs_with_a_warning():
    '''Mathjax glyphs are recovered from data c and use hrefs with a warning.'''
    markup = section(
        '<p>x <mjx-container class="MathJax" jax="SVG"><svg><g><path data-c="2192" d="M0"></path>'
        '<use data-c="41" xlink:href="#MJX-1-TEX-I-1D434"></use></g></svg></mjx-container></p>'
    )
    deck = m.recover_deck(document(markup))
    assert deck.slides[0].body == 'x $→\U0001d434$'
    assert deck.slides[0].warnings == ['slide 1: MathJax block recovered only as $→\U0001d434$; restore its TeX']


# --- block markup ----------------------------------------------------------------------


def test_headings_paragraphs_rules_and_blockquotes():
    '''Headings paragraphs rules and blockquotes.'''
    markup = section('<h1 id="t">Title:</h1><h3>Sub</h3><p>Para</p><hr /><blockquote><p>q1</p><p>q2</p></blockquote>')
    assert body_of(markup) == '# Title:\n\n### Sub\n\nPara\n\n***\n\n> q1\n>\n> q2'


def test_leading_markers_in_prose_are_protected():
    '''Leading markers in prose are protected.'''
    assert body_of(section('<p>1. not a list</p><p>- nor this</p>')) == '1\\. not a list\n\n\\- nor this'


def test_nested_lists_indent_by_the_parent_marker_width():
    '''Nested lists indent by the parent marker width.'''
    markup = section(
        '<ul><li>one<ul><li>deep</li></ul></li><li>two</li></ul>'
        '<ol><li>first<ul><li>under a number</li></ul></li><li>second</li></ol>'
    )
    assert body_of(markup) == (
        '- one\n  - deep\n- two\n\n1. first\n   - under a number\n2. second'
    )


def test_loose_list_items_are_separated_by_blank_lines():
    '''Loose list items are separated by blank lines.'''
    markup = section('<ul><li><p>a</p></li><li><p>b</p></li></ul>')
    assert body_of(markup) == '- a\n\n- b'


def test_block_inside_a_list_item_is_indented_after_a_blank_line():
    '''Block inside a list item is indented after a blank line.'''
    markup = section('<ul><li>lead<table><tr><th>h</th></tr><tr><td>c</td></tr></table>tail</li></ul>')
    assert body_of(markup) == '- lead\n\n  | h |\n  | --- |\n  | c |\n  tail'


def test_list_item_with_only_a_nested_list_keeps_its_marker_line():
    '''List item with only a nested list keeps its marker line.'''
    assert body_of(section('<ul><li><ul><li>x</li></ul></li></ul>')) == '-\n  - x'


def test_code_block_language_and_highlighting_spans():
    '''Code block language and highlighting spans.'''
    markup = section(
        '<pre is="marp-pre" data-auto-scaling="downscale-only"><code class="language-c">'
        '<span class="hljs-type">int</span> x;\n  y();\n</code></pre>'
        '<pre><code>plain</code></pre>'
    )
    assert body_of(markup) == '```c\nint x;\n  y();\n```\n\n```\nplain\n```'


def test_table_cells_escape_pipes_and_short_rows_are_padded():
    '''Table cells escape pipes and short rows are padded.'''
    markup = section(
        '<table><thead><tr><th>a|b</th><th>c</th></tr></thead>'
        '<tbody><tr><td><img src="i.svg" alt="I" /></td><td>x<br />y</td></tr><tr><td>short</td></tr></tbody></table>'
    )
    assert body_of(markup) == '| a\\|b | c |\n| --- | --- |\n| ![I](i.svg) | x<br>y |\n| short |  |'


def test_empty_table_renders_nothing():
    '''Empty table renders nothing.'''
    assert m.MarkdownEmitter(1).table(m.Node('table')) == ''


def test_div_wrappers_survive_as_raw_html_around_markdown():
    '''Div wrappers survive as raw html around markdown.'''
    markup = section('<div class="columns"><div class="column-left"><p>a</p></div><div></div></div>')
    assert body_of(markup) == (
        '<div class="columns">\n\n<div class="column-left">\n\na\n\n</div>\n\n<div></div>\n\n</div>'
    )


def test_stray_inline_content_between_blocks_becomes_a_paragraph():
    '''Stray inline content between blocks becomes a paragraph.'''
    assert body_of(section('<h1>T</h1>loose <strong>text</strong><p>p</p>')) == '# T\n\nloose **text**\n\np'


# --- directives, notes, front matter ---------------------------------------------------


def test_directives_drop_theme_owned_classes_and_keep_the_rest():
    '''Directives drop theme owned classes and keep the rest.'''
    deck = m.recover_deck(document(
        section('<h1>A</h1>', classes='lead invert', paginate='skip'),
        section('<h1>B</h1>', classes='invert'),
        section('<h1>C</h1>', classes='code-description invert fit-70'),
    ))
    assert [s.classes for s in deck.slides] == [['lead'], [], ['code-description', 'fit-70']]
    assert m.render_slide(deck.slides[0]) == '<!-- _class: lead -->\n\n<!-- _paginate: skip -->\n\n# A'
    assert m.render_slide(deck.slides[1]) == '# B'


def test_notes_attach_to_their_slide_and_cannot_close_the_comment():
    '''Notes attach to their slide and cannot close the comment.'''
    deck = m.recover_deck(document(
        section('<h1>A</h1>'), section('<h1>B</h1>'),
        notes=note(1, 'say -- this\n  and that') + note(0, '   '),
    ))
    assert deck.slides[0].note == ''
    assert m.render_slide(deck.slides[1]) == '# B\n\n<!--\nsay - -  this\nand that\n-->'


def test_blank_slide_gets_a_placeholder_comment():
    '''Blank slide gets a placeholder comment.'''
    deck = m.recover_deck(document(section('')))
    assert m.render_slide(deck.slides[0]) == '<!-- blank slide in the source -->'


def test_front_matter_carries_footer_background_and_title():
    '''Front matter carries footer background and title.'''
    deck = m.recover_deck(document(section('<h1>A</h1>')))
    assert m.front_matter(deck, 'pach') == (
        '---\nmarp: true\ntheme: pach\npaginate: true\nfooter: "CSCI 112 | C |  J. L. Pach"\n'
        'backgroundColor: "#fdfaf3"\ntitle: "CSCI 112"\n---'
    )


def test_front_matter_omits_what_the_deck_did_not_carry():
    '''Front matter omits what the deck did not carry.'''
    deck = m.Deck(title='', footer='', background='')
    assert m.front_matter(deck, 'pach') == '---\nmarp: true\ntheme: pach\npaginate: true\ntitle: ""\n---'


def test_empty_document_yields_an_empty_deck():
    '''Empty document yields an empty deck.'''
    deck = m.recover_deck('<html><body></body></html>')
    assert not deck.slides and deck.footer == '' and deck.title == ''


def test_render_deck_strips_trailing_whitespace_and_joins_slides():
    '''Render deck strips trailing whitespace and joins slides.'''
    deck = m.recover_deck(document(section('<h2></h2>'), section('<p>b </p>')))
    assert m.render_deck(deck, 'pach').endswith('---\n\n##\n\n---\n\nb\n')


# --- command line ----------------------------------------------------------------------


def test_main_writes_slides_md_beside_the_source_and_logs_warnings(tmp_path: Path, caplog):
    '''Main writes slides md beside the source and logs warnings.'''
    source = tmp_path / 'index.html'
    source.write_text(document(section('<p><mjx-container><svg><path data-c="41"></path></svg></mjx-container></p>')),
                      encoding='utf-8')
    with caplog.at_level(logging.WARNING):
        assert m.main([str(source), '-q']) == 0
    assert (tmp_path / 'slides.md').read_text(encoding='utf-8').endswith('---\n\n$A$\n')
    assert 'restore its TeX' in caplog.text


def test_main_honours_out_and_theme(tmp_path: Path):
    '''Main honours out and theme.'''
    source = tmp_path / 'index.html'
    source.write_text(document(section('<h1>A</h1>')), encoding='utf-8')
    target = tmp_path / 'out' / 'deck.md'
    target.parent.mkdir()
    assert m.main([str(source), '--out', str(target), '--theme', 'gaia']) == 0
    assert 'theme: gaia' in target.read_text(encoding='utf-8')


@pytest.mark.parametrize('tag', ['h1', 'h6'])
def test_heading_levels(tag: str):
    '''Heading levels.'''
    assert body_of(section(f'<{tag}>x</{tag}>')) == f'{"#" * int(tag[1])} x'


def test_scoped_style_blocks_are_recovered():
    '''Scoped style blocks are recovered.'''
    markup = document(
        '<style>div#p > section[data-marpit-scope-aBc] .columns{display:flex;gap:30px}'
        'section[data-marpit-scope-aBc]{font-size:20px}'
        'section[data-marpit-scope-aBc] div#p section.x{--marpit-root-font-size: 0.5em}'
        'section[data-marpit-scope-other] .y{color:red}</style>'
        + section('<h1>A</h1>', **{'data_marpit_scope_aBc': ''}) + section('<h1>B</h1>')
    )
    deck = m.recover_deck(markup)
    assert m.render_slide(deck.slides[0]) == (
        '<style scoped>\n.columns { display:flex; gap:30px }\nsection { font-size:20px }\n</style>\n\n# A'
    )
    assert deck.slides[1].style == ''
