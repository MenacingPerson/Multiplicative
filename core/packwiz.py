"""Functions for packwiz"""

import requests
from core.base import echo, runcmd, config, ODIR

modloader_compat = {
    'fabric': ['fabric'],
    'quilt': ['fabric', 'quilt']
}

requests_headers = {
    'User-Agent': 'MenacingPerson/Multiplicative'
}


def query_modrinth_project_versions(pack: dict, modid: str):
    """Query modrinth API for project versions"""
    mod_url_path = f'https://api.modrinth.com/v2/project/{modid}/version' + \
        '?loaders=' + str(modloader_compat[pack['modloader']]) \
        .replace("'", '"') + '&game_versions=' + \
        str(config['game_version_compat']).replace("'", '"')
    return (ver['id'] for ver in requests.request(
        'GET', mod_url_path, timeout=5, headers=requests_headers).json())


def pw_rm_mods(pack: dict, mods_removed_key: str) -> None:
    """Remove mods from an edition using a list in config"""
    for mod in config[mods_removed_key]:
        echo(f'Removing mod {mod} from version {pack["edition"]}')
        runcmd('packwiz remove', mod)


def pw_refresh(pack: dict):
    """Refresh packwiz"""
    echo(f'Running packwiz refresh for {pack["edition"]}')
    return runcmd('packwiz refresh')


def pw_export_pack(pack: dict):
    """Export mrpack file"""
    echo(f'Packing up {pack["edition"]}')
    runcmd('packwiz mr export -o', f'{ODIR}/packs/{pack["fullver"]}.mrpack')
