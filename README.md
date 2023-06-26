# Multiplicative

My custom modpack, meant to be played on Wynncraft, Hypixel, SMP/Vanilla Servers, and Singleplayer

If you want a base for a modpack you're making, you can clone this repo
and use it as a template to develop your modpack. The config.json file contain
extra fields that I don't use exactly for this purpose. Thus, the only file you
would need to change is the config.json, config folder and README.md. Also, you
would need to remove all branding of `Multiplicative` from your pack.
Feel free to credit me, though!

# Mod list

To find the mod list, look in [mod-list.md](./mod-list.md).
Alternatively, run the following script to generate the list (unix-like OSes only):
```
./gen_mod_list.sh
```


## Optional mods

Marked optional because some might not want them

```
Distant Horizons // Temporarily Disabled in 1.20
```

## Mods removed from Additive

Because I didn't like these/they conflicted with another mod

```
Capes
LambdaBetterGrass
```

# Compiling modpack

Required tools in $PATH:
- `git`
- `packwiz`
- `python`
- unix-like coreutils

Required pip libraries: `tomli`, `tomli_w`

```bash
# Install git, packwiz, python
# Modify config.json according to liking

  $ git clone --recursive --depth 1 https://github.com/MenacingPerson/Multiplicative.git
  $ python -m pip install -r requirements.txt
  $ bash ./runscript.sh

# Import preferred pack in your launcher
```

# Bugs
None currently

##### Licensed under MIT

##### Based on [Additive](https://github.com/intergrav/Additive)
