#!/usr/bin/env bash

set -e

cd "$(realpath "$(dirname "$0")"/..)"

./scripts/runscript.sh

if command -v prismlauncher > /dev/null
then
    cd ./packs/
    prismlauncher --import *
fi
