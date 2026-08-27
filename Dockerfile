# Stage 1: Render Marp slide decks (markdown source at teaching/**/slides.md)
# to HTML and PDF, in place next to their source. Uses the official marp-cli
# image because it bundles the Chromium build that PDF export needs - do not
# replace this with a bare `npm install @marp-team/marp-cli`, which does not
# ship a browser.
FROM marpteam/marp-cli:v4.5.0 AS marp-render

WORKDIR /home/marp/app
COPY . .
# Runs as root, the image's default user for this build-only stage. The
# script calls marp-cli's own entry point directly rather than going through
# docker-entrypoint, which would drop to the unprivileged "marp" user via
# gosu and fail to write into this root-owned output directory.
RUN ./tools/render-decks.sh

# Stage 2: Build Markdown to HTML with Jekyll (mirrors GitHub Pages)
FROM ruby:3.2-alpine AS builder

# Pinned to the packages in alpine 3.23 (the base of ruby:3.2-alpine); bump together.
RUN apk add --no-cache build-base=0.5-r3 git=2.52.0-r0

# jekyll-github-metadata needs the repository name. It normally reads this from
# the origin remote, but .git is not copied into the image, so pass it explicitly.
ARG PAGES_REPO_NWO=jpach-cs/jpach-cs.github.io
ENV PAGES_REPO_NWO=${PAGES_REPO_NWO}

WORKDIR /site
COPY Gemfile ./
RUN bundle install

COPY . .
# Freshly rendered decks overlay the committed teaching/ tree, so a deck that
# has been migrated to teaching/<path>/slides.md always wins over any stale
# rendered artifact still checked in at the same path.
COPY --from=marp-render /home/marp/app/teaching/ /site/teaching/
# Jekyll excludes slides.md (it would otherwise render each deck's markdown as
# a page), so copy every deck's markdown source into the output verbatim after
# the build: each deck is published as index.html, index.pdf, and slides.md.
RUN bundle exec jekyll build --destination /site/_site \
    && find teaching -name slides.md -exec sh -c \
        'mkdir -p "/site/_site/$(dirname "$1")" && cp "$1" "/site/_site/$1"' _ {} \;

# Stage 3: Serve with nginx
FROM nginx:alpine

RUN rm -rf /usr/share/nginx/html/*
COPY --from=builder /site/_site /usr/share/nginx/html/

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
