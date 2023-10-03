"""Functions for packwiz"""

import core.base


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
