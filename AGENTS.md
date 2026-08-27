# AGENTS.md

Rules for AI agents working in this repository. The umbrella file at
`../AGENTS.md` (Montana Tech coursework) applies too; where the two conflict,
this file wins. `CONTRIBUTING.md` is the how-to; this file is the what-not-to-do.

## Whose content this is

This is Dr. Jacob L. Pach's site. The slide decks are his lectures, converted
from his PowerPoint files. The job is a faithful reproduction, not an edit.

- Do not reword, reorder, add, or delete his content. Not a typo, not a
  mistranslation, not a duplicated slide, not an empty paragraph. If something
  in a deck is wrong, it goes in a comment to him on the pull request, not into
  the markdown.
- Repairing a conversion artifact is allowed and expected: a title split
  across two shapes, a label that PowerPoint z-ordered below the block it
  introduces, an unclosed code fence, an HTML entity left unescaped inside
  code, non-breaking spaces inside a makefile recipe. The test is whether the
  words he wrote come out identical; the word multiset of the deck must not
  change.
- Polish text in a deck is his. Report it with a translation; leave it in place.
- Presenter notes are HTML comments. Keep them; students never see them.
- Slides hidden in PowerPoint (`<p:sld show="0">`) are not published; the
  converter skips them. A deck that shows a private checklist or a draft slide
  is a deck that still has one, not a reason to translate it.
- Any comment posted to Dr. Pach on GitHub says that an AI agent wrote it, at
  the top, and is signed the way the pull-request body is signed.

## The source of truth for a deck

The `.pptx` files are the ground truth. They are not in git: `robert.7z` at the
repository root holds all 65 (gitignored, along with anything it is extracted
to). When checking a deck's fidelity, compare against the PowerPoint, not
against an earlier markdown revision. LibreOffice renders a `.pptx` to PDF
without a display:

```sh
docker run --rm -v "$PWD:/data" --entrypoint soffice lscr.io/linuxserver/libreoffice:latest \
  --headless --convert-to pdf --outdir /data/out /data/deck.pptx
```

## The theme is the contract

`assets/marp/theme.css` is the one theme, and
`teaching/csci-232/lectures/lecture01-intro/` is the one deck Dr. Pach built
with it by hand. A converted deck is right when it looks like that deck.

- Every slide's title is an `h1`. The theme's `h1` is the title bar.
- Only the classes the theme defines may be used (`lead`, `caption-slide`,
  `code-description`, `small-code`, `tiny-code`, `long-title`). No inline
  `<style>`, no per-deck CSS, no `style:` front matter.
- A styling problem that shows up across decks is fixed once, in the theme or
  in `tools/pptx2marp.py`, never by hand in sixty files.
- `tests/content/test_deck_styling.py` enforces this. If it fails, the deck is
  wrong, not the test.

## What to run before a pull request

```sh
python3 -m pytest tests/unit --cov && python3 -m pytest tests/content
python3 -m pylint tools tests && python3 -m pyright tools tests
npm run lint:md && npm run lint:css && npm run lint:toml && yamllint .
pip-audit -r tests/requirements.txt --strict
trivy fs --scanners vuln,secret,misconfig --severity HIGH,CRITICAL --exit-code 1 .
```

The security scans are a gate, not a report: a HIGH or CRITICAL finding blocks
the push until it is fixed (upgrade the package, pin a fixed base image), never
ignored.

`tests/content` has known failures that report real upstream defects (see
`tests/README.md`); a change must not add to them. A change to a deck's
markdown is not done until the deck has been rendered
(`docker compose run --rm marp`) and looked at in a browser: 41 percent of
converted slides overflowed the slide box before anyone measured, because
PowerPoint shrinks text to fit and Marp does not. `tests/e2e` drives a real
browser; use it, or a Selenium script, to measure rather than assume.

## Git

- Branch from `main`, open a pull request, never push to `main`. Do not merge
  your own pull request.
- Stage files by name. `git status` before committing a deck: the rendered
  `index.html` sits next to `slides.md` and is not gitignored.
- Commit generated output never; commit `slides.md` and its `assets/`.
- No emoji anywhere in the repository. No lint suppressions; if a rule is wrong
  for a whole file type, change the configuration file and say why.

## Subagents

Split work by course, not by task. Give every agent the same brief, name the
reference deck, and require it to verify content fidelity mechanically (word
multiset plus an ordered diff against the previous commit) before it reports.
An agent that edits sixty decks under a wrong instruction is a bigger repair
than the one it was fixing; when two agents disagree about a rule, stop and
settle it against the theme and the reference deck before either continues.
