#!/bin/bash
# Builds the AJP/partner-facing page: redacted PRD, separate password, served at /ajp/.
# Run:  ./build-ajp.sh   then commit & push docs/ to publish.
set -euo pipefail
cd "$(dirname "$0")"
APP=../civic-action-toolbox-app
mkdir -p build/ajp docs/ajp

python3 scripts/make_ajp_prd.py "$APP/PRD.md" build/ajp-prd.md
pandoc -f gfm -t html5 build/ajp-prd.md -o build/ajp-fragment.html
{ cat template/head-ajp.html
  cat build/ajp-fragment.html
} | sed "s/BUILD_DATE/$(date '+%B %e, %Y')/" > build/ajp/index.html
cat template/foot-ajp.html | sed "s/BUILD_DATE/$(date '+%B %e, %Y')/" >> build/ajp/index.html

PASSWORD=$(cat .password-ajp)
npx --yes staticrypt build/ajp/index.html -d docs/ajp \
  --password "$PASSWORD" \
  --remember 30 \
  --template-title "Toolbox Partner Overview" \
  --template-instructions "Enter the password Planet Detroit shared with you." \
  --template-color-primary "#1B2FC4" \
  --template-color-secondary "#FFF3DC" \
  --template-button "Unlock"

echo "Encrypted AJP page written to docs/ajp/index.html"
