'''
Layer 1 content check: every deck follows the shared theme's styling contract.

`assets/marp/theme.css` is the only styling mechanism the decks may use, and it
assigns specific meanings to the markup:

  * `h1` IS the slide-title style - an absolutely positioned title bar in
    --color-primary with the accent rule drawn by `h1::before`. `h2` is an
    inline subheading within the slide body.
  * `section.lead` recentres a title slide, `section.caption-slide` styles a
    divider, and `section.long-title` rescues a title too long for the bar.

The hand-authored reference deck at teaching/csci-232/lectures/lecture01-intro/
uses `<h1>` on all 25 of its slides and `<h2>` only for subheads inside a
slide. The decks converted from PowerPoint originally used `##` for every
slide title, so no converted slide rendered in the title bar at all. These
checks keep them in line with the reference deck.
'''

from __future__ import annotations

import re
from pathlib import Path

import pytest

from repo import TEACHING_ROOT

# The section classes assets/marp/theme.css actually defines. A deck may not
# name a class the theme has no rule for - it would silently do nothing.
THEME_CLASSES = frozenset({
    'lead', 'caption-slide', 'code-description', 'small-code', 'tiny-code', 'long-title',
    # The tighter metrics the PowerPoint-converted decks run at; deck-level and on every _class line.
    'compact',
    # PowerPoint's autofit shrink factor, carried over by the converter.
    'fit-90', 'fit-80', 'fit-70', 'fit-60', 'fit-50', 'fit-40', 'fit-30',
})

FRONT_MATTER_PATTERN = re.compile(r'\A---\r?\n.*?\r?\n---\r?\n', re.DOTALL)
CLASS_DIRECTIVE_PATTERN = re.compile(r'<!--\s*_?class:\s*([^>]*?)\s*-->')
HEADING_PATTERN = re.compile(r'^(#{1,6})\s')
FENCE_PATTERN = re.compile(r'^(`{3,}|~{3,})')

# Marp themes are shared files, never inlined per deck; a `style:` front-matter
# key or an inline <style> block would fork the theme for one deck.
INLINE_STYLE_PATTERN = re.compile(r'<style\b', re.IGNORECASE)


def deck_slides(path: Path) -> list[str]:
    '''Split a deck source into slides, dropping the front matter.'''
    text = path.read_text(encoding='utf-8')
    match = FRONT_MATTER_PATTERN.match(text)
    return (text[match.end():] if match else text).split('\n---\n')


def slide_headings(slide: str) -> list[str]:
    '''Return the `#` runs of each heading in a slide, ignoring fenced code.'''
    headings = []
    fence = None
    for line in slide.split('\n'):
        opener = FENCE_PATTERN.match(line)
        if fence is not None:
            if opener and line.strip().startswith(fence):
                fence = None
            continue
        if opener:
            fence = opener.group(1)
            continue
        heading = HEADING_PATTERN.match(line)
        if heading:
            headings.append(heading.group(1))
    return headings


DECKS = sorted(TEACHING_ROOT.rglob('slides.md'))
DECK_IDS = [str(p.parent.relative_to(TEACHING_ROOT)) for p in DECKS]


def test_decks_were_discovered() -> None:
    '''Sanity check: fail loudly if the glob stops finding deck sources.'''
    assert DECKS, f'No teaching/**/slides.md files found under {TEACHING_ROOT}'


@pytest.mark.parametrize('deck', DECKS, ids=DECK_IDS)
def test_slide_titles_are_h1(deck: Path) -> None:
    '''
    A slide's title must be an `h1`, so it renders in the theme's title bar.
    A slide may carry further `h2` subheads, but never open with one.
    '''
    offenders = [
        index for index, slide in enumerate(deck_slides(deck), start=1)
        if (headings := slide_headings(slide)) and headings[0] != '#'
    ]
    assert not offenders, (
        f'{deck.parent.relative_to(TEACHING_ROOT)}: slide(s) {offenders} open with a '
        f'heading below `#`, so their title renders as inline body text instead of in '
        f'the theme title bar.'
    )


@pytest.mark.parametrize('deck', DECKS, ids=DECK_IDS)
def test_only_one_h1_per_slide(deck: Path) -> None:
    '''One title per slide: a second `h1` would be drawn over the first.'''
    offenders = [
        index for index, slide in enumerate(deck_slides(deck), start=1)
        if slide_headings(slide).count('#') > 1
    ]
    assert not offenders, (
        f'{deck.parent.relative_to(TEACHING_ROOT)}: slide(s) {offenders} carry more than '
        f'one `#` heading; the theme positions `h1` absolutely, so they would overlap.'
    )


@pytest.mark.parametrize('deck', DECKS, ids=DECK_IDS)
def test_exactly_one_lead_slide(deck: Path) -> None:
    '''Each deck opens with exactly one `lead` title slide, as the reference deck does.'''
    slides = deck_slides(deck)
    leads = [
        index for index, slide in enumerate(slides, start=1)
        if any('lead' in match.split() for match in CLASS_DIRECTIVE_PATTERN.findall(slide))
    ]
    assert len(leads) == 1, (
        f'{deck.parent.relative_to(TEACHING_ROOT)}: expected exactly one '
        f'`<!-- _class: lead -->` title slide, found {len(leads)} (slides {leads}).'
    )


@pytest.mark.parametrize('deck', DECKS, ids=DECK_IDS)
def test_only_theme_defined_classes_are_used(deck: Path) -> None:
    '''A deck may only name section classes the shared theme actually defines.'''
    used = {
        name
        for slide in deck_slides(deck)
        for match in CLASS_DIRECTIVE_PATTERN.findall(slide)
        for name in match.split()
    }
    unknown = sorted(used - THEME_CLASSES)
    assert not unknown, (
        f'{deck.parent.relative_to(TEACHING_ROOT)} uses section class(es) '
        f'{", ".join(unknown)}, which assets/marp/theme.css does not define, so they '
        f'would have no effect.'
    )


@pytest.mark.parametrize('deck', DECKS, ids=DECK_IDS)
def test_no_per_deck_styling(deck: Path) -> None:
    '''
    Styling lives in the one shared theme. An inline `<style>` block or a
    `style:` front-matter directive forks the theme for a single deck, which is
    exactly what collapsing 65 copies of the CSS into assets/marp/theme.css
    removed.
    '''
    text = deck.read_text(encoding='utf-8')
    assert not INLINE_STYLE_PATTERN.search(text), (
        f'{deck.parent.relative_to(TEACHING_ROOT)} contains an inline <style> block; '
        f'styling belongs in assets/marp/theme.css.'
    )
    match = FRONT_MATTER_PATTERN.match(text)
    front_matter = match.group(0) if match else ''
    assert not re.search(r'(?m)^style:', front_matter), (
        f'{deck.parent.relative_to(TEACHING_ROOT)} sets a `style:` front-matter '
        f'directive; styling belongs in assets/marp/theme.css.'
    )
