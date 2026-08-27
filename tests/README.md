# Tests

Three independent layers. Layer 0 unit-tests the converter in `tools/` against
synthetic decks built in memory. Layer 1 is pure file inspection against the
working tree -- no Docker, no running site, no network. Layer 2 drives a real
browser against the running site over the remote WebDriver protocol.

All three run in `.github/workflows/ci.yml`, along with pylint, pyright, and
yamllint. Layer 0 carries a 95% branch-coverage gate (`pyproject.toml`).

Both layers report real defects that exist in this repo today. That is by
design, not a bug in the tests -- see "Expected failures" below before
assuming something is broken. In particular, checks (d) and (i) below assert
there are zero broken links and are currently **red**, on purpose, until the
underlying content is filled in -- see "Broken links are asserted, not
allowlisted" further down.

```text
tests/
  README.md
  requirements.txt          pip deps for all layers (pytest, pytest-cov, pylint, pyright, selenium, requests)
  unit/                     Layer 0 -- unit tests for tools/pptx2marp.py
    conftest.py             puts tools/ on sys.path
    pptx_builder.py         assembles minimal .pptx archives from hand-written OOXML
    test_pptx2marp.py       one test per code path in the converter
  content/                  Layer 1 -- content integrity, no Docker
    repo.py                 finds the repo root, no hardcoded paths
    course_codes.py         "csci-232" <-> "CSCI 232" normalization
    pdf_text.py             pdftotext wrapper, skips gracefully if missing
    link_resolver.py        resolves a Jekyll relative_url link to a source file
    test_pdf_integrity.py       (a) every PDF is a real PDF
    test_deck_branding.py       (b) lecture decks branded for their own course
                                 (c) no "??" placeholder outlines
    test_markdown_branding.py   bonus: syllabus.md/schedule.md branding (see below)
    test_index_links.py         (d) every index.md local link resolves
    test_deck_sources.py        (j) every teaching/**/slides.md is valid Marp source
                                 (k) every asset a slides.md references exists
                                 (l) no directory has both slides.md and a committed index.html
  e2e/                      Layer 2 -- Selenium against the running site
    conftest.py             base_url / browser_base_url / driver / visit fixtures
    crawler.py              same-origin link+image crawler (requests-based)
    soft_404.py             "does this 200 page actually say not-found" heuristic
    docker-compose.selenium.yml   selenium/standalone-chrome, nothing else
    test_home_and_nav.py        (e) home page loads, title, nav links work
    test_course_pages.py        (f) 4 course pages return 200 + render heading
    test_syllabus_schedule.py   (g) syllabus/schedule pages render
    test_soft_404.py            (h) no page is a soft 404
    test_link_crawler.py        (i) every <a href>/<img src> resolves
```

## Layer 0: unit tests (tools/)

```bash
pip install -r tests/requirements.txt
python3 -m pytest tests/unit --cov            # fails below 95% branch coverage
python3 -m pylint tools tests/unit            # must be 10.00/10
python3 -m pyright tools tests/unit           # must report 0 errors
```

No fixture binaries: `pptx_builder.py` zips hand-written OOXML parts into a
`.pptx` in memory, so each test states exactly which slide structure it is
exercising (grouped shapes, SmartArt, linked images, malformed rels, ...).

## Layer 1: content integrity (fast, no Docker)

Pure Python plus one external binary (`pdftotext`, from poppler-utils) for the
checks that need to read PDF text. Nothing here touches the network or Docker.
This is the fastest feedback loop and should run on every commit.

### Run it

```bash
pip install -r tests/requirements.txt   # just pytest; everything else is stdlib
python3 -m pytest tests/content -v
```

No `cd` required and no absolute paths anywhere -- `tests/content/repo.py`
finds the repo root by walking up from itself looking for `_config.yml`, so
this works from any checkout location, including a CI runner's workspace.

`pdftotext` is a system package, not a pip package:

```bash
# Debian/Ubuntu (GitHub Actions ubuntu-latest runners):
sudo apt-get update && sudo apt-get install -y poppler-utils

# macOS:
brew install poppler
```

If it is not installed, `test_deck_branding.py`'s two tests are **skipped**
(not failed, not erroring) with a message saying so. `test_pdf_integrity.py`
and `test_index_links.py` do not need it at all.

### What each check does, and what it finds today

