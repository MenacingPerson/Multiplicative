"""Functions for packwiz"""

import requests
import core.base

modloaders = {
    'fabric': {
        'modloader_compat': [
            'fabric',
        ],
        'version': core.base.base_conf['modloaders']['fabric']['version']
    },
    'quilt': {
        'modloader_compat': [
            'fabric',
            'quilt',
        ],
        'version': core.base.base_conf['modloaders']['quilt']['version']
    }
}

requests_headers = {
    'User-Agent': core.base.base_conf['pack_user_agent']
}


def query_modrinth_project_versions(pack: dict, modid: str):
    """Query modrinth API for project versions"""
    mod_url_path = f'https://api.modrinth.com/v2/project/{modid}/version?loaders=' \
        + str(modloaders[pack['modloader']]['modloader_compat']) \
        .replace("'", '"') + '&game_versions=' + \
        str(core.base.config['game_version_compat']).replace("'", '"')
    return (ver['id'] for ver in requests.request(
        'GET', mod_url_path, timeout=5, headers=requests_headers).json())


def pw_rm_mods(pack: dict, mods_removed_key: str) -> None:
    """Remove mods from an edition using a list in config"""
    for mod in core.base.config[mods_removed_key]:
        core.base.echo(f'Removing mod {mod} from version {pack["edition"]}')
        core.base.runcmd('packwiz remove', mod)


def pw_refresh(pack: dict):
    """Refresh packwiz"""
    core.base.echo(f'Running packwiz refresh for {pack["edition"]}')
    return core.base.runcmd('packwiz refresh')


def pw_export_pack(pack: dict):
    """Export mrpack file"""
    core.base.echo(f'Packing up {pack["edition"]}')
    core.base.runcmd('packwiz mr export -o', f'{core.base.ODIR}/packs/{pack["fullver"]}.mrpack')
