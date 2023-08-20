"""Pack editions management"""

import glob
import os
import core.base
import core.packwiz


def run_in(modloader: str, func, *args):
    """Run function in certain edition of pack"""
    if modloader not in ('fabric', 'quilt', 'forge', 'all'):
        raise NameError('That\'s not a modloader!')
    if modloader == 'all':
        for i in core.packwiz.modloaders:
            if loader_is_valid(i):
                run_in(i, func, *args)
        return
    for pack_edition_path in glob.glob(f'{modloader}/*'):
        if pack_edition_path == []:
            raise NameError(f'No {modloader} pack editions found!')
        os.chdir(pack_edition_path)
        pack = {}
        pack['modloader'] = modloader
        pack['edition'] = modloader + '+' + core.base.config['game_version']
        pack['fullver'] = f'{core.base.base_conf["pack_name"]}-{core.base.base_conf["pack_version"]}-{pack["edition"]}'
        func(pack, *args)
        core.base.chodir()


def run_separately_in_all(func, *args):
    """Run function separately in all editions"""
    args_forwarded = {}
    for i in core.packwiz.modloaders:
        if loader_is_valid(i):
            args_forwarded[i] = [arg.replace('[ml]', i) for arg in args]
            run_in(i, func, *args_forwarded[i])
    args = [arg.replace('_[ml]', '') for arg in args]
    run_in('all', func, *args)


def loader_is_valid(modloader: str) -> bool:
    return modloader in core.packwiz.modloaders and modloader in core.base.config['modloaders']