| Check | File | Finds today |
| --- | --- | --- |
| (a) Every PDF is really a PDF (magic bytes `%PDF-` + minimum size) | `test_pdf_integrity.py` | See below |
| (b) Lecture decks are branded for their own course | `test_deck_branding.py` | See below |
| (c) No placeholder "??" outline | `test_deck_branding.py` | See below |
| (d) Every local link in `teaching/**/index.md` resolves | `test_index_links.py` | **Fails** -- see below |
| (j) Every `teaching/**/slides.md` opens with `marp: true` front matter | `test_deck_sources.py` | Passes |
| (k) Every `assets/...` a `slides.md` references exists | `test_deck_sources.py` | Passes |
| (l) No directory has both a `slides.md` source and a committed `index.html` | `test_deck_sources.py` | Passes |
| bonus: syllabus/schedule markdown branding | `test_markdown_branding.py` | See below |

Detail on each row above, keyed by check letter:

* **(a)** `teaching/csci-232/assignments/ass01/index.pdf` is 6 bytes (a UTF-16LE
  BOM + CRLF), not a PDF at all.
* **(b)** `teaching/csci-232/lectures/lecture02/index.pdf` and
  `teaching/csci-446/lectures/lecture02/index.pdf` both say "CSCI 112 /
  Programming with C".
* **(c)** The same two lecture02 decks have an "OUTLINE:" section that is
  literally "??".
* **(d)** 213 broken links today (missing Lecture/Lab 03-15 content across all
  four courses) -- see "Broken links are asserted, not allowlisted" below.
* **bonus** `csci-446/schedule.md` and `esof-322/schedule.md` both read
  "Course Schedule — CSCI 232" (copy-pasted, never updated); `esof-322/
  syllabus.md`'s back-link points at `/teaching/csci-446/`.

The course-code check in (b) is scoped to **lecture decks only**
(`teaching/*/lectures/*/index.pdf`), not labs or assignments. The Git,
debugging, and command-line labs are intentionally reused verbatim across all
four courses and keep their original "CSCI 112" branding by design -- that is
shared boilerplate, not a mislabel. Lecture decks are expected to be
course-specific, which is why a mismatch there is a real defect and a mismatch
in a shared lab is not.

`test_markdown_branding.py` was not in the original spec for this suite. It
exists because the same class of bug (copy-paste branding mismatch) showed up
in markdown pages while exploring the site for the E2E layer, and it is exactly
as cheap to catch with a regex over a markdown heading as it is over PDF text.
It is kept in its own file so it is clear it is additional coverage.

### Broken links are asserted, not allowlisted (check d)

The course index pages (`teaching/*/index.md`) advertise Lectures 01-15 and
Labs 01-15 for every course. Only a couple of each actually exist per course
today, so `test_index_links.py` fails on ~213 broken links.

This suite deliberately does not carry a "known broken links" allowlist for
this. An allowlist would make the suite green today, but only by hiding the
very thing it exists to report, and it needs constant upkeep (every new
broken link has to be added, every fixed one has to be removed) that silently
rots the moment someone forgets a step. `test_index_links.py` instead asserts
there are zero broken links, full stop, and fails loudly -- with every broken
link listed, grouped by source page -- until the content is actually filled
in. The failure message is the report; there is no separate tool to run.

## Layer 2: end to end (Selenium against the running site)

Needs two things running first. Neither is started by the test suite itself.

**1. The site**, already built and running per the task this suite was built
for:

```bash
WEB_PORT=8082 docker compose up -d --build
```

**2. A disposable Selenium Grid**, using the official image so nothing browser-
or driver-related needs installing on the host:

```bash
docker compose -f tests/e2e/docker-compose.selenium.yml up -d
```

Then run the suite:

```bash
pip install -r tests/requirements.txt
E2E_BASE_URL=http://localhost:8082 python3 -m pytest tests/e2e -v
```

