#!/usr/bin/env bash

set -e

cd "$(realpath "$(dirname "$0")"/..)"

./scripts/runscript.sh
./scripts/gen_mod_list.sh > mod-list.md

if [[ $- == *i* ]] && command -v prismlauncher > /dev/null
then
    cd ./packs/
    prismlauncher --import *
fi
