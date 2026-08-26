#!/bin/bash
# Rebuilds the password-protected docs site from the app repo's PRD.md + ROADMAP.md.
# Run:  ./build.sh        then commit & push the site/ folder to publish.
# The password lives in .password (never committed). Plaintext HTML stays in build/ (never committed).
set -euo pipefail
cd "$(dirname "$0")"

APP=../civic-action-toolbox-app
mkdir -p build site

pandoc -f gfm -t html5 "$APP/PRD.md" -o build/prd-fragment.html
pandoc -f gfm -t html5 "$APP/ROADMAP.md" -o build/roadmap-fragment.html

cat template/head.html build/prd-fragment.html template/mid.html build/roadmap-fragment.html template/foot.html \
  | sed "s/BUILD_DATE/$(date '+%B %e, %Y')/" > build/index.html

PASSWORD=$(cat .password)
npx --yes staticrypt build/index.html -d site \
  --password "$PASSWORD" \
  --remember 30 \
  --template-title "Toolbox Product Docs" \
  --template-instructions "Planet Detroit internal. Enter the shared password to unlock the PRD and roadmap." \
  --template-color-primary "#1B2FC4" \
  --template-color-secondary "#FFF3DC" \
  --template-button "Unlock"

echo "Encrypted site written to site/index.html"
