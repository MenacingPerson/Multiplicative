#!/usr/bin/env python

# Command syntax : $1 = optional mod key in config

# This file is for internal use by the shell script only. Do not run manually.
# Syntax provided only for documentation purposes
# It exists because I couldn't find a proper way to edit toml files in bash.

import os
import sys
import tomli
import tomli_w
import json


if len(sys.argv) != 2:
    sys.exit(1)


def readfile(file):
    with open(file, 'rb') as x:
        return tomli.load(x)


def writefile(content, file):
    with open(file, 'wb') as x:
        tomli_w.dump(content, x)


with open(os.environ['MODPACK_CONFIG']) as a:
    config = json.load(a)

pack_edition = os.environ["pack_edition"].replace('/', '+')

x = readfile('pack.toml')
x['name'] = config['pack_name']
x['author'] = config['pack_author']
x['version'] = f'{config["pack_name"]}-{config["pack_version"]}-{pack_edition}'
writefile(x, 'pack.toml')

if sys.argv[1].strip() == "":
    sys.exit()

for i in config[sys.argv[1]]:
    print(f"Marked {i} as optional in {sys.argv[1]}")
    f = f'mods/{i}.pw.toml'
    x = readfile(f)
    x["option"] = {
        "optional": True
    }
    writefile(x, f)
