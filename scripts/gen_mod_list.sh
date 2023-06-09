#!/usr/bin/env bash

set -e

cd "$(realpath "$(dirname "$0")"/..)"

cd conf

echo "# Mod list for Multiplicative"

for i in *
do
    if [[ -d $i ]]
    then
        echo -e "\n## Version $i:\n(excludes all Additive mods)\n"
        (ls $i/mods; ls $i/mods_fabric; ls $i/mods_quilt) | sed 's/.pw.toml//g; s/^/- /'
    fi
done
