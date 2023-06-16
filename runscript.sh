#!/usr/bin/env bash

set -e

rm -f ./packs/*.mrpack

script -eq -c './setup.py 1.19.4' /dev/null
script -eq -c './setup.py 1.20' /dev/null
