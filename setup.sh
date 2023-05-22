#!/usr/bin/env bash

set -e

GREEN='\033[0;32m'
NC='\033[0m'

# cd to dir where this script is located
export ODIR=$(dirname $(realpath "$0"))
cd "${ODIR}"

export MODPACK_CONFIG="${ODIR}/config.json"

print() {
    echo -e "\n${GREEN}======>${NC} ${@}"
}

getconf() {
    jq -r ".${1}" < "${MODPACK_CONFIG}"
}

getconf_arr() {
    jq -r ".${1}[]" < "${MODPACK_CONFIG}"
}

# Reset to certain hash to avoid unwanted changes
(
    print "Updating Additive to specified hash"
    git submodule update --init
    cd Additive
    git pull origin main
    git reset --hard "$(getconf additive_hash)"
    git submodule update --init
)

# Recreate modified pack
rm -rf ./Modified ./packs
mkdir -p ./Modified ./packs
cp -r Additive/* ./Modified
cd ./Modified/versions

# Remove unwanted versions
for i in $(getconf_arr unwanted_mc_versions)
do
    if [[ -d "${i}" ]]
    then
        print "Removing pack version ${i}"
        rm -r "${i}"
    fi
done

run_in_fabric() {
    for pack_edition in fabric/*
    do
        (
            export pack_edition pack_ver="$(getconf pack_name)-$(getconf pack_version)-$(echo $pack_edition | sed 's|/|\+|g')"
            cd "${pack_edition}"
            ${@}
        )
    done
}

run_in_quilt() {
    for pack_edition in quilt/*
    do
        (
            export pack_edition pack_ver="$(getconf pack_name)-$(getconf pack_version)-$(echo $pack_edition | sed 's|/|\+|g')"
            cd "${pack_edition}"
            ${@}
        )
    done
}

run_in_all() {
    run_in_fabric ${@}
    run_in_quilt ${@}
}

add_mods_mr() {
    for mod in ${@}
    do
        mod=( $(echo $mod | tr "::" " ") )
        if [[ ${mod[1]} == "" ]]
        then
            print "Mod version not specified for mod ${mod}" >&2
            return 1
        fi
        print "Adding modrinth mod ${mod[0]} version ${mod[1]} to ${pack_edition}"
        packwiz mr add "${mod[0]}" --version-filename $mod[1]
    done
}

add_mods_cf() {
    for mod in ${@}
    do
        mod=( $(echo $mod | tr "::" " ") )
        if [[ ${mod[1]} == "" ]]
        then
            print "Mod version not specified for mod ${mod}" >&2
            return 1
        fi
        print "Adding curseforge mod ${mod[0]} version ${mod[1]} to ${pack_edition}"
        packwiz cf add --category mc-mods "${mod[0]}" --file-id "${mod[1]}"
    done
}

# Add fabric-only mods
run_in_fabric add_mods_mr $(getconf_arr mods_mr_fabric)
run_in_fabric add_mods_cf $(getconf_arr mods_cf_fabric)
# Add quilt-only mods
run_in_quilt add_mods_mr $(getconf_arr mods_mr_quilt)
run_in_quilt add_mods_cf $(getconf_arr mods_cf_quilt)
# Add mods
run_in_all add_mods_mr $(getconf_arr mods_mr)
run_in_all add_mods_cf $(getconf_arr mods_cf)

rm_mods() {
    for j in ${@}
    do
        print "Removing mod '$j' from version ${pack_edition}"
        packwiz remove "$j"
    done
}

# Remove unwanted mods
run_in_fabric rm_mods $(getconf_arr mods_removed_fabric)
run_in_quilt rm_mods $(getconf_arr mods_removed_quilt)
run_in_all rm_mods $(getconf_arr mods_removed)


modify_configs() {
    "${ODIR}"/scripts/modify-configs.py "${1}"
}

# Add optional mods
run_in_fabric modify_configs mods_optional_fabric
run_in_quilt modify_configs mods_optional_quilt
run_in_all modify_configs mods_optional

# Copy config file over
run_in_all cp -r "$ODIR/config/" ./

fix_pack_version() {
    sed -i "s|$(getconf pack_name) ver|$(getconf pack_name) $(getconf pack_version)|g" ./config/isxander-main-menu-credits.json
}

run_in_all fix_pack_version

# Refresh
run_in_all packwiz refresh

# Turn into pack
pack_up() {
    packed_name="${ODIR}/packs/${pack_ver}.mrpack"
    packwiz mr export -o "${packed_name}"
    print "Pack name is ${packed_name} for $pack_edition"
}

run_in_all pack_up
