#!/usr/bin/bash

set -e

cd $(realpath $(dirname "$0")/..)

modpack_name=$(jq -r '.pack_name' < ./conf/base_config.json)
modpack_vers=$(jq -r '.pack_version' < ./conf/base_config.json)

git add .
git commit -m "Release $modpack_vers" --allow-empty

./scripts/runscript.sh

git tag "$modpack_vers"
git push origin main "$modpack_vers"
