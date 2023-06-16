#!/usr/bin/env python


"""
Main Multiplicative pack creation tool.
$1 = config directory
Refer to config.json for configuration info.
"""

import glob
import json
import subprocess
import shutil
import sys
import os
import tomli
import tomli_w

ODIR = os.path.dirname(os.path.realpath(sys.argv[0]))
os.chdir(ODIR)


def echo(text: str, i=6):
    """Echo text with attached green arrow at front"""
    return print('\n\033[0;32m' + '=' * i + f'>\033[0m {text}')


def runcmd(cmd: str, *args):
    """Run command with args using subprocess"""
    return subprocess.run([*cmd.split(' '), *args], check=True)


def chodir():
    """Change dir to Modified/versions"""
    os.chdir(f'{ODIR}/Modified/versions')


# File handling functions

def toml_read(filename: str) -> dict:
    """Read toml file"""
    with open(filename, 'rb') as file:
        return tomli.load(file)


def toml_write(content: dict, filename: str):
    """Write to toml file"""
    with open(filename, 'wb') as file:
        tomli_w.dump(content, file)


def json_read(filename: str) -> dict:
    """Read json file"""
    with open(filename, 'r', encoding='utf_8') as file:
        return json.load(file)


def json_write(content: dict, filename: str, indent: int = 4):
    """Write to json file"""
    with open(filename, 'w', encoding='utf_8') as file:
        json.dump(content, file, indent=indent)


def if_not_exists_create_dir(path: str):
    """Create directory if doesn't exist"""
    if not os.path.exists(path):
        os.mkdir(path)


def if_exists_rm(path: str):
    """Remove path if exists"""
    if os.path.exists(path):
        shutil.rmtree(path)


def if_exists_recreate(path: str):
    """Recreate path if exists"""
    if_exists_rm(path)
    os.mkdir(path)


# Actual logic (functions)

def run_in(modloader: str, func, *args):
    """Run function in certain edition of pack"""
    if modloader not in ('fabric', 'quilt', 'all'):
        raise NameError('That\'s not a modloader!')
    if modloader == 'all':
        run_in('fabric', func, *args)
        run_in('quilt', func, *args)
        return
    for pack_edition_path in glob.glob(f'{modloader}/*'):
        if pack_edition_path == []:
            raise NameError(f'No {modloader} versions found!')
        os.chdir(pack_edition_path)
        pack_edition = pack_edition_path.replace('/', '+')
        pack_fullver = f'{pack_name}-{pack_version}-{pack_edition}'
        func(pack_edition, pack_fullver, *args)
        chodir()


# Adding mods

def add_mod_mr(pack_edition: str, mod: list):
    """Add a modrinth mod"""
    echo(f'Adding modrinth mod {mod[1]} version {mod[2]} to {pack_edition}')
    runcmd(f'packwiz mr add --project-id {mod[1].strip()} --version-id {mod[2]}')


def add_mod_cf(pack_edition: str, mod: list):
    """Add a curseforge mod"""
    echo(f'Adding curseforge mod {mod[1]} version {mod[2]} to {pack_edition}')
    runcmd(f'packwiz mr add --category mc-mods {mod[1].strip()} --file-id {mod[2]}')


def add_mods(pack_edition: str, _pack_fullver: str, mod_list_key: str):
    """Add mods to an edition using a list in config"""
    for mod in config[mod_list_key]:
        if len(mod) != 3:
            raise ValueError(f"Mod platform/name/version unspecified for {mod[1]}")
        match mod[0]:
            case 'mr' | 'modrinth':
                add_mod_mr(pack_edition, mod)
            case 'cf' | 'curseforge':
                add_mod_cf(pack_edition, mod)
            case _:
                raise ValueError(f'Platform name {mod[1]} is invalid! exiting...')


def rm_mods(pack_edition: str, _pack_fullver: str, mods_removed_key: str):
    """Remove mods from an edition using a list in config"""
    for mod in config[mods_removed_key]:
        echo(f'Removing mod {mod} from version {pack_edition}')
        runcmd('packwiz remove', mod)


