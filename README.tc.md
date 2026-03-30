# Cascadia Next Nerd Font

**[简体中文](README.md)** · **繁體中文** · **[English](README.en.md)** · **[日本語](README.ja.md)**

為 [Cascadia Next](https://github.com/microsoft/cascadia-code/releases/tag/cascadia-next) 字體打上完整 [Nerd Fonts](https://www.nerdfonts.com/) 補丁，同時支援簡中（SC）、繁中（TC）、日文（JP）三個中日文變體。

## 預覽
![預覽](showcase/preview.png)

## 字體變體

| 字體族名稱          | 適用場景 | 字重數量 |
| ------------------- | -------- | -------- |
| Cascadia Next SC NF | 簡體中文 | 7        |
| Cascadia Next TC NF | 繁體中文 | 7        |
| Cascadia Next JP NF | 日文     | 7        |

可用字重：ExtraLight · Light · Regular · Medium · SemiBold · Bold · ExtraBold

---

## 安裝

前往 [Releases](https://github.com/LiLittleCat/Cascadia-Next-Nerd-Font/releases) 頁面，下載對應變體的壓縮包：

| 檔案                        | 內容                   |
| --------------------------- | ---------------------- |
| `CascadiaNextSCNF-ttf.zip`  | SC 變體，單個 TTF 檔案 |
| `CascadiaNextSCNF-ttc.zip`  | SC 變體，TTC 合集      |
| `CascadiaNextTCNF-ttf.zip`  | TC 變體，單個 TTF 檔案 |
| `CascadiaNextJPNF-ttf.zip`  | JP 變體，單個 TTF 檔案 |

同時提供 `.tar.gz` 格式，檔名對應將 `.zip` 替換為 `.tar.gz`。

解壓後依系統安裝：

**macOS（推薦：Homebrew）**
```bash
brew tap LiLittleCat/tap

# 簡體中文
brew install --cask font-cascadia-next-sc-nerd-font
# 繁體中文
brew install --cask font-cascadia-next-tc-nerd-font
# 日文
brew install --cask font-cascadia-next-jp-nerd-font
```

**macOS（手動）**
```bash
cp *.ttf ~/Library/Fonts/
```

**Linux**
```bash
mkdir -p ~/.local/share/fonts
cp *.ttf ~/.local/share/fonts/
fc-cache -fv
```

**Windows**：在 `.ttf` / `.ttc` 檔案上按右鍵 → **為所有使用者安裝**

---

## 使用

安裝完成後，在終端機或編輯器中將字體設定為 `Cascadia Next TC NF`（或 SC / JP 變體）。

**kitty**
```
font_family Cascadia Next TC NF
```

**Alacritty** (`alacritty.toml`)
```toml
[font.normal]
family = "Cascadia Next TC NF"
```

**VS Code** (`settings.json`)
```json
"editor.fontFamily": "'Cascadia Next TC NF', monospace"
```

**Windows Terminal** (`settings.json`)
```json
"font": { "face": "Cascadia Next TC NF" }
```

---

## 卸載

**macOS（Homebrew）**
```bash
brew uninstall --cask font-cascadia-next-sc-nerd-font
brew uninstall --cask font-cascadia-next-tc-nerd-font
brew uninstall --cask font-cascadia-next-jp-nerd-font

brew untap LiLittleCat/tap
```

**macOS（手動）**
```bash
rm ~/Library/Fonts/CascadiaNext*NF-*.ttf
```

**Linux**
```bash
rm ~/.local/share/fonts/CascadiaNext*NF-*.ttf && fc-cache -fv
```

**Windows**：控制面板 → 字型 → 對着對應字型按右鍵 → 刪除

---

## 自行建置

### 前置需求

| 相依套件              | 說明                                                     |
| --------------------- | -------------------------------------------------------- |
| Python ≥ 3.10         | 執行建置腳本                                             |
| fontTools             | `pip install fonttools`                                  |
| FontForge + ffpython  | 用於執行 `font-patcher`；需要 `ffpython` 在 PATH 中     |
| font-patcher          | Nerd Fonts 補丁工具，放在 `FontPatcher/` 目錄或目前目錄 |

### 步驟

**1. 安裝系統相依套件**

```bash
sudo apt update && sudo apt install -y fontforge python3-fontforge python3-fonttools
```

**2. 複製儲存庫**

```bash
git clone https://github.com/LiLittleCat/Cascadia-Next-Nerd-Font.git
cd Cascadia-Next-Nerd-Font
```

**3. 下載原始字體**

前往 [Cascadia Next 發布頁](https://github.com/microsoft/cascadia-code/releases/tag/cascadia-next) 下載壓縮包，解壓後將以下檔案放入 `original/`：

```
original/
├── CascadiaNextSC.wght.ttf
├── CascadiaNextTC.wght.ttf
└── CascadiaNextJP.wght.ttf
```

或直接用命令列下載（版本號請依實際修改）：

```bash
mkdir -p original
wget -O cascadia-next.zip https://github.com/microsoft/cascadia-code/releases/download/cascadia-next/CascadiaNext.zip
unzip cascadia-next.zip "*.wght.ttf" -d original
```

**4. 下載 font-patcher**

```bash
wget -q https://github.com/ryanoasis/nerd-fonts/raw/refs/heads/master/FontPatcher.zip
unzip FontPatcher.zip -d FontPatcher
```

**5. 執行建置**

```bash
# 建置全部三個變體（SC / TC / JP）
python script/build.py

# 只建置某一個變體
python script/build.py original/CascadiaNextTC.wght.ttf

# 只產生指定字重
python script/build.py --weights 400 700
```

產物輸出至 `dist/`。

### 輸出目錄結構

```
dist/
├── CascadiaNextSC/
│   ├── ttf/          # 單個 TTF 檔案（每個字重一個）
│   ├── ttc/          # 所有字重合併的 TTC 集合
│   └── archives/     # ttf / ttc 的 .zip 和 .tar.gz 打包
├── CascadiaNextTC/
│   └── ...（同上）
└── CascadiaNextJP/
    └── ...（同上）
```

### 命令列參數

```
usage: build.py [-h] [--weights N [N ...]] [--ffpython PATH]
                [--font-patcher PATH] [--out DIR] [--temp DIR]
                [fonts ...]

positional arguments:
  fonts                 要處理的可變字體檔案（預設處理 original/ 下的 SC/TC/JP）

options:
  --weights N [N ...]   要產生的字重，預設: 200 300 400 500 600 700 800
  --ffpython PATH       ffpython 的完整路徑；省略則從 PATH 自動尋找
  --font-patcher PATH   font-patcher 的路徑；省略則在 FontPatcher/ 或目前目錄尋找
  --out DIR             輸出根目錄，預設: dist
  --temp DIR            暫存工作目錄，預設: .build_temp
```

### 建置流程說明

1. **實例化**：使用 `fontTools.varLib.instancer` 將可變字體（`.wght.ttf`）依目標字重切分為靜態 TTF。
2. **補丁**：以臨時短名（如 `CNextTCNF`）呼叫 `font-patcher --complete`，嵌入完整 Nerd Fonts 圖示，避免內部名稱超過 63 字元限制。
3. **重新命名**：以 `fontTools` 覆寫 name 表（nameID 1/2/4/6/16/17），寫入正確的最終字體族名稱和 PostScript 名稱。
4. **封裝**：將所有字重合併為 TTC，並分別產生 `.zip` 與 `.tar.gz` 封存檔。

---

## 授權條款

本專案包含兩個授權條款：

| 內容                    | 授權條款                                           |
| ----------------------- | -------------------------------------------------- |
| 建置腳本（`script/`）   | [MIT License](LICENSE)                             |
| 輸出字體檔案            | [SIL Open Font License 1.1](LICENSE-OFL)           |

字體檔案衍生自 [Cascadia Next](https://github.com/microsoft/cascadia-code/releases/tag/cascadia-next)（© Microsoft Corporation，SIL OFL 1.1），並嵌入了 [Nerd Fonts](https://github.com/ryanoasis/nerd-fonts) 圖示（SIL OFL 1.1）。
