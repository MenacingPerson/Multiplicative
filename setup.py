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
from core.base import (echo, runcmd, toml_read, toml_write, json_read,
                       json_write, if_not_exists_create_dir,
                       if_exists_rm, ODIR, config, base_conf)
from core.packwiz import pw_add_mods, pw_rm_mods, pw_refresh, pw_export_pack

os.chdir(ODIR)


def chodir() -> None:
    """Change dir to Modified/versions"""
    os.chdir(f'{ODIR}/Modified/versions')

# logic (functions)


def run_in(modloader: str, func, *args):
    """Run function in certain edition of pack"""
    if modloader not in ('fabric', 'quilt', 'all'):
        raise NameError('That\'s not a modloader!')
    elif modloader == 'all':
        if 'fabric' in config['pack_editions']:
            run_in('fabric', func, *args)
        if 'quilt' in config['pack_editions']:
            run_in('quilt', func, *args)
        return
    elif modloader != 'all' and modloader not in config['pack_editions']:
        raise ValueError(f'Modloader {modloader} has not been added to config!')
    for pack_edition_path in glob.glob(f'{modloader}/*'):
        if pack_edition_path == []:
            raise NameError(f'No {modloader} versions found!')
        os.chdir(pack_edition_path)
        pack = {}
        pack['modloader'] = modloader
        pack['edition'] = modloader + '+' + config['game_version']
        pack['fullver'] = f'{base_conf["pack_name"]}-{base_conf["pack_version"]}-{pack["edition"]}'
        func(pack, *args)
        chodir()


def run_separately_in_all(func, *args):
    fabric_args = [arg.replace('[ml]', 'fabric') for arg in args]
    quilt_args = [arg.replace('[ml]', 'quilt') for arg in args]
    args = [arg.replace('_[ml]', '') for arg in args]
    if 'fabric' in config['pack_editions']:
        run_in('fabric', func, *fabric_args)
    if 'quilt' in config['pack_editions']:
        run_in('quilt', func, *quilt_args)
    run_in('all', func, *args)


def modify_packtoml(pack: dict):
    """Modify the pack.toml to contain modpack branding"""
    echo(f'Modifying pack.toml file for {pack["edition"]}')
    pack_toml = toml_read('./pack.toml')
    pack_toml['name'] = base_conf['pack_name']
    pack_toml['author'] = base_conf['pack_author']
    pack_toml['version'] = pack['fullver']
    toml_write(pack_toml, './pack.toml')


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


def change_modloader_ver(pack: dict, modloader) -> None:
    """Change version of specified modloader"""
    echo(f'Updating {modloader} to {base_conf[f"{modloader}_version"]} for {pack["edition"]}')
    pack_toml = toml_read('./pack.toml')
    pack_toml['versions'][modloader] = base_conf[f'{modloader}_version']


# Reset to certain hash to avoid unwanted changes
echo('Updating Additive to specified hash')
runcmd('git submodule update --recursive --init --remote')
os.chdir('Additive/')
runcmd('git pull origin main')
runcmd('git reset --hard', base_conf["additive_hash"])
os.chdir(ODIR)
runcmd('git add Additive/')

# Error handling
if_exists_rm(f'{ODIR}/Additive/Modified')
if_exists_rm(f'{ODIR}/Additive/packs')

# Recreate modified pack
echo("Removing previous modified packs")
if_exists_rm(f'{ODIR}/Modified')
if_not_exists_create_dir(f'{ODIR}/packs')
shutil.copytree(f'{ODIR}/Additive/', f'{ODIR}/Modified/')

chodir()

unwanted_pack_editions = glob.glob('*/*')
wanted_pack_editions = [pack_edition + '/' + config['game_version']
                        for pack_edition in config['pack_editions']]
for pack_edition in unwanted_pack_editions:
    if pack_edition in wanted_pack_editions:
        unwanted_pack_editions.remove(pack_edition)
for pack_edition in unwanted_pack_editions:
    shutil.rmtree(pack_edition)

run_separately_in_all(pw_add_mods, 'mods_[ml]')

run_separately_in_all(mark_mods_optional, 'mods_optional_[ml]')

run_separately_in_all(pw_rm_mods, 'mods_removed_[ml]')

run_in('all', pw_rm_mods, 'mods_temp_removed')

run_in('all', modify_packtoml)

run_in('all', config_cp)

run_in('all', fix_mmc_config)

if 'fabric' in config['pack_editions']:
    run_in('fabric', change_modloader_ver, 'fabric')
if 'quilt' in config['pack_editions']:
    run_in('quilt', change_modloader_ver, 'quilt')

run_in('all', pw_refresh)

run_in('all', pw_export_pack)

echo('Packed files located in packs folder:')
print('  '.join(os.listdir(f'{ODIR}/packs')))
