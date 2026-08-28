'''
Every migrated deck is published in three formats side by side: rendered HTML,
PDF, and the Marp markdown source itself.
'''

from __future__ import annotations

import requests

DECK = '/teaching/csci-232/laboratories/lab03/'


def test_deck_is_served_as_html_pdf_and_markdown(base_url: str) -> None:
    '''
    index.html, index.pdf, and slides.md all return 200 for a migrated deck.
    '''
    for name in ('index.html', 'index.pdf', 'slides.md'):
        response = requests.get(f'{base_url}{DECK}{name}', timeout=30)
        assert response.status_code == 200, f'{name}: {response.status_code}'
    markdown = requests.get(f'{base_url}{DECK}slides.md', timeout=30).text
    assert markdown.startswith('---\nmarp: true')


def test_deck_markdown_is_not_rendered_as_a_jekyll_page(base_url: str) -> None:
    '''
    slides.html must not exist; only Marp renders the deck.
    '''
    assert requests.get(f'{base_url}{DECK}slides.html', timeout=30).status_code == 404
