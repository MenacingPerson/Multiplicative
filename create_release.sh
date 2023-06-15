#!/usr/bin/bash

set -e

cd $(realpath $(dirname "$0"))

modpack_name=$(jq -r '.pack_name' < ./conf/1.20/config.json)
modpack_vers=$(jq -r '.pack_version' < ./conf/1.20/config.json)

git add .
git commit -m "Release $modpack_vers" --allow-empty

./runscript.sh

git tag "$modpack_vers"
git push origin main "$modpack_vers"
