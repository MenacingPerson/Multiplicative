#!/usr/bin/env bash

set -e

cd "$(realpath "$(dirname "$0")"/..)"

echo "# Mod list for Multiplicative"

for i in $(jq -r '.build[]' < conf/base_config.json)
do
    if [[ -d conf/$i ]]
    then
        echo -e "\n## Version $i:\n(excludes all Additive mods)"
        echo -e "\n### Mods:"
        (ls conf/$i/mods; ls conf/$i/mods_fabric; ls conf/$i/mods_quilt) | \
            sed 's/.pw.toml//g; s/^/- /'
        echo -e "\n ### Resource packs:"
        ls conf/$i/resourcepacks | sed 's/.pw.toml//g; s/^/- /'
    fi
done
