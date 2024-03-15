#!/usr/bin/env fish

cd (realpath (dirname (status -f))/..)

if [ "$argv" = "" ]
    echo "Needs args. Ex: 1.20.2"
    exit 1
end

git stash

for i in $argv
    cd ./conf/"$i"
    packwiz update --all --yes
    git restore mods_neoforge
    packwiz refresh
    git add .
    cd ../..
end

git status
git commit -m "Update fabric mods"

for i in $argv
    cd ./conf/"$i"
    sed 's/fabric/neoforge/g' pack.toml -i
    packwiz update --all --yes
    cp (git status | grep modified: | grep ' mods/' | awk '{print $2}') mods_neoforge
    git restore mods pack.toml
    packwiz refresh
    git add .
    cd ../..
end

git status

./scripts/runscript.sh
git add .
git commit --am -m "Update mods"

git stash pop
