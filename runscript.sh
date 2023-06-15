#!/usr/bin/env sh

set -e

if [[ -e ./packs/* ]]
then
  rm ./packs/*
fi

script -eq -c './setup.py 1.19.4' /dev/null
script -eq -c './setup.py 1.20' /dev/null
