# Contributing

This site is built with Jekyll. Slide decks (lectures, labs, assignments) are
authored in [Marp](https://marp.app/) markdown and rendered to HTML and PDF at
build time - the markdown is the source of truth, not the rendered files.

## Authoring a slide deck

1. Create `decks/<same path as the deck lives under teaching/>/index.md`. For
   example, the source for `teaching/csci-232/lectures/lecture03/` lives at
   `decks/csci-232/lectures/lecture03/index.md`.
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

3. Put any images the deck uses next to `index.md` (or in an `assets/`
   subfolder beside it) and reference them with a relative path, e.g.
   `![diagram](assets/diagram.png)`. Everything in the deck's folder except
   `index.md` itself is copied over to the rendered output automatically.
4. Render it:

   ```sh
   docker compose run --rm marp
   ```

   This renders every deck under `decks/` into matching HTML and PDF under
   `teaching/`, using the shared theme, and writes them straight onto your
   working tree (no container-only output to dig out).
5. Commit `decks/<path>/index.md` and any images it needs. Do **not** commit
   the generated `teaching/<path>/index.html` for a migrated deck going
   forward, per "Generated output and .gitignore" below - the transition plan
   for the files that are *already* committed is still an open question (see
   that section).
6. Preview the whole site the normal way:

   ```sh
   WEB_PORT=8083 docker compose up --build web
   ```

   (Port 8080/8081 may already be in use locally; 8083 is free.)

There's a working example at `decks/pipeline-smoketest/index.md` if you want
to see a minimal deck end to end - it's a build smoke test, not real course
content, and can be deleted once you're comfortable with the workflow.

## Why `decks/` is separate from `teaching/`

`teaching/` is what Jekyll and GitHub Pages serve. `decks/` is Marp source
only and is excluded from the Jekyll build entirely (see `exclude:` in
`_config.yml`). Two reasons it isn't just `index.md` sitting directly in
`teaching/<path>/` next to the rendered output:

- Marp front matter and Jekyll front matter are both YAML between `---`
  fences. A `decks/.../index.md` with `marp: true` in it would also look like
  a valid Jekyll page if it sat inside `teaching/`, and Jekyll would try to
  render it with the site's default layout - producing a second, wrong page
  at the same URL as the real deck.
- It keeps authoring source from ever being one accidental Jekyll config
  change away from overwriting rendered output, in either direction.

The render stage writes generated HTML/PDF into `teaching/<same path>/`,
mirroring `decks/`, so URLs don't change.

## The shared theme

`assets/marp/theme.css` is the single copy of Dr. Pach's Marp theme. It used
to be copied into every deck's markdown front matter by hand (as a `style:`
block) and then got embedded again by marp-cli into the rendered HTML -
duplicated across every deck, with no way to tell whether two copies had
drifted apart. That's how a CSCI 112 deck ended up published as CSCI 232's
lecture 2.

Reference it from a deck's front matter with `theme: pach`, not by pasting
CSS. If the look needs to change, edit `assets/marp/theme.css` once.

`theme.css` also carries `assets/marp/logo.svg`, `mt.svg`, and `picax.svg` -
the logo, bullet icon, and Montana Tech icon the theme's CSS custom
properties (`--logo-main`, `--bullet-icon`, `--mt-icon`) point at. The theme
references them with plain relative `url('logo.svg')` paths rather than a
root-relative `/assets/marp/logo.svg` path. That's a deliberate choice, not
an oversight: those `url()` values get embedded into each deck's own
`index.html` and are resolved by the browser (or by Chromium during PDF
export) relative to *that page's own location*, not relative to
`theme.css`'s location - a root-relative path would work when the site is
served over HTTP but break for PDF export, since Chromium loads the page
from a local file and has no server root to resolve `/...` against. So the
render script (`tools/render-decks.sh`) copies the three shared asset
files into every deck's output directory alongside its `index.html`, sourced
from `assets/marp/` each time. There's exactly one authored copy of each
asset; the small binary copies in build output are disposable, unlike the
24KB of theme CSS this replaces.

## Generated output and `.gitignore`

Going forward, `teaching/**/*.pdf` is gitignored - PDFs are Marp render
output, not something to hand-edit or diff in review.

**This does not touch the roughly 18 PDFs already committed under
`teaching/`** (one per existing lecture, lab, and assignment deck). Ignoring
a pattern in Git has no effect on files that are already tracked; they stay
in the repository and `git status` will not flag them. What changes is that
*new* PDFs generated by the render pipeline won't accidentally get staged.

**Open question, not decided here:** should those ~18 already-committed
PDFs (and their `index.html` siblings) be migrated to `decks/*/index.md` and
untracked, or left as committed legacy content indefinitely? Two things make
this more than a cleanup task:

- The markdown source for those decks doesn't exist anywhere - only the
  rendered HTML/PDF do. Migrating a deck means reconstructing its markdown
  from the rendered output (lossy - speaker intent, incremental builds, and
  any authoring shortcuts are gone), not a mechanical move.
- This repository is `jpach-cs.github.io` - it deploys as a GitHub Pages
  site, and native GitHub Pages runs Jekyll only. It does not run this
  repo's Dockerfile or Marp. If a deck's `index.html`/`index.pdf` are ever
  removed from Git in favor of `decks/*/index.md` alone, the live site will
  have nothing to serve at that URL unless the render step also runs
  somewhere before deploy (a GitHub Actions workflow that commits or
  publishes the rendered output, or switching the deployed artifact to this
  Dockerfile's nginx stage instead of native Pages). That deploy question is
  out of scope here and belongs to whoever owns the migration.

Until that's decided, treat committed `index.html`/`index.pdf` under
`teaching/` as legacy and leave them alone; only add new decks through
`decks/`.

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
