#!/bin/sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
IMAGE=${1:-sift:dev}
CONTEXT=${2:-$ROOT}
CONTEXT=$(CDPATH= cd -- "$CONTEXT" && pwd)

# Resolve from the checkout, independently of the Docker context so the
# context can omit .git while the image still records its source revision.
if [ -n "${BUILD_COMMIT:-}" ]; then
  COMMIT=$BUILD_COMMIT
else
  COMMIT=$(git -C "$ROOT" rev-parse --short=12 HEAD 2>/dev/null || printf 'unknown')
fi

exec docker build \
  --build-arg "BUILD_COMMIT=$COMMIT" \
  --label "org.opencontainers.image.revision=$COMMIT" \
  -t "$IMAGE" \
  -f "$CONTEXT/Dockerfile" \
  "$CONTEXT"
