#!/bin/bash
# Builds the partner page: redacted PRD + redacted roadmap, own password, served at /partner/.
set -euo pipefail
cd "$(dirname "$0")"
APP=../civic-action-toolbox-app
mkdir -p build/partner docs/partner

python3 scripts/make_partner_prd.py "$APP/PRD.md" build/partner-prd.md
python3 scripts/make_partner_roadmap.py "$APP/ROADMAP.md" build/partner-roadmap.md
pandoc -f gfm -t html5 build/partner-prd.md -o build/partner-prd-fragment.html
pandoc -f gfm -t html5 build/partner-roadmap.md -o build/partner-roadmap-fragment.html
cat template/head-partner.html build/partner-prd-fragment.html template/mid-partner.html build/partner-roadmap-fragment.html template/foot-partner.html \
  | sed "s/BUILD_DATE/$(date '+%B %e, %Y')/" > build/partner/index.html

PASSWORD=$(cat .password-partner)
npx --yes staticrypt build/partner/index.html -d docs/partner \
  --password "$PASSWORD" \
  --remember 30 \
  --template-title "Toolbox Partner Overview" \
  --template-instructions "Enter the password Planet Detroit shared with you." \
  --template-color-primary "#1B2FC4" \
  --template-color-secondary "#FFF3DC" \
  --template-button "Unlock"

echo "Encrypted partner page written to docs/partner/index.html"
