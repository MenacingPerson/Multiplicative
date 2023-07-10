#!/usr/bin/bash

set -e

cd "$(realpath "$(dirname "$0")"/..)"

modpack_vers=$(jq -r '.pack_version' < ./conf/base_config.json)

./scripts/test_commit.sh

git add .
git commit -m "Release $modpack_vers" --allow-empty

git tag "$modpack_vers"
git push origin main "$modpack_vers"
