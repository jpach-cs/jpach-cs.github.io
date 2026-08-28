'''
Layer 1 content check: lecture decks must be branded for the course they live
under, and must not ship placeholder outlines.

Both checks read the deck's `slides.md` source: the footer directive names the
course on every slide, and the first slide is the title slide, so the first
course code the source mentions is the course the deck presents itself as.

The course-code check is scoped to *lecture* decks only. Labs and assignments
(e.g. the Git and command-line labs) are reused verbatim across courses and
keep their original "CSCI 112" branding by design -- that is shared
boilerplate, not a mislabel. Lecture decks are expected to be course-specific,
which is why a mismatch there is a real defect.
'''

from __future__ import annotations

import re
from pathlib import Path

import pytest

from course_codes import course_code_from_path, first_course_code_in_text
from repo import TEACHING_ROOT

# A line consisting of only "??" (optionally surrounded by whitespace). Scoped
# to a whole line so we do not false-positive on legitimate uses of "??" inside
# a sentence, e.g. "?? -- Untracked file (not added to Git yet)" in the Git lab.
PLACEHOLDER_LINE = re.compile(r'(?m)^\s*\?\?\s*$')


def discover_lecture_decks() -> list[Path]:
    '''Return every lecture deck source under the teaching tree, sorted for stable test IDs.'''
    return sorted(TEACHING_ROOT.glob('*/lectures/*/slides.md'))


LECTURE_DECKS = discover_lecture_decks()
DECK_IDS = [str(p.relative_to(TEACHING_ROOT)) for p in LECTURE_DECKS]


def test_lecture_decks_were_discovered() -> None:
    '''Sanity check: fail loudly if the glob above stops finding anything.'''
    assert LECTURE_DECKS, f'No lecture decks found under {TEACHING_ROOT}'


@pytest.mark.parametrize('deck_path', LECTURE_DECKS, ids=DECK_IDS)
def test_deck_is_branded_for_its_own_course(deck_path: Path) -> None:
    '''The first course code a lecture deck names must be the course it lives under.'''
    expected = course_code_from_path(deck_path, TEACHING_ROOT)
    actual = first_course_code_in_text(deck_path.read_text(encoding='utf-8'))
    assert actual == expected, (
        f'{deck_path.relative_to(TEACHING_ROOT)} is branded "{actual}" '
        f'but lives under the "{expected}" course directory.'
    )


@pytest.mark.parametrize('deck_path', LECTURE_DECKS, ids=DECK_IDS)
def test_deck_has_no_placeholder_outline(deck_path: Path) -> None:
    '''A lecture deck's outline must be real content, not a "??" placeholder.'''
    match = PLACEHOLDER_LINE.search(deck_path.read_text(encoding='utf-8'))
    assert match is None, (
        f'{deck_path.relative_to(TEACHING_ROOT)} contains a placeholder "??" line '
        f'where real slide content should be.'
    )