Tear down the Selenium container when done (the site's own container is not
this suite's to manage):

```bash
docker compose -f tests/e2e/docker-compose.selenium.yml down
```

### Environment variables

| Variable | Default | Meaning |
| --- | --- | --- |
| `E2E_BASE_URL` | `http://localhost:8082` | Where pytest (on the host) reaches the site, for plain HTTP checks |
| `E2E_BROWSER_BASE_URL` | derived from `E2E_BASE_URL` | Where the *browser* reaches the site -- see below |
| `SELENIUM_REMOTE_URL` | `http://localhost:4444/wd/hub` | The Selenium Grid's WebDriver endpoint |

`E2E_BROWSER_BASE_URL` almost never needs setting by hand. The selenium
container cannot reach the site via `localhost` (inside that container,
`localhost` means the container itself), so if `E2E_BASE_URL` is a
`localhost`/`127.0.0.1` URL, `tests/e2e/conftest.py` automatically rewrites the
browser's copy to use `host.docker.internal` instead, which
`docker-compose.selenium.yml` maps to the real host via
`extra_hosts: host.docker.internal:host-gateway` (works on Docker Desktop out
of the box, and on Linux/GitHub Actions runners with Docker Engine 20.10+).
If `E2E_BASE_URL` is already a routable, non-localhost address (e.g. a real
CI hostname), no rewriting happens and both variables are the same.

### Why some checks use `requests` instead of pure Selenium

The WebDriver protocol does not expose the HTTP status code of a navigation
(that needs Chrome DevTools Protocol network-log wiring, which is fragile
across Chrome/driver versions). This site is static, server-rendered HTML with
no client-side routing, so there is nothing lost by using a plain HTTP client
for status-code-only assertions ("does this return 200") and reserving the
real browser for what it is actually for: rendering pages and driving clicks.
See the module docstring in `tests/e2e/crawler.py` for the full reasoning.
Every test still documents which tool it uses and why.

### What each check does, and what it finds today (end-to-end layer)

| Check | File | Result today |
| --- | --- | --- |
| (e) Home page loads, non-empty title, nav links work | `test_home_and_nav.py` | **Fails** -- see below |
| (f) 4 course pages return 200 and render their heading | `test_course_pages.py` | Passes |
| (g) Syllabus/schedule pages render | `test_syllabus_schedule.py` | Schedule **fails** -- see below |
| (h) No page returns a soft 404 | `test_soft_404.py` | Passes |
| (i) Every `<a href>`/`<img src>` resolves | `test_link_crawler.py` | **Fails** -- see below |

Detail on each row above, keyed by check letter:

* **(e)** the home page's "Research" link (`/research/`) 404s -- there is no
  research page.
* **(g)** Syllabus: passes. **Schedule fails**: `csci-446/schedule.html` and
  `esof-322/schedule.html` both render the heading "Course Schedule — CSCI
  232".
* **(i)** ~250 broken same-origin links/images -- see "Broken links are
  asserted, not allowlisted" below.

Two of these are left failing **on purpose**. They are one-off, already-live
content bugs (a dead nav link, a copy-pasted heading), the same species of
defect Layer 1's branding checks are designed to surface loudly rather than
paper over. Silencing them with an allowlist would defeat the point of having
them. If you fix the underlying content, the tests will go green on their own
with no test changes needed.

### Broken links are asserted, not allowlisted (check i)

Crawling the live site from `/` and `/teaching/` finds ~250 broken same-origin
links/images, the large majority of which are the exact same missing
lecture/lab content Layer 1 finds in the source tree (Lectures/Labs 03-15).
As with Layer 1's `test_index_links.py`, this suite does not allowlist that
away: `test_link_crawler.py` asserts there are zero broken same-origin
links/images and fails with every broken link listed -- grouped by the page
that links to it -- until the underlying content is fixed. There is no
separate report script; the test failure output is the report.

A handful of the broken links are HTML-layer-only defects Layer 1 cannot see
from the source tree alone (Layer 1 checks whether files exist; these are
about how Jekyll's actual URLs differ from what the pages link to):

* Every course's "Syllabus"/"Schedule" nav link points at an extensionless
  URL (e.g. `/teaching/csci-232/syllabus`), but Jekyll renders `syllabus.md`
  at `syllabus.html` with no permalink override, so all 8 of those links 404.
  (`test_syllabus_schedule.py` hits the real `.html` URLs directly, which is
  why it can still confirm the *content* renders correctly even though the
  site's own nav can't reach it.)
* `/teaching/csci-232/assignments/ass01/` returns **403**, not 404: that
  directory has no `index.html` (unlike the other three courses' `ass01/`,
  which have both an HTML and a PDF version), and directory listing is off.

## Running everything in CI

Neither layer needs any interactive step or a host-specific absolute path.
A GitHub Actions job could look like:

```yaml
name: tests
on: [push, pull_request]
jobs:
  content-integrity:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: '3.12' }
      - run: sudo apt-get update && sudo apt-get install -y poppler-utils
      - run: pip install -r tests/requirements.txt
      - run: python3 -m pytest tests/content -v

  end-to-end:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: '3.12' }
      - run: pip install -r tests/requirements.txt
      - run: docker compose up -d --build
      - run: docker compose -f tests/e2e/docker-compose.selenium.yml up -d --wait
      - run: E2E_BASE_URL=http://localhost:8080 python3 -m pytest tests/e2e -v
      - if: always()
        run: |
          docker compose -f tests/e2e/docker-compose.selenium.yml down
          docker compose down
```

(Port 8080 above matches this repo's `docker-compose.yml` default; adjust if
`WEB_PORT` is overridden.)
