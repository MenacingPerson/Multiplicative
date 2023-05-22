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


with open('./config.json', 'rb') as conffile:
    config = json.load(conffile)


# Reset to certain hash to avoid unwanted changes
echo('Updating Additive to specified hash')
runcmd('git submodule update --init')
os.chdir('Additive/')
runcmd('git pull origin main')
runcmd('git reset --hard', config["additive_hash"])
os.chdir(ODIR)
runcmd('git submodule update --init')

# Recreate modified pack
if os.path.exists(f'{ODIR}/Modified'):
    shutil.rmtree(f'{ODIR}/Modified')
if os.path.exists(f'{ODIR}/packs'):
    shutil.rmtree(f'{ODIR}/packs')
os.mkdir(f'{ODIR}/packs')
shutil.copytree(f'{ODIR}/Additive', f'{ODIR}/Modified')
