# Contributing

This site is built with Jekyll. Slide decks (lectures, labs, assignments) are
authored in [Marp](https://marp.app/) markdown and rendered to HTML and PDF at
build time - the markdown is the source of truth, not the rendered files.

## Authoring a slide deck

1. Create `teaching/<path>/slides.md`, right next to where the deck is
   served. For example, the source for `teaching/csci-232/lectures/lecture03/`
   lives at `teaching/csci-232/lectures/lecture03/slides.md`.

   The source file is named `slides.md`, not `index.md`: Marp front matter
   and Jekyll front matter are both YAML between `---` fences, so a
   `marp: true` file named `index.md` would also look like a valid Jekyll
   page. Jekyll would try to render it with the site's default layout,
   producing a second, wrong page at the same URL as the real deck (the
   Marp-rendered `index.html`). `_config.yml`'s `exclude:` also excludes
   `teaching/**/slides.md` from the Jekyll build as a second line of
   defense.
2. Give it Marp front matter and use the shared theme:

   ```markdown
   ---
   marp: true
   theme: pach
   paginate: true
   footer: "CSCI 232 | Algorithms & Data Structures | J. L. Pach"
   ---

   # Lecture 3

   Slide content here.
   ```

3. Put any images the deck uses next to `slides.md`, in an `assets/`
   subfolder, and reference them with a relative path, e.g.
   `![diagram](assets/diagram.png)`.
4. Render it:

   ```sh
   docker compose run --rm marp
   ```

   This renders every deck at `teaching/**/slides.md` into `index.html` and
   `index.pdf` in the same directory as its source, using the shared theme,
   and writes them straight onto your working tree (no container-only output
   to dig out).
5. Add the deck to `_data/decks.yml` so its course page links to it - see
   "The deck catalog" below.
6. Commit `teaching/<path>/slides.md` and its `assets/` folder. Do **not**
   commit the generated `teaching/<path>/index.html` or `index.pdf` - see
   "Generated output and committed legacy content" below.
7. Preview the whole site the normal way:

   ```sh
   WEB_PORT=8083 docker compose up --build web
   ```

   (Port 8080/8081 may already be in use locally; 8083 is free.)

## The deck catalog

`_data/decks.yml` names every deck the site publishes. The four course pages
render their lists from it through `_includes/deck-lists.html`, so a deck's
name, its position in the course, and the formats it is offered in are
written down once instead of once per page.

Each entry looks like this:

```yaml
- dir: lecture05
  label: Lecture 05
  title: Unit Testing with Unity, and Forking on GitHub
  source: slides
```

- `dir` is the directory under `teaching/<course>/<section>/`.
- `label` is the short position name, and must agree with `dir`: a deck in
  `lecture05/` is labelled `Lecture 05`. A suffixed directory such as
  `lecture01-intro/` sits outside the numbered run and takes a descriptive
  label instead.
- `title` says what the deck actually covers, read off the deck itself. It is
  descriptive, not aspirational - where a deck's content disagrees with the
  course it sits under, the index shows that rather than hiding it.
- `source` is `slides` for a deck rendered from `slides.md` (linked as HTML,
  PDF and Markdown) or `legacy` for one that only has committed output
  (linked as HTML and PDF).

`tests/content/test_deck_catalog.py` holds the catalog and the directories on
disk to each other: an unlisted deck directory, a listed deck with no
directory, a label that disagrees with its directory, or a `source` that
disagrees with the directory's contents all fail. Before this catalog existed
the course pages hand-listed Lectures 01-15 and Labs 01-15 for every course
whether or not those decks had been written, which is where the site's few
hundred dead links came from.

## The shared theme

`assets/marp/theme.css` is the single copy of Dr. Pach's Marp theme. It used
to be copied into every deck's markdown front matter by hand (as a `style:`
block) and then got embedded again by marp-cli into the rendered HTML -
duplicated across every deck, with no way to tell whether two copies had
drifted apart. That's how a CSCI 112 deck ended up published as CSCI 232's
lecture 2.

Reference it from a deck's front matter with `theme: pach`, not by pasting
CSS. If the look needs to change, edit `assets/marp/theme.css` once.

`theme.css` also carries every image it uses - the Montana Tech logo, the
bullet icon, and the title-slide MT icon (the theme's CSS custom properties
`--logo-main`, `--bullet-icon`, `--mt-icon` point at them), plus the three
per-language badges shown on Python, x86 assembly, and C code blocks -
embedded directly as base64 `data:image/svg+xml;base64,...` URIs rather than
as `url('logo.svg')`-style paths to sibling files. That's a deliberate
choice, not an oversight: a deck's rendered `index.html` can live anywhere
under `teaching/`, and PDF export has Chromium load that HTML from a local
file with no server root to resolve a path against, so any `url()` pointing
at a separate asset file would need that file copied alongside every single
rendered deck to resolve correctly in both HTML and PDF output. Embedding the
assets as data URIs sidesteps that path-resolution problem entirely - the
theme is fully self-contained, `tools/render-decks.sh` has nothing asset-related
to copy, and there's exactly one authored copy of each image, living only in
`theme.css`.

## What the theme expects of a deck

The theme assigns meanings to the markup, so a deck has to use the right
element for the right job. `tests/content/test_deck_styling.py` enforces all
of this.

**`h1` is the slide title.** `theme.css` positions `h1` absolutely in a title
bar at the top of the slide, in `--color-primary`, with the accent rule drawn
by `h1::before`. `h2` is an inline subheading *within* the slide body. So each
slide opens with a single `#`, and uses `##` only for subheads under it. Dr.
Pach's hand-authored deck at `teaching/csci-232/lectures/lecture01-intro/`
uses `<h1>` on all 25 of its slides and `<h2>` only for subheads; that deck is
the reference every other deck is matched against.

