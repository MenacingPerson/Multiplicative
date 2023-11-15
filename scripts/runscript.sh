#!/usr/bin/env bash

set -e

cd "$(realpath "$(dirname "$0")"/..)"

rm -f ./packs/*.mrpack
rm -rf ./unsup/versions
mkdir ./unsup/versions

for i in $(jq -r '.build[].mc' < conf/base_config.json)
do
    if [[ -d ./conf/$i ]]
    then
        script -eq -c "./setup.py $i" /dev/null
        cp ./Modified/versions ./unsup/ -r
    fi
done

./scripts/gen_mod_list.sh > ./mod-list.md

cp additive/LICENSE ./unsup/versions
