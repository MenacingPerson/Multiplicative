#!/usr/bin/env python

import tomli
import json
import subprocess
import shutil
import sys
import os

ODIR = os.path.dirname(os.path.realpath(sys.argv[0]))
os.chdir(ODIR)


def echo(text):
    print(f"\n\033[92m======>\033[00m {text}")


def splitstr(string):
    return string.split(' ')


def runcmd(cmd, *args):
    return subprocess.run([*splitstr(cmd), *args])


def chodir():
    os.chdir(ODIR)


with open('./config.json', 'rb') as conffile:
    config = json.load(conffile)


# Reset to certain hash to avoid unwanted changes
echo('Updating Additive to specified hash')
runcmd('git submodule update --recursive --init')
os.chdir('Additive/')
runcmd('git reset --hard', config["additive_hash"])
os.chdir(ODIR)


# Recreate modified pack
if os.path.exists(f'{ODIR}/Modified'):
    shutil.rmtree(f'{ODIR}/Modified')
if os.path.exists(f'{ODIR}/packs'):
    shutil.rmtree(f'{ODIR}/packs')
os.mkdir(f'{ODIR}/packs')
shutil.copytree(f'{ODIR}/Additive', f'{ODIR}/Modified')

# Remove unwanted versions
for i in config['unwanted_mc_versions']:
    if os.path.isdir(i):
        echo(f'Removing pack version {i}')
        shutil.rmtree(i)


# Function to run in certain packs
def run_in(modloader, cmd):
    match modloader:
        case 'fabric':
            for i in os.listdir(f'{ODIR}/versions/fabric'):
                os.chdir(i)
                runcmd(cmd)
                chodir()
        case 'quilt':
            for i in os.listdir(f'{ODIR}/versions/quilt'):
                os.chdir(i)
                runcmd(cmd)
                chodir()
        case 'all':
            run_in('fabric', cmd)
            run_in('quilt', cmd)
        case _:
            raise Exception('That\'s not a modloader!')
