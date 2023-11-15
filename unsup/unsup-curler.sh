#!/usr/bin/env bash

set -e

cd "$(realpath "$(dirname "$0")")"

unsup_ver=0.2.3
unsup_url="https://git.sleeping.town/attachments/7edb17a2-e43f-4789-8bae-6140cbe98311"

mkdir -p .cache

read -p "Modloader: " modloader

read -p "Minecraft Version: " mc_version

mkdir unsup-$modloader-$mc_version
cd unsup-$modloader-$mc_version

packwiz init --name "Multiplicative Unsup $modloader $mc_version" --author MenacingPerson --mc-version $mc_version \
--version 1.0.0 --modloader $modloader --$modloader-version $(jq -r ".modloaders.$modloader.version" < ../../conf/base_config.json)

if [[ ! -f ../.cache/unsup-$unsup_ver.jar ]]
then
    curl "$unsup_url" --output ../.cache/unsup-$unsup_ver.jar
fi

cp ../.cache/unsup-$unsup_ver.jar unsup.jar

cp ../unsup.ini .

sed -i "s|!!mcver!!|$modloader/$mc_version|g" unsup.ini

packwiz refresh

packwiz mr export -o ../../packs/Multiplicative-$modloader-$mc_version-unsup-$unsup_ver.mrpack
