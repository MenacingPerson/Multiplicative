#!/usr/bin/env bash

set -e

cd "$(realpath "$(dirname "$0")"/..)"

cd conf

for i in *
do
    if [[ -d $i ]]
    then
        echo "# Version $i:"
        jq -r '.mods[][1]' < "$i/config.json" | sed 's/^/- /'
    fi
done