def modify_packtoml(pack_edition: str, pack_fullver: str):
    """Modify the pack.toml to contain modpack branding"""
    echo(f'Modifying pack.toml file for {pack_edition}')
    pack_toml = toml_read('./pack.toml')
    pack_toml['name'] = base_conf['pack_name']
    pack_toml['author'] = base_conf['pack_author']
    pack_toml['version'] = pack_fullver
    toml_write(pack_toml, './pack.toml')


def mark_mods_optional(pack_edition: str, _pack_fullver: str, optional_mods_key: str):
    """Mark mods as optional in pack edition"""
    echo(f'Marking optional mods using {optional_mods_key} for {pack_edition}')
    for mod in config[optional_mods_key]:
        print(f'Marked {mod} as optional')
        mod_toml = toml_read(f'mods/{mod}.pw.toml')
        mod_toml['option'] = {
            'optional': True
        }
        toml_write(mod_toml, f'mods/{mod}.pw.toml')


def config_cp(pack_edition: str, _pack_fullver: str):
    """Copy config over to edition"""
    echo(f'Copying config files over for {pack_edition}')
    return shutil.copytree(f'{ODIR}/conf/{sys.argv[1]}/config',
                           './config', dirs_exist_ok=True)


def fix_mmc_config(pack_edition: str, _pack_fullver: str):
    """Fix Main Menu Credit json file to include branding"""
    echo(f'Fixing Main Menu Credits config for {pack_edition}')
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


def change_modloader_ver(pack_edition: str, _pack_fullver: str, modloader):
    """Change version of specified modloader"""
    echo(f'Updating {modloader} version to {base_conf[f"{modloader}_version"]} for {pack_edition}')
    pack_toml = toml_read('./pack.toml')
    pack_toml['versions'][modloader] = base_conf[f'{modloader}_version']


def packwiz_refresh(pack_edition: str, _pack_fullver: str):
    """Refresh packwiz"""
    echo(f'Running packwiz refresh for {pack_edition}')
    return runcmd('packwiz refresh')


def export_pack(pack_edition: str, pack_fullver: str):
    """Export mrpack file"""
    echo(f'Packing up {pack_edition}')
    runcmd('packwiz mr export -o', f'{ODIR}/packs/{pack_fullver}.mrpack')


config = json_read(f'{ODIR}/conf/{sys.argv[1]}/config.json')
base_conf = json_read(f'{ODIR}/base_config.json')
pack_name = base_conf['pack_name']
pack_version = base_conf['pack_version']


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

for unwanted_pack_ed in config['unwanted_mc_versions']:
    echo(f'Removing pack edition {unwanted_pack_ed}')
    if os.path.isdir(unwanted_pack_ed):
        shutil.rmtree(unwanted_pack_ed)
    else:
        raise ValueError(f'Unwanted pack version {unwanted_pack_ed} does not exist!')

run_in('fabric', add_mods, 'mods_fabric')
run_in('quilt', add_mods, 'mods_quilt')
run_in('all', add_mods, 'mods')

run_in('all', mark_mods_optional, 'mods_optional')
run_in('fabric', mark_mods_optional, 'mods_optional_fabric')
run_in('quilt', mark_mods_optional, 'mods_optional_quilt')

run_in('fabric', rm_mods, 'mods_removed_fabric')
run_in('quilt', rm_mods, 'mods_removed_quilt')
run_in('all', rm_mods, 'mods_removed')
run_in('all', rm_mods, 'mods_temp_removed')

run_in('all', modify_packtoml)

run_in('all', config_cp)

run_in('all', fix_mmc_config)

run_in('fabric', change_modloader_ver, 'fabric')
run_in('quilt', change_modloader_ver, 'quilt')

run_in('all', packwiz_refresh)

run_in('all', export_pack)

echo('Packed files located in packs folder:')
print('  '.join(os.listdir(f'{ODIR}/packs')))
