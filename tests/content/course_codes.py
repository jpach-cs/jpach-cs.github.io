'''
Course code helpers shared by the branding-integrity tests.

A "course code" here is normalized to the form "CSCI 232" or "ESOF 322": the
subject letters, a single space, then the three-digit number. Content in the
repo spells this inconsistently ("CSCI-232", "csci232", "CSCI 232"), so every
comparison goes through `normalize_course_code` first.
'''

from __future__ import annotations

import re
from pathlib import Path

# Matches a course directory name like "csci-232" or "esof-322".
_DIR_PATTERN = re.compile(r'^(csci|esof)-(\d{3})$', re.IGNORECASE)

# Matches a course code appearing in free text: "CSCI 232", "CSCI-232", "CSCI232".
_TEXT_PATTERN = re.compile(r'(csci|esof)\s*-?\s*(\d{3})', re.IGNORECASE)


def normalize_course_code(subject: str, number: str) -> str:
    '''Return the canonical "SUBJECT NNN" spelling, e.g. "CSCI 232".'''
    return f'{subject.upper()} {number}'


def course_code_from_path(path: Path, teaching_root: Path) -> str:
    '''
    Derive the expected course code from a path's position under
    `teaching/<course-dir>/...`. Raises ValueError if the path is not under a
    recognized course directory.
    '''
    relative = path.resolve().relative_to(teaching_root.resolve())
    course_dir = relative.parts[0]
    match = _DIR_PATTERN.match(course_dir)
    if not match:
        raise ValueError(f'"{course_dir}" is not a recognized course directory name')
    return normalize_course_code(match.group(1), match.group(2))


def first_course_code_in_text(text: str) -> str | None:
    '''
    Return the first course code mentioned in `text`, normalized, or None if
    none is found. Used to read the branding printed on the first line/page of
    an extracted PDF deck.
    '''
    match = _TEXT_PATTERN.search(text)
    if not match:
        return None
    return normalize_course_code(match.group(1), match.group(2))
