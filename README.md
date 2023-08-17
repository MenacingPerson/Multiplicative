# Multiplicative

My custom modpack, meant to be played on servers and singleplayer

# Mod list

To find the mod list, look at [mod-list.md](./mod-list.md).
Alternatively, run the following script to generate the list (unix-like OSes only):
```
./scripts/gen_mod_list.sh
```

# Usage as a base for another pack

For this purpose, you can clone this repo and use it as a sort of template to develop your modpack.
The `config.json` files contains extra fields that I don't use exactly for this purpose.
All branding is contained within base_config.json.
Thus, the only file you would need to change is the `base_config.json`,config folder (`conf`) and README.md.
Also, you would need to remove all branding of `Multiplicative` from this pack.
Feel free to credit me, though!

# Compiling modpack

Required tools in $PATH:
- `git`
- `packwiz`
- `python`
- jq
- unix-like coreutils

```bash
# Install git, packwiz, python, jq
# Modify config.json according to liking

  $ git clone --recursive https://github.com/MenacingPerson/Multiplicative.git
  $ cd ./Multiplicative
# OPTIONALLY setup a python venv here
  $ python -m pip install -r requirements.txt
  $ bash ./scripts/runscript.sh

# Import preferred pack in your launcher
```

#### Licensed under MIT

#### Based on [Additive](https://github.com/intergrav/Additive)
