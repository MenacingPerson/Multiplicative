#!/usr/bin/env bash

set -e

cd "$(realpath "$(dirname "$0")")"

unsup_ver=0.2.3
unsup_url="https://git.sleeping.town/attachments/7edb17a2-e43f-4789-8bae-6140cbe98311"

mkdir -p .cache

for ver in $@
do
    cd $ver

    if [[ ! -f ../.cache/unsup-$unsup_ver.jar ]]
    then
        curl "$unsup_url" --output ../.cache/unsup-$unsup_ver.jar
    fi

    cp ../.cache/unsup-$unsup_ver.jar unsup.jar
    packwiz refresh
    packwiz mr export -o ../../packs/Multiplicative-$ver-unsup-$unsup_ver.mrpack
    rm unsup.jar
    packwiz refresh

    cd ..
done
