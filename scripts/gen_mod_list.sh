#!/usr/bin/env bash

set -e

cd "$(realpath "$(dirname "$0")"/..)"

echo "# Mod list for $(jq -r '.pack_name' < conf/base_config.json)"
echo "(excluding all Additive mods)"

for i in $(jq -r '.build[].mc' < conf/base_config.json)
do
    if [[ -d conf/$i ]]
    then
        echo -e "\n# Version $i:"

        echo -e "\n## Mods\n"
        echo -e "\n### All:\n"
        ls "conf/$i/mods" | sed 's/.pw.toml//g; s/^/- /'
        echo -e "\n### Fabric:\n"
        ls "conf/$i/mods_fabric" | sed 's/.pw.toml//g; s/^/- /'
        echo -e "\n### Quilt:\n"
        ls "conf/$i/mods_quilt" | sed 's/.pw.toml//g; s/^/- /'

        echo -e "\n## Resource packs:\n"
        ls conf/$i/resourcepacks | sed 's/.pw.toml//g; s/^/- /'

        echo -e "\n## Removed from Additive\n"
        echo -e "\n### All:"
        jq -r '.mods_removed[]' < conf/$i/config.json | sed 's/^/- /'
        echo -e "\n### Fabric:\n"
        jq -r '.mods_removed_fabric[]' < conf/$i/config.json | sed 's/^/- /'
        echo -e "\n### Quilt:\n"
        jq -r '.mods_removed_quilt[]' < conf/$i/config.json | sed 's/^/- /'
    fi
done
