'''
Heuristic for detecting a "soft 404": a page that responds 200 OK but whose
body is actually a not-found message (something Jekyll can produce if a
layout falls back or a page is misconfigured, even though nginx itself would
give a real 404 for a missing file).

Scoped to phrases unlikely to appear in this site's real academic content
(course descriptions, syllabi, lecture material) so it does not false-positive.
'''

from __future__ import annotations

import re

SOFT_404_PATTERNS = [
    re.compile(r'page not found', re.IGNORECASE),
    re.compile(r'\b404\b.{0,30}not found', re.IGNORECASE | re.DOTALL),
    re.compile(r"the page you('re| are)? (looking|searching) for", re.IGNORECASE),
    re.compile(r"we can'?t seem to find", re.IGNORECASE),
]


def looks_like_soft_404(page_source: str) -> str | None:
    '''Return the matched phrase if `page_source` looks like a not-found page, else None.'''
    for pattern in SOFT_404_PATTERNS:
        match = pattern.search(page_source)
        if match:
            return match.group(0)
    return None
