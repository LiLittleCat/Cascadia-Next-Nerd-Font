# Cascadia Next Nerd Font

**[简体中文](README.md)** · **[繁體中文](README.tc.md)** · **English** · **[日本語](README.ja.md)**

[Cascadia Next](https://github.com/microsoft/cascadia-code/releases/tag/cascadia-next) patched with the full [Nerd Fonts](https://www.nerdfonts.com/) icon set. Supports Simplified Chinese (SC), Traditional Chinese (TC), and Japanese (JP) variants.

## Preview
![Preview](showcase/preview.png)

## Variants

| Family Name         | Target    | Weights |
| ------------------- | --------- | ------- |
| Cascadia Next SC NF | Simplified Chinese | 7 |
| Cascadia Next TC NF | Traditional Chinese | 7 |
| Cascadia Next JP NF | Japanese  | 7       |

Available weights: ExtraLight · Light · Regular · Medium · SemiBold · Bold · ExtraBold

---

## Installation

Go to the [Releases](https://github.com/LiLittleCat/Cascadia-Next-Nerd-Font/releases) page and download the archive for your variant:

| File                        | Contents                  |
| --------------------------- | ------------------------- |
| `CascadiaNextSCNF-ttf.zip`  | SC variant, individual TTF files |
| `CascadiaNextSCNF-ttc.zip`  | SC variant, TTC collection |
| `CascadiaNextTCNF-ttf.zip`  | TC variant, individual TTF files |
| `CascadiaNextJPNF-ttf.zip`  | JP variant, individual TTF files |

`.tar.gz` archives are also available with matching filenames.

**macOS (recommended: Homebrew)**
```bash
brew tap LiLittleCat/tap

# Simplified Chinese
brew install --cask font-cascadia-next-sc-nerd-font  
# Traditional Chinese
brew install --cask font-cascadia-next-tc-nerd-font  
# Japanese
brew install --cask font-cascadia-next-jp-nerd-font  
```

**macOS (manual)**
```bash
cp *.ttf ~/Library/Fonts/
```

**Linux**
```bash
mkdir -p ~/.local/share/fonts
cp *.ttf ~/.local/share/fonts/
fc-cache -fv
```

**Windows**: Right-click the `.ttf` / `.ttc` file → **Install for all users**

---

## Usage

After installation, set the font to `Cascadia Next SC NF` (or TC / JP) in your terminal or editor.

**kitty**
```
font_family Cascadia Next SC NF
```

**Alacritty** (`alacritty.toml`)
```toml
[font.normal]
family = "Cascadia Next SC NF"
```

**VS Code** (`settings.json`)
```json
"editor.fontFamily": "'Cascadia Next SC NF', monospace"
```

**Windows Terminal** (`settings.json`)
```json
"font": { "face": "Cascadia Next SC NF" }
```

---

## Build from Source

### Requirements

| Dependency           | Notes                                                        |
| -------------------- | ------------------------------------------------------------ |
| Python ≥ 3.10        | To run the build script                                      |
| fontTools            | `pip install fonttools`                                      |
| FontForge + ffpython | Required by `font-patcher`; `ffpython` must be on PATH       |
| font-patcher         | Place in `FontPatcher/` directory or current directory       |

### Steps

**1. Install system dependencies**

```bash
sudo apt update && sudo apt install -y fontforge python3-fontforge python3-fonttools
```

**2. Clone the repository**

```bash
git clone https://github.com/LiLittleCat/Cascadia-Next-Nerd-Font.git
cd Cascadia-Next-Nerd-Font
```

**3. Download the source fonts**

Go to the [Cascadia Next releases page](https://github.com/microsoft/cascadia-code/releases/tag/cascadia-next), download the archive, and place the following files in `original/`:

```
original/
├── CascadiaNextSC.wght.ttf
├── CascadiaNextTC.wght.ttf
└── CascadiaNextJP.wght.ttf
```

Or download directly from the command line:

```bash
mkdir -p original
wget -O cascadia-next.zip https://github.com/microsoft/cascadia-code/releases/download/cascadia-next/CascadiaNext.zip
unzip cascadia-next.zip "*.wght.ttf" -d original
```

**4. Download font-patcher**

```bash
wget -q https://github.com/ryanoasis/nerd-fonts/raw/refs/heads/master/FontPatcher.zip
unzip FontPatcher.zip -d FontPatcher
```

**5. Run the build**

```bash
# Build all three variants (SC / TC / JP)
python script/build.py

# Build a single variant
python script/build.py original/CascadiaNextSC.wght.ttf

# Build specific weights only
python script/build.py --weights 400 700
```

Output goes to `dist/`.

### Output Structure

```
dist/
├── CascadiaNextSC/
│   ├── ttf/          # Individual TTF per weight
│   ├── ttc/          # All weights in a single TTC collection
│   └── archives/     # .zip and .tar.gz for both ttf and ttc
├── CascadiaNextTC/
│   └── ... (same)
└── CascadiaNextJP/
    └── ... (same)
```

### CLI Reference

```
usage: build.py [-h] [--weights N [N ...]] [--ffpython PATH]
                [--font-patcher PATH] [--out DIR] [--temp DIR]
                [fonts ...]

positional arguments:
  fonts                 Variable font files to process (default: SC/TC/JP in original/)

options:
  --weights N [N ...]   Weights to generate (default: 200 300 400 500 600 700 800)
  --ffpython PATH       Full path to ffpython; auto-detected from PATH if omitted
  --font-patcher PATH   Path to font-patcher; searched in FontPatcher/ if omitted
  --out DIR             Output root directory (default: dist)
  --temp DIR            Temporary working directory (default: .build_temp)
```

### How It Works

1. **Instantiate**: Uses `fontTools.varLib.instancer` to slice the variable font (`.wght.ttf`) into static TTFs per weight.
2. **Patch**: Calls `font-patcher --complete` with a short temporary name (e.g. `CNextSCNF`) to embed the full Nerd Fonts icon set, avoiding the 63-character internal name limit.
3. **Rename**: Overwrites the name table (nameID 1/2/4/6/16/17) using `fontTools` to set the correct final family and PostScript names.
4. **Package**: Merges all weights into a TTC collection and creates `.zip` and `.tar.gz` archives.

---

## License

This project uses two licenses:

| Content                  | License                                        |
| ------------------------ | ---------------------------------------------- |
| Build scripts (`script/`) | [MIT License](LICENSE)                        |
| Output font files        | [SIL Open Font License 1.1](LICENSE-OFL)       |

Font files are derived from [Cascadia Next](https://github.com/microsoft/cascadia-code/releases/tag/cascadia-next) (© Microsoft Corporation, SIL OFL 1.1) and embed icons from [Nerd Fonts](https://github.com/ryanoasis/nerd-fonts) (SIL OFL 1.1).