This is worth stating plainly because it was got wrong at scale: the decks
converted from PowerPoint originally emitted `##` for every slide title, so
not one converted slide rendered in the title bar. 2,433 titles were promoted
in one pass, and `tools/pptx2marp.py` now emits `#` for a slide title.

**Section classes.** The theme defines exactly these, and a deck may not name
any other (a class the theme has no rule for silently does nothing):

| Class | Use |
| --- | --- |
| `lead` | The deck's title slide. Recentres the title and sizes the `h2` subtitle. Exactly one per deck. |
| `caption-slide` | A divider slide: white title on a filled background. Used for the closing "Thank You" slide. |
| `long-title` | A slide whose title is a whole caption sentence. Steps the type down and lets the title bar grow. |
| `code-description` | Two-column layout, code on the left and prose on the right. |
| `small-code`, `tiny-code` | Reduce `--code-base-size` on a slide with a large code block. |

Apply one with a per-slide directive:

```markdown
<!-- _class: lead -->

# CSCI 232

## Algorithms & Data Structures
```

**Nothing else styles a deck.** No inline `<style>` block, no `style:`
front-matter directive, no per-deck CSS file. If the look needs to change,
`assets/marp/theme.css` changes once.

## Generated output and committed legacy content

Every deck directory under `teaching/` is in exactly one of two states:

- **Source (current)**: `slides.md` + an `assets/` folder. `index.html` and
  `index.pdf` next to them are Marp build output - regenerate them with
  `docker compose run --rm marp`, don't hand-edit them, and don't commit
  them. `teaching/**/*.pdf` is gitignored for this reason; `index.html` isn't
  (`.gitignore` can't express "ignore this file only in directories that
  also have a `slides.md`"), so nothing stops `git add` from picking one up
  by accident - check `git status` before committing a deck.
- **Committed legacy (no source yet)**: just `index.html` and `index.pdf`,
  with no `slides.md`. The markdown source for these was never written -
  only the rendered output exists. These 15 directories are still in this
  state:

  - `csci-112/assignments/ass01`
  - `csci-112/laboratories/lab01`
  - `csci-112/laboratories/lab02`
  - `csci-112/lectures/lecture01-intro`
  - `csci-232/lectures/lecture01-intro`
  - `csci-232/lectures/lecture02`
  - `csci-446/assignments/ass01`
  - `csci-446/laboratories/lab01`
  - `csci-446/laboratories/lab02`
  - `csci-446/lectures/lecture01-intro`
  - `csci-446/lectures/lecture02`
  - `esof-322/assignments/ass01`
  - `esof-322/laboratories/lab01`
  - `esof-322/laboratories/lab02`
  - `esof-322/lectures/lecture01-intro`

  Migrating one of these means reconstructing its markdown from the rendered
  output (lossy - speaker intent, incremental builds, and any authoring
  shortcuts are gone), not a mechanical move. Until someone does that for a
  given directory, leave its `index.html`/`index.pdf` alone and committed.

  This repository is `jpach-cs.github.io` - native GitHub Pages runs Jekyll
  only and does not run this repo's Dockerfile or Marp, so it can't render a
  `slides.md` on its own. That's what the `deploy` job in
  `.github/workflows/ci.yml` is for: on push to `main` it builds the same
  Dockerfile used locally (Marp render, then Jekyll) and publishes the
  result via GitHub Actions, so `index.html`/`index.pdf` for a source-backed
  deck never need to be committed to be live. That job only takes effect
  once the repository's Pages source is set to "GitHub Actions" (Settings >
  Pages > Build and deployment); until then, native Pages keeps publishing
  from `main` directly and won't render a deck that only has `slides.md`.

## Local development

- `docker compose up --build` serves the full site (`WEB_PORT` defaults to
  8080; override if that's taken, e.g. `WEB_PORT=8083`).
- `docker compose run --rm marp` renders decks only, straight onto the host
  filesystem, without building Jekyll or nginx - the fast loop while writing
  slides.
- Both use the same `Dockerfile`; `marp` targets its `marp-render` stage
  directly instead of building the whole image.

## Linting

Every file type in the repo has a linter, and CI (`.github/workflows/ci.yml`) runs all
of them. Run the same commands locally before opening a pull request:

| Files | Tool | Command |
| --- | --- | --- |
| `tools/*.py`, `tests/**/*.py` | pylint, pyright | `python3 -m pylint tools tests`, `python3 -m pyright tools tests` |
| `tests/unit` | pytest with a 95% branch-coverage gate | `python3 -m pytest tests/unit --cov` |
| `*.yml`, `*.yaml` | yamllint | `yamllint .` |
| `tools/*.sh` | shellcheck | `shellcheck tools/*.sh` |
| `.github/workflows/*.yml` | actionlint | `actionlint` |
| `Dockerfile` | hadolint | `hadolint Dockerfile` |
| `pyproject.toml` | taplo | `npm run lint:toml` |
| `assets/**/*.css` | stylelint | `npm run lint:css` |
| `**/*.md` | markdownlint | `npm run lint:md` |
| `**/*.svg` | xmllint (well-formedness) | `xmllint --noout $(find . -name '*.svg')` |
| `Gemfile` | ruby syntax check | `ruby -c Gemfile` |

Python tools come from `tests/requirements.txt`; node tools from `package.json`
(`npm ci`). Every version is pinned in those two files. Linter configuration lives in
`.pylintrc`, `pyproject.toml`, `.yamllint`, `.markdownlint.yaml`, and `.stylelintrc.json`;
the only rule relaxed anywhere is the line length, set to 120 to match the repo
convention.

Do not add per-line lint suppressions. If a linter is wrong for a whole file type,
change the configuration file and say why in the pull request.
