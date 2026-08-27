# Jacob L. Pach Teaching Site

Course pages and slide decks for Dr. Jacob L. Pach's classes at Montana
Technological University, published with GitHub Pages at
<https://jpach-cs.github.io>.

The site is a Jekyll site. Slide decks are written in [Marp](https://marp.app/)
markdown and rendered to HTML and PDF at build time; the markdown is the only
thing committed. Course pages list their decks from one catalog file, so a deck
appears on its course page as soon as it is catalogued.

## Quick start

Requirements: Docker Desktop (or Docker Engine with the compose plugin). Nothing
else is installed on the host.

```sh
git clone https://github.com/jpach-cs/jpach-cs.github.io.git
cd jpach-cs.github.io
docker compose up --build
```

Open <http://localhost:8080>. The build renders every deck under `teaching/`,
builds the Jekyll site, and serves it with nginx. If port 8080 is taken:

```sh
WEB_PORT=8083 docker compose up --build
```

To render the decks alone, straight onto your working tree, while writing
slides:

```sh
docker compose run --rm marp
```

This writes `index.html` and `index.pdf` next to each `teaching/**/slides.md`.
Do not commit them: the PDF is gitignored, the HTML is not (see
"Generated output and committed legacy content" in `CONTRIBUTING.md`), so
check `git status` before staging a deck.

## Where things are

| Path | What it is |
| --- | --- |
| `index.md`, `teaching/`, `portfolio/`, `downloads/` | Site content, rendered by Jekyll |
| `teaching/<course>/index.md` | A course page; deck lists come from `_data/decks.yml` |
| `teaching/<course>/<section>/<deck>/slides.md` | A deck's Marp source, with any images in `assets/` beside it |
| `_data/decks.yml` | The deck catalog: one entry per deck with its label and title |
| `_includes/deck-lists.html` | Renders the catalog onto a course page |
| `assets/marp/theme.css` | The single shared Marp theme (`pach`) |
| `tools/pptx2marp.py` | Converts a PowerPoint `.pptx` to Marp markdown, standard library only |
| `tools/render-decks.sh` | Renders every deck; run inside the marp-cli image by `docker compose` |
| `tests/` | Unit, content-integrity, and end-to-end suites; see `tests/README.md` |
| `.github/workflows/ci.yml` | Lint, test, build, and deploy to GitHub Pages |

## Adding or changing a deck

1. Write `teaching/<course>/<section>/<deck>/slides.md` with the `pach` theme.
2. Add the deck to `_data/decks.yml` so its course page links to it.
3. Render it with `docker compose run --rm marp` and check it in the browser.
4. Run the tests and linters below, then open a pull request.

`CONTRIBUTING.md` covers the details: the theme's rules for titles and slide
classes, the catalog format, and what the converter does and does not repair.

### Converting a PowerPoint deck

```sh
python3 tools/pptx2marp.py path/to/deck.pptx --out teaching/csci-232/lectures/lecture21 \
  --theme pach --footer "CSCI 232 | Algorithms & Data Structures | J. L. Pach"
```

The converter extracts text, code, tables, images, and speaker notes (as HTML
comments), skips slides hidden in PowerPoint, and publishes a text box that
contains equations as PowerPoint's own rendering of it. Read the result:
PowerPoint carries no notion of "this text box is code" or "this shape is a
section divider", so some slides need a hand pass. `CONTRIBUTING.md` lists the
artifact classes that have come up and how each was handled.

## Tests and linters

```sh
pip install -r tests/requirements.txt
npm ci

python3 -m pytest tests/unit --cov        # converter unit tests, 95% branch-coverage gate
python3 -m pytest tests/content           # every deck, catalog entry, link, and PDF in the tree
python3 -m pylint tools tests
python3 -m pyright tools tests
npm run lint:md && npm run lint:css && npm run lint:toml
yamllint .
pip-audit -r tests/requirements.txt --strict         # known CVEs in the Python tooling
trivy fs --scanners vuln,secret,misconfig --severity HIGH,CRITICAL --exit-code 1 .
trivy image --severity HIGH,CRITICAL --exit-code 1 --ignore-unfixed jpach-csgithubio-web
```

The end-to-end suite drives a real browser against the running site:

```sh
WEB_PORT=8082 docker compose up --build -d --wait
docker compose -f tests/e2e/docker-compose.selenium.yml up -d --wait
python3 -m pytest tests/e2e
docker compose -f tests/e2e/docker-compose.selenium.yml down
```

Some content checks are red on purpose: they assert there are no broken
links, mis-branded decks, or corrupt PDFs, and the tree still has a few. The
CI jobs for those checks are `continue-on-error` until the content is fixed.
`tests/README.md` lists every check and what it finds today.

## Deployment

Pushes to `main` build the site in CI and deploy it with the GitHub Pages
Actions deployment. The repository's Pages source must be set to "GitHub
Actions" (Settings, Pages, Source) for that deployment to be served.
