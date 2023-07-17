#!/usr/bin/env bash

set -e

cd "$(realpath "$(dirname "$0")"/..)"

echo "# Mod list for Multiplicative"
echo "(excluding all Additive mods)"

for i in $(jq -r '.build[]' < conf/base_config.json)
do
    if [[ -d conf/$i ]]
    then
        echo -e "\n## Version $i:"
        echo -e "\n### Mods:\n"
        (ls conf/$i/mods; ls conf/$i/mods_fabric; ls conf/$i/mods_quilt) | \
            sed 's/.pw.toml//g; s/^/- /'
        echo -e "\n### Resource packs:\n"
        ls conf/$i/resourcepacks | sed 's/.pw.toml//g; s/^/- /'
        echo -e "\n### Removed from Additive:\n"
        jq -r '.mods_removed[]' < conf/$i/config.json | sed 's/^/- /'
        echo -e "\n### Removed from Additive (fabric):\n"
        jq -r '.mods_removed_fabric[]' < conf/$i/config.json | sed 's/^/- /'
        echo -e "\n### Removed from Additive (quilt):\n"
        jq -r '.mods_removed_quilt[]' < conf/$i/config.json | sed 's/^/- /'
    fi
done
