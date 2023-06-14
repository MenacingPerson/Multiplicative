#!/usr/bin/bash

set -e

cd $(realpath $(dirname "$0"))

modpack_name=$(jq -r '.pack_name' < config.json)
modpack_vers=$(jq -r '.pack_version' < config.json)

git add .
git commit -m "Release $modpack_vers" --allow-empty

./setup.py 1.19.4
./setup.py 1.20

git tag "$modpack_vers"
git push origin main "$modpack_vers"
