#!/usr/bin/env bash

set -e

cd "$(realpath "$(dirname "$0")"/..)"

dump_toml() {
    cat $@ 2>/dev/null | (grep -iE '^name =' || echo '"(Nothing)"') | awk -F\" '{print $2}'
}

markdownify() {
    cat | sed 's/^/- /g'
}

get_json_or_nothing() {
    local x="$(cat | jq -r $1)"
    if [[ -z $x ]]
    then
        echo '(Nothing)'
        return
    fi
    echo "$x"
}


echo -e "# Mod list for $(jq -r '.pack_name' < conf/base_config.json)\n"
echo "(excluding all Additive mods)"

for i in $(jq -r '.build[].mc' < conf/base_config.json)
do
    if [[ -d conf/$i ]]
    then
        echo -e "\n\n# Version $i:"
        echo -e "\n## Mods"
        echo -e "\n### All:"
        dump_toml "conf/$i/mods/*" | markdownify
        echo -e "\n### Fabric:"
        dump_toml "conf/$i/mods_fabric/*" | markdownify
#        echo -e "\n### Quilt:"
#        dump_toml "conf/$i/mods_quilt/*" | markdownify
        echo -e "\n### Forge:"
        dump_toml "conf/$i/mods_forge/*" | markdownify

        echo -e "\n## Resource packs:"
        dump_toml "conf/$i/resourcepacks/*" | markdownify

        echo -e "\n## Removed from Additive"
        echo -e "\n### All:"
        get_json_or_nothing '.mods_removed[]' < conf/$i/config.json | markdownify
        echo -e "\n### Fabric:"
        get_json_or_nothing '.mods_removed_fabric[]' < conf/$i/config.json | markdownify
#        echo -e "\n### Quilt:"
#        get_json_or_nothing '.mods_removed_quilt[]' < conf/$i/config.json | markdownify
        echo -e "\n### Forge:"
        get_json_or_nothing '.mods_removed_forge[]' < conf/$i/config.json | markdownify
    fi
done
