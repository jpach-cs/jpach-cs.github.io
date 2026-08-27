#!/bin/sh
# Renders every Marp deck under decks/ into matching HTML and PDF under the
# given output root (teaching/ by default), using the single shared theme at
# assets/marp/theme.css.
#
# Deck source is decks/<course path>/index.md, mirroring the layout of the
# existing teaching/ output tree and the index.md + assets/ convention used
# by tools/pptx2marp.py, so its output can be dropped straight into decks/.
#
# Requires marp-cli's Chromium build for PDF export, so this only runs inside
# the marpteam/marp-cli image (see the "marp-render" stage in Dockerfile, and
# the "marp" service in docker-compose.yml for local authoring).
#
# Usage: render-decks.sh [output-root]   (default: teaching)
set -e

SRC_ROOT="decks"
OUT_ROOT="${1:-teaching}"
THEME="assets/marp/theme.css"

mkdir -p "$OUT_ROOT"

if [ ! -d "$SRC_ROOT" ]; then
  echo "No $SRC_ROOT/ directory found, nothing to render."
  exit 0
fi

find "$SRC_ROOT" -type f -name 'index.md' | while IFS= read -r src; do
  deck_dir=$(dirname "$src")
  rel=${deck_dir#"$SRC_ROOT"/}
  out_dir="$OUT_ROOT/$rel"
  mkdir -p "$out_dir"

  # Deck-specific files authored alongside index.md (images, an assets/
  # subfolder, etc.) - everything except the markdown source itself.
  find "$deck_dir" -mindepth 1 ! -name 'index.md' -exec sh -c '
    dest="$1/${2#"$3"/}"
    if [ -d "$2" ]; then mkdir -p "$dest"; else cp "$2" "$dest"; fi
  ' _ "$out_dir" {} "$deck_dir" \;

  # Called directly (bypassing the image's docker-entrypoint, which drops to
  # the unprivileged "marp" user via gosu) so file ownership always matches
  # whatever user is running this script - root during the Dockerfile build,
  # or the bind-mounted host user under `docker compose run marp`.
  echo "Rendering $src -> $out_dir"
  node /home/marp/.cli/marp-cli.js --theme-set "$THEME" --html "$src" -o "$out_dir/index.html" < /dev/null
  node /home/marp/.cli/marp-cli.js --theme-set "$THEME" --pdf --allow-local-files "$src" -o "$out_dir/index.pdf" < /dev/null
done
