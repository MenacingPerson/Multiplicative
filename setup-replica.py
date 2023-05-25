#!/usr/bin/env python

import glob
import tomli
import tomli_w
import json
import subprocess
import shutil
import sys
import os

ODIR = os.path.dirname(os.path.realpath(sys.argv[0]))
os.chdir(ODIR)


def echo(text: str):
    return print(f"\n\033[0;32m======>\033[0m {text}")


def splitstr(string: str):
    return string.split(' ')


def runcmd(cmd: str, *args):
    return subprocess.run([*splitstr(cmd), *args])


def chodir():
    os.chdir(f'{ODIR}/Modified/versions')


def toml_read(filename: str) -> dict:
    with open(filename, 'rb') as file:
        return tomli.load(file)


def toml_write(content: dict, filename: str):
    with open(filename, 'wb') as file:
        return tomli_w.dump(content, file)


with open('./config.json', 'rb') as conffile:
    config = json.load(conffile)


# Reset to certain hash to avoid unwanted changes
echo('Updating Additive to specified hash')
runcmd('git submodule update --recursive --init')
os.chdir('Additive/')
runcmd('git reset --hard', config["additive_hash"])
os.chdir(ODIR)


# Recreate modified pack
echo("Removing previous modified packs")
if os.path.exists(f'{ODIR}/Modified'):
    shutil.rmtree(f'{ODIR}/Modified')
if os.path.exists(f'{ODIR}/packs'):
    shutil.rmtree(f'{ODIR}/packs')
os.mkdir(f'{ODIR}/packs')
shutil.copytree(f'{ODIR}/Additive', f'{ODIR}/Modified')
chodir()

# Remove unwanted versions
for i in config['unwanted_mc_versions']:
    if os.path.isdir(i):
        echo(f'Removing pack version {i}')
        shutil.rmtree(i)


# Function to run in certain packs
def run_in(modloader: str, func, args: list = []):
    match modloader:
        case 'fabric':
            for pack_edition in glob.glob('fabric/*'):
                if pack_edition == []:
                    Exception('No fabric versions found!')
                pack_name_full = \
                    f'{config["pack_name"]}-{config["pack_version"]}-{pack_edition.replace("/", "+")}'
                os.chdir(pack_edition)
                func(pack_edition, pack_name_full, *args)
                chodir()
        case 'quilt':
            for pack_edition in glob.glob('quilt/*'):
                if pack_edition == []:
                    Exception('No quilt versions found!')
                pack_name_full = \
                    f'{config["pack_name"]}-{config["pack_version"]}-{pack_edition.replace("/", "+")}'
                os.chdir(pack_edition)
                func(pack_edition, pack_name_full, *args)
                chodir()
        case 'all':
            run_in('fabric', func, args)
            run_in('quilt', func, args)
        case _:
            raise Exception('That\'s not a modloader!')


# TODO: Fix duplicate logic here

def add_mods(pack_edition: str, pack_name_full: str, platform: str, mod_list_key: str):
    match platform:
        case 'mr' | 'modrinth':
            for mod in config[mod_list_key]:
                mod = mod.split('::')
                if len(mod) != 2:
                    raise Exception(f"Mod version not specified for mod {mod[0]}")
                echo(f"Adding modrinth mod {mod[0]} version {mod[1]} to {pack_edition}")
                runcmd('packwiz mr add', mod[0], '--version-filename', mod[1])
        case 'cf' | 'curseforge':
            for mod in config[mod_list_key]:
                mod = mod.split('::')
                if len(mod) != 2:
                    raise Exception(f"Mod version not specified for mod {mod[0]}")
                echo(f"Adding curseforge mod {mod[0]} version {mod[1]} to {pack_edition}")
                runcmd('packwiz cf add --category mc-mods', mod[0], '--file-id', mod[1])
        case _:
            raise Exception(f'Platform name {platform} is invalid! exiting...')


run_in('fabric', add_mods, ['mr', 'mods_mr_fabric'])
run_in('fabric', add_mods, ['cf', 'mods_cf_fabric'])
run_in('quilt', add_mods, ['mr', 'mods_mr_quilt'])
run_in('quilt', add_mods, ['cf', 'mods_cf_quilt'])
run_in('all', add_mods, ['mr', 'mods_mr'])
run_in('all', add_mods, ['cf', 'mods_cf'])


def rm_mods(pack_edition: str, pack_name_full: str, mods_removed_key: str):
    for mod in config[mods_removed_key]:
        echo(f'Removing mod {mod} from version {pack_edition}')
        runcmd('packwiz remove', mod)


# Remove unwanted mods
run_in('fabric', rm_mods, ['mods_removed_fabric'])
run_in('quilt', rm_mods, ['mods_removed_quilt'])
run_in('all', rm_mods, ['mods_removed'])


# TODO: code to modify pack.toml files here
def modify_edition_name(pack_edition: str, pack_name_full: str, optional_mods_key: str):
    pack_toml = toml_read('./pack.toml')
    pack_toml['name'] = config['pack_name']
    pack_toml['author'] = config['pack_author']
    pack_toml['version'] = pack_name_full
    toml_write(pack_toml, './pack.toml')
    for mod in config[optional_mods_key]:
        print(f'Marked {mod} as optional in {optional_mods_key}')
        mod_toml = toml_read(f'mods/{mod}.pw.toml')
        mod_toml['option'] = {
            'optional': True
        }
        toml_write(mod_toml, f'mods/{mod}.pw.toml')


run_in('all', modify_edition_name, ['mods_optional'])
run_in('fabric', modify_edition_name, ['mods_optional_fabric'])
run_in('quilt', modify_edition_name, ['mods_optional_quilt'])


def config_cp(pack_edition, pack_name_full):
    echo(f'Copying config files over for {pack_edition}')
    return shutil.copytree(f'{ODIR}/config', './config', dirs_exist_ok=True)


# Copy config files over
run_in('all', config_cp)

# TODO: change this so file in the config folder is not needed


def fix_mmc_config(pack_edition, pack_name_full):
    with open('./config/isxander-main-menu-credits.json', 'r') as mmc_config:
        mmc_conf_json = json.load(mmc_config)
    mmc_conf_json['main_menu']['bottom_left'][0]['text'] = \
        f'{config["pack_name"]} {config["pack_version"]}'
    with open('./config/isxander-main-menu-credits.json', 'w') as mmc_config:
        json.dump(mmc_conf_json, mmc_config, indent=4)


run_in('all', fix_mmc_config)


def packwiz_refresh(pack_edition, pack_name_full):
    return runcmd('packwiz refresh')


run_in('all', packwiz_refresh)


def create_pack(pack_edition, pack_name_full):
    echo(f'Packing up {pack_edition}')
    runcmd('packwiz mr export -o', f'{ODIR}/packs/{pack_name_full}.mrpack')


run_in('all', create_pack)

echo('Packed files located in packs folder:')
print('  '.join(os.listdir(f'{ODIR}/packs')))
