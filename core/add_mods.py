"""Functions to add mods"""

import time
import requests
from core.base import echo, runcmd, config

modloader_compat = {
    'fabric': ['fabric'],
    'quilt': ['fabric', 'quilt']
}


def query_modrinth_project_versions(pack: dict, modid: str):
    """Query modrinth API for project versions"""
    mod_url_path = f'https://api.modrinth.com/v2/project/{modid}/version' + \
        '?loaders=' + str(modloader_compat[pack['modloader']]) \
        .replace("'", '"') + '&game_versions=' + \
        str(config['game_version_compat']).replace("'", '"')
    return (ver['id'] for ver in requests.request(
        'GET', mod_url_path, timeout=5).json())


def add_mod_mr(pack: dict, mod: list) -> None:
    """Add a modrinth mod"""
    echo(f'Adding modrinth mod {mod[1]} version {mod[2]} to {pack["edition"]}')
    if not mod[2] in query_modrinth_project_versions(pack, mod[1]):
        raise ValueError('File version not in project page')
    runcmd(f'packwiz mr add --project-id {mod[1].strip()} --version-id {mod[2]}')


def add_mod_cf(pack: dict, mod: list) -> None:
    """Add a curseforge mod"""
    echo(f'Adding curseforge mod {mod[1]} version {mod[2]} to {pack["edition"]}')
    runcmd(f'packwiz mr add --category mc-mods {mod[1].strip()} --file-id {mod[2]}')


def add_mods(pack: dict, mod_list_key: str) -> None:
    """Add mods to an edition using a list in config"""
    for mod in config[mod_list_key]:
        if len(mod) != 3:
            raise ValueError(f"Mod platform/name/version unspecified for {mod[1]}")
        time.sleep(0.25)
        match mod[0]:
            case 'mr' | 'modrinth':
                add_mod_mr(pack, mod)
            case 'cf' | 'curseforge':
                add_mod_cf(pack, mod)
            case _:
                raise ValueError(f'Platform name {mod[1]} is invalid! exiting...')
