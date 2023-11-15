# Multiplicative

My custom modpack, meant to be played on servers and singleplayer

# Mod list

To find the mod list, look at the [mod list](./conf/mod-list.md).
The `./scripts/gen_mod_list.sh` script generates the list (unix-like OSes only)

# Installation using unsup

Use the `./unsup/unsup-curler.sh` script.
Add unsup as a java agent in Prism Launcher directly or use `-javaagent:unsup.jar` as a java argument.

# Usage as a base for another pack

For this purpose, you can clone this modpack repo and use it as a template to develop your own.
All branding is contained within the `base_config.json`.
Thus, the only file you would need to change is the `base_config.json`, the config folder (`conf`) and `README.md`.
Also, you would need to remove all branding of `Multiplicative` from this pack.
(Please credit me, though!)

# Compiling modpack

Required tools:
- `git`
- `packwiz`
- `python`
- `jq`
- (any unix-like coreutils, probably GNU)

```bash
# Modify config.json according to liking

  $ git clone --recursive https://github.com/MenacingPerson/Multiplicative.git
  $ cd Multiplicative
# OPTIONALLY setup a python venv here
  $ python -m pip install -r requirements.txt
  $ bash ./scripts/runscript.sh

# Import preferred pack in your launcher
```

## TODO

- Make the copying process of Additive more robust
  - Copy over the Additive editions to the config's name, not the one it's named as

#### Licensed under MIT

#### Based on [Additive](https://github.com/intergrav/Additive)
