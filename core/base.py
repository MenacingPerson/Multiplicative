"""Base code for python"""


import os
import subprocess
import sys
import json
import shutil
import tomli
import tomli_w


def echo(text: str, arrow_len=6) -> None:
    """Echo text with attached green arrow at front"""
    return print('\n\033[0;32m' + '=' * arrow_len + f'>\033[0m {text}')


def runcmd(cmd: str, *args) -> subprocess.CompletedProcess:
    """Run command with args using subprocess"""
    return subprocess.run([*cmd.split(' '), *args], check=True)

# File handling functions


def toml_read(filename: str) -> dict:
    """Read toml file"""
    with open(filename, 'rb') as file:
        return tomli.load(file)


def toml_write(content: dict, filename: str) -> None:
    """Write to toml file"""
    with open(filename, 'wb') as file:
        return tomli_w.dump(content, file)


def json_read(filename: str) -> dict:
    """Read json file"""
    with open(filename, 'r', encoding='utf_8') as file:
        return json.load(file)


def json_write(content: dict, filename: str, indent: int = 4) -> None:
    """Write to json file"""
    with open(filename, 'w', encoding='utf_8') as file:
        return json.dump(content, file, indent=indent)


def if_not_exists_create_dir(path: str) -> None:
    """Create directory if doesn't exist"""
    if not os.path.exists(path):
        os.mkdir(path)


def if_exists_rm(path: str) -> None:
    """Remove path if exists"""
    if os.path.exists(path):
        shutil.rmtree(path)


def if_exists_recreate(path: str) -> None:
    """Recreate path if exists"""
    if_exists_rm(path)
    os.mkdir(path)


ODIR = os.path.realpath(os.path.dirname(sys.argv[0]))
config = json_read(f'{ODIR}/conf/{sys.argv[1]}/config.json')
base_conf = json_read(f'{ODIR}/conf/base_config.json')
