# Multiplicative

My custom modpack, meant to be played on Wynncraft, Hypixel, SMP/Vanilla Servers, and Singleplayer

If you want a base for a modpack you're making, you can clone this repo
and use it as a template to develop your modpack. The config.json file contain
extra fields that I don't use exactly for this purpose. Thus, the only file you
would need to change is the config.json, config folder and README.md. Also, you
would need to remove all branding of `Multiplicative` from your pack.
Feel free to credit me, though!

# Mod list

```
// In addition to all mods in Additive, minus removed mods

3D Skin Layers
Blur (Fabric)
CameraOverhaul
Chat Heads
CompleteConfig
Cosmetica
CreativeCore
Do a Barrel Roll
Don't Clear Chat History
Dynamic FPS
EMI
Gamma Utils
ItemPhysic Lite
Jade
Model Gap Fix
ModernFix
Mods Command
MoreChatHistory
Nicer Skies
No Chat Reports
Not Enough Animations
Presence Footsteps
Raised
Remember My Txt
Server Pack Unlocker
Smooth Swapping
Sound Physics Remastered
Spark
Wavey Capes
Who am I?
```

## Optional mods

Marked optional because some might not want them

```
Distant Horizons
```

## Mods removed from Additive

Because I didn't like these/they conflicted with another mod

```
Capes
Exordium
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
  $ python -m pip install tomli tomli_w
  $ python ./setup.py

# Import preferred pack in your launcher
```

# Bugs
Currently when compiling the pack, it downloads latest version of mods instead of specified one

##### Licensed under MIT

##### Based on [Additive](https://github.com/intergrav/Additive)
