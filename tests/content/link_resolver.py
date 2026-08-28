'''
Resolves a `{{ '/some/path' | relative_url }}` link found in a Jekyll page back
to the source-tree file it is supposed to point at.

This works purely against the *source* tree (no `jekyll build` required),
which is what keeps Layer 1 fast and Docker-free. It understands the three
link shapes actually used in this repo's `teaching/**/index.md` files:

  1. A directory link ending in "/", e.g. "/teaching/csci-232/lectures/lecture02/"
     -> resolves if that directory contains an index.html or index.md.
  2. A direct file link with an extension, e.g.
     "/teaching/csci-232/lectures/lecture02/index.pdf"
     -> resolves if that exact file exists.
  3. An extensionless page link, e.g. "/teaching/csci-232/syllabus"
     -> resolves if "<path>.md" exists as a source file (Jekyll pages are
     written as .md and rendered to .html with no front-matter permalink
     override in this repo).
'''

from __future__ import annotations

from pathlib import Path


def resolve_link(link: str, repo_root: Path) -> Path | None:
    '''Return the source file a link resolves to, or None if it does not resolve.'''
    relative = link.strip('/')

    if link.endswith('/') or link == '/':
        base = (repo_root / relative) if relative else repo_root
        for candidate in (base / 'index.html', base / 'index.md'):
            if candidate.is_file():
                return candidate
        return None

    direct = repo_root / relative
    if direct.is_file():
        return direct

    md_candidate = repo_root / f'{relative}.md'
    if md_candidate.is_file():
        return md_candidate

    return None
