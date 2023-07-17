#!/usr/bin/env bash

set -e

cd "$(realpath "$(dirname "$0")"/..)"

rm -f ./packs/*.mrpack

for i in 1.19.4
do
    if [[ -d ./conf/$i ]]
    then
        script -eq -c "./setup.py $i" /dev/null
    fi
done
