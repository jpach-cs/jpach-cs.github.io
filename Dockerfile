# Stage 1: Build Markdown to HTML with Jekyll (mirrors GitHub Pages)
FROM ruby:3.2-alpine AS builder

RUN apk add --no-cache build-base git

# jekyll-github-metadata needs the repository name. It normally reads this from
# the origin remote, but .git is not copied into the image, so pass it explicitly.
ARG PAGES_REPO_NWO=jpach-cs/jpach-cs.github.io
ENV PAGES_REPO_NWO=${PAGES_REPO_NWO}

WORKDIR /site
COPY Gemfile ./
RUN bundle install

COPY . .
RUN bundle exec jekyll build --destination /site/_site

# Stage 2: Serve with nginx
FROM nginx:alpine

RUN rm -rf /usr/share/nginx/html/*
COPY --from=builder /site/_site /usr/share/nginx/html/

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
