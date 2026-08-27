#!/bin/sh
# Renders every Marp deck under teaching/ in place: each deck's markdown
# source lives at teaching/<course path>/slides.md, next to an optional
# assets/ subfolder, and this script renders index.html and index.pdf into
# that same directory, using the single shared theme at assets/marp/theme.css.
#
# The source filename is slides.md, not index.md: Jekyll turns any markdown
# file with front matter into a page, so a source named index.md would
# collide with the Marp-rendered index.html at the same URL.
#
# Requires marp-cli's Chromium build for PDF export, so this only runs inside
# the marpteam/marp-cli image (see the "marp-render" stage in Dockerfile, and
# the "marp" service in docker-compose.yml for local authoring).
#
# Usage: render-decks.sh
set -e

SRC_ROOT="teaching"
THEME="assets/marp/theme.css"

if [ ! -d "$SRC_ROOT" ]; then
  echo "No $SRC_ROOT/ directory found, nothing to render."
  exit 0
fi

find "$SRC_ROOT" -type f -name 'slides.md' | while IFS= read -r src; do
  deck_dir=$(dirname "$src")

  # Called directly (bypassing the image's docker-entrypoint, which drops to
  # the unprivileged "marp" user via gosu) so file ownership always matches
  # whatever user is running this script - root during the Dockerfile build,
  # or the bind-mounted host user under `docker compose run marp`.
  echo "Rendering $src -> $deck_dir"
  node /home/marp/.cli/marp-cli.js --theme-set "$THEME" --html "$src" -o "$deck_dir/index.html" < /dev/null
  node /home/marp/.cli/marp-cli.js --theme-set "$THEME" --pdf --allow-local-files "$src" -o "$deck_dir/index.pdf" < /dev/null
done
