#!/usr/bin/env python


"""
Main Multiplicative pack creation tool.
Use the stuff in ./scripts/ instead of this.
$1 = config directory
Refer to config.json for configuration info.
"""

import glob
import shutil
import sys
import os
import core.base
import core.packwiz
import core.pack_editions
from core.base import (echo, ODIR, runcmd, toml_read,
                       toml_write, json_read, json_write,
                       config, base_conf)
from core.packwiz import pw_rm_mods, pw_refresh, pw_export_pack
from core.pack_editions import run_in, run_separately_in_all

os.chdir(core.base.ODIR)

# logic (functions)


def modify_packtoml(pack: dict):
    """Modify the pack.toml to contain modpack branding"""
    echo(f'Modifying pack.toml file for {pack["edition"]}')
    pack_toml = toml_read('./pack.toml')
    pack_toml['name'] = base_conf['pack_name']
    pack_toml['author'] = base_conf['pack_author']
    pack_toml['version'] = pack['fullver']
    toml_write(pack_toml, './pack.toml')


def cp_mods(_pack: dict, mods_key: str):
    """Copy packwiz pw.toml mod files over to pack edition"""
    shutil.copytree(f'{ODIR}/conf/{sys.argv[1]}/{mods_key}', './mods/', dirs_exist_ok=True)


def cp_rps(_pack: dict, rps_key: str):
    """Copy packwiz pw.toml resourcepack files over to pack edition"""
    shutil.copytree(f'{ODIR}/conf/{sys.argv[1]}/{rps_key}',
                    './resourcepacks', dirs_exist_ok=True)


def mark_mods_optional(pack: dict, optional_mods_key: str):
    """Mark mods as optional in pack edition"""
    echo(f'Marking optional mods using {optional_mods_key} for {pack["edition"]}')
    for mod in config[optional_mods_key]:
        print(f'Marked {mod} as optional')
        mod_toml = toml_read(f'mods/{mod}.pw.toml')
        mod_toml['option'] = {
            'optional': True
        }
        toml_write(mod_toml, f'mods/{mod}.pw.toml')


def config_cp(pack: dict):
    """Copy config over to edition"""
    echo(f'Copying config files over for {pack["edition"]}')
    return shutil.copytree(f'{ODIR}/conf/{sys.argv[1]}/config',
                           './config', dirs_exist_ok=True)


def fix_mmc_config(pack: dict):
    """Fix Main Menu Credit json file to include branding"""
    echo(f'Fixing Main Menu Credits config for {pack["edition"]}')
    mmc_conf_json = json_read('./config/isxander-main-menu-credits.json')
    mmc_conf_json = {
        'main_menu': {
            'bottom_left': [
                {
                    'text': f'{base_conf["pack_name"]} {base_conf["pack_version"]}',
                    'clickEvent': {
                        'action': 'open_url',
                        'value': base_conf['pack_url']
                    }
                }
            ]
        }
    }
    json_write(mmc_conf_json, './config/isxander-main-menu-credits.json')


def change_modloader_ver(pack: dict) -> None:
    """Change version of specified modloader"""
    modloader = pack['modloader']
    if core.pack_editions.loader_is_valid(modloader):
        echo(f"Updating {modloader} to {core.base.base_conf['modloaders'][modloader]['version']} for {pack['edition']}")
        pack_toml = toml_read('./pack.toml')
        pack_toml['versions'][modloader] = core.base.base_conf['modloaders'][modloader]['version']
        toml_write(pack_toml, './pack.toml')
    else:
        print(f'{i} is not a valid modloader!')


# Reset to certain hash to avoid unwanted changes
echo('Updating Additive to specified hash')
runcmd('git submodule update --recursive --init --remote')
os.chdir('Additive/')
runcmd('git pull origin main')
runcmd('git reset --hard', base_conf["additive_hash"])
os.chdir(ODIR)
runcmd('git add Additive/')

# Error handling
core.base.if_exists_rm(f'{ODIR}/Additive/Modified')
core.base.if_exists_rm(f'{ODIR}/Additive/packs')

# Recreate modified pack
echo("Removing previous modified packs")
core.base.if_exists_rm(f'{ODIR}/Modified')
core.base.if_not_exists_create_dir(f'{ODIR}/packs')
shutil.copytree(f'{ODIR}/Additive/', f'{ODIR}/Modified/')

core.base.chodir()

unwanted_pack_editions = glob.glob('*/*')
wanted_pack_editions = [modloader + '/' + config['game_version']
                        for modloader in config['modloaders']]
for pack_edition in unwanted_pack_editions:
    if pack_edition in wanted_pack_editions:
        unwanted_pack_editions.remove(pack_edition)
for pack_edition in unwanted_pack_editions:
    shutil.rmtree(pack_edition)

run_in('all', pw_refresh)

run_separately_in_all(cp_mods, 'mods_[ml]')

run_separately_in_all(mark_mods_optional, 'mods_optional_[ml]')

run_separately_in_all(pw_rm_mods, 'mods_removed_[ml]')

run_in('all', cp_rps, 'resourcepacks')

run_in('all', pw_rm_mods, 'mods_temp_removed')

run_in('all', modify_packtoml)

run_in('all', config_cp)

run_in('all', fix_mmc_config)

for i in core.packwiz.modloaders:
    run_in(i, change_modloader_ver)

run_in('all', pw_refresh)

run_in('all', pw_export_pack)

echo('Packed files located in packs folder:')
print('  '.join(os.listdir(f'{ODIR}/packs')))
