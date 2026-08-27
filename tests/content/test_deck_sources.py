'''
Layer 1 content check: every deck source under `teaching/**/slides.md` is a
valid, self-contained Marp deck, and no deck directory is left in an
ambiguous state between authored source and committed legacy output.

A deck directory is in exactly one of two states (see "Generated output and
committed legacy content" in CONTRIBUTING.md): committed legacy `index.html`/
`index.pdf` with no source, or a `slides.md` source (plus an `assets/` folder)
with `index.html`/`index.pdf` as untracked build output. This file only
checks the second state - `slides.md` sources - since legacy directories have
nothing generated here to validate.
'''

from __future__ import annotations

import re
from pathlib import Path

import pytest

from repo import GIT_AVAILABLE, REPO_ROOT, TEACHING_ROOT, tracked_files

# Matches the leading '---\n ... \n---\n' YAML front matter block a Marp deck
# opens with, capturing everything between the fences.
FRONT_MATTER_PATTERN = re.compile(r'\A---\r?\n(.*?\r?\n)---\r?\n', re.DOTALL)

# Matches a Marp-specific "marp: true" line inside that front matter block.
MARP_TRUE_PATTERN = re.compile(r'^marp:\s*true\s*$', re.MULTILINE)

# Matches the "assets/<path>" portion of any "(assets/<path>)" markdown link
# target, e.g. the image target in "![alt](assets/image2.png)". The match
# starts at the opening paren, so multi-line alt text ahead of it (common in
# decks converted from PowerPoint) does not confuse it.
ASSET_REFERENCE_PATTERN = re.compile(r'\(assets/([^)\s]+)\)')


def discover_deck_sources() -> list[Path]:
    '''Return every Marp deck source under teaching/, sorted for stable test IDs.'''
    return sorted(TEACHING_ROOT.rglob('slides.md'))


DECK_SOURCES = discover_deck_sources()
DECK_SOURCE_IDS = [str(p.relative_to(TEACHING_ROOT)) for p in DECK_SOURCES]


def test_deck_sources_were_discovered() -> None:
    '''Sanity check: fail loudly if the glob above stops finding anything.'''
    assert DECK_SOURCES, f'No teaching/**/slides.md files found under {TEACHING_ROOT}'


@pytest.mark.parametrize('slides_path', DECK_SOURCES, ids=DECK_SOURCE_IDS)
def test_slides_have_marp_front_matter(slides_path: Path) -> None:
    '''Every deck source must open with Marp front matter declaring `marp: true`.'''
    text = slides_path.read_text(encoding='utf-8')
    match = FRONT_MATTER_PATTERN.match(text)
    assert match, (
        f"{slides_path.relative_to(TEACHING_ROOT)} does not start with a '---' "
        f'front matter block, so Marp will not treat it as a deck.'
    )
    assert MARP_TRUE_PATTERN.search(match.group(1)), (
        f"{slides_path.relative_to(TEACHING_ROOT)} front matter does not set "
        f"'marp: true'."
    )


@pytest.mark.parametrize('slides_path', DECK_SOURCES, ids=DECK_SOURCE_IDS)
def test_referenced_assets_exist(slides_path: Path) -> None:
    '''Every `assets/...` image a deck references must exist next to its source.'''
    text = slides_path.read_text(encoding='utf-8')
    missing = sorted({
        rel for rel in ASSET_REFERENCE_PATTERN.findall(text)
        if not (slides_path.parent / 'assets' / rel).is_file()
    })
    assert not missing, (
        f'{slides_path.relative_to(TEACHING_ROOT)} references missing asset(s): '
        f'{", ".join(missing)}'
    )


@pytest.mark.parametrize('slides_path', DECK_SOURCES, ids=DECK_SOURCE_IDS)
def test_every_asset_is_referenced(slides_path: Path) -> None:
    '''
    Every file in a deck's `assets/` folder is used by the deck. An unreferenced
    asset is usually an image from a slide that was hidden in PowerPoint (and so
    is not published) or from a slide that was later removed; it is dead weight
    in the repository and in the built site.
    '''
    assets_dir = slides_path.parent / 'assets'
    if not assets_dir.is_dir():
        return
    referenced = set(ASSET_REFERENCE_PATTERN.findall(slides_path.read_text(encoding='utf-8')))
    unused = sorted(path.name for path in assets_dir.iterdir() if path.name not in referenced)
    assert not unused, (
        f'{slides_path.relative_to(TEACHING_ROOT)} has asset(s) no slide uses: {", ".join(unused)}'
    )


@pytest.mark.skipif(not GIT_AVAILABLE, reason='git is not installed')
@pytest.mark.parametrize('slides_path', DECK_SOURCES, ids=DECK_SOURCE_IDS)
def test_no_committed_index_html_alongside_source(slides_path: Path) -> None:
    '''A deck directory must not carry both a slides.md source and a committed index.html.'''
    index_html = slides_path.parent / 'index.html'
    relative = index_html.relative_to(REPO_ROOT).as_posix()
    assert relative not in tracked_files(), (
        f'{relative} is committed to git alongside '
        f'{slides_path.relative_to(TEACHING_ROOT)}. index.html is Marp build '
        f'output and must not be committed once a slides.md source exists for '
        f'the same deck - see "Generated output and committed legacy content" '
        f'in CONTRIBUTING.md.'
    )
