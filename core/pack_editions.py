"""Pack editions management"""

import glob
import os
from core.base import chodir, config, base_conf
import core.packwiz


def run_in(modloader: str, func, *args):
    """Run function in certain edition of pack"""
    if modloader not in ('fabric', 'quilt', 'all'):
        raise NameError('That\'s not a modloader!')
    if modloader == 'all':
        for i in core.packwiz.modloaders:
            if i in config['modloaders']:
                run_in(i, func, *args)
        return
    if modloader not in config['modloaders']:
        raise ValueError(f'Modloader {modloader} has not been added to config!')
    for pack_edition_path in glob.glob(f'{modloader}/*'):
        if pack_edition_path == []:
            raise NameError(f'No {modloader} pack editions found!')
        os.chdir(pack_edition_path)
        pack = {}
        pack['modloader'] = modloader
        pack['edition'] = modloader + '+' + config['game_version']
        pack['fullver'] = f'{base_conf["pack_name"]}-{base_conf["pack_version"]}-{pack["edition"]}'
        func(pack, *args)
        chodir()


def run_separately_in_all(func, *args):
    """Run function separately in all editions"""
    args_forwarded = {}
    for i in core.packwiz.modloaders:
        if i in config['modloaders']:
            args_forwarded[i] = [arg.replace('[ml]', i) for arg in args]
            run_in(i, func, *args_forwarded[i])
    args = [arg.replace('_[ml]', '') for arg in args]
    run_in('all', func, *args)
