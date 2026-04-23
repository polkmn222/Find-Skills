#!/usr/bin/env sh
set -eu

ROOT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)

cd "$ROOT_DIR"

echo "==> Checking scoring cases"
./scripts/check-scoring-cases.py

echo "==> Checking host skill sync"
./scripts/check-skill-sync.sh

echo "All maintainer checks passed."
