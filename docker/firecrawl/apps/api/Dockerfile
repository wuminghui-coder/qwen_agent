FROM node:20-slim AS base
ENV PNPM_HOME="/pnpm"
ENV PATH="$PNPM_HOME:$PATH"
LABEL fly_launch_runtime="Node.js"
RUN corepack enable
COPY . /app
WORKDIR /app

FROM base AS prod-deps
RUN --mount=type=cache,id=pnpm,target=/pnpm/store pnpm install --prod --frozen-lockfile

FROM base AS build
RUN --mount=type=cache,id=pnpm,target=/pnpm/store pnpm install --frozen-lockfile

RUN apt-get update -qq && apt-get install -y ca-certificates && update-ca-certificates
RUN pnpm install
RUN --mount=type=secret,id=SENTRY_AUTH_TOKEN \
    bash -c 'export SENTRY_AUTH_TOKEN="$(cat /run/secrets/SENTRY_AUTH_TOKEN)"; if [ -z $SENTRY_AUTH_TOKEN ]; then pnpm run build:nosentry; else pnpm run build; fi'

# Install Go
FROM golang:1.19 AS go-base
COPY sharedLibs/go-html-to-md /app/sharedLibs/go-html-to-md

# Install Go dependencies and build parser lib
RUN cd /app/sharedLibs/go-html-to-md && \
    go mod tidy && \
    go build -o html-to-markdown.so -buildmode=c-shared html-to-markdown.go && \
    chmod +x html-to-markdown.so

FROM base
COPY --from=prod-deps /app/node_modules /app/node_modules
COPY --from=build /app /app
COPY --from=go-base /app/sharedLibs/go-html-to-md/html-to-markdown.so /app/sharedLibs/go-html-to-md/html-to-markdown.so

# Start the server by default, this can be overwritten at runtime
EXPOSE 8080
ENV PUPPETEER_EXECUTABLE_PATH="/usr/bin/chromium"

# Make sure the entrypoint script has the correct line endings
RUN sed -i 's/\r$//' /app/docker-entrypoint.sh

ENTRYPOINT "/app/docker-entrypoint.sh"