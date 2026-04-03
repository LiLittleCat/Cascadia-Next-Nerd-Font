# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.1] - 2026-04-03

### 修复

- 修复 JetBrains IDE 和 Warp 终端无法识别字体为等宽字体的问题，原因是字体元数据不正确：
  - 修正 `font-patcher` 引入的 1 单位偏差（2046/2047/2049），将所有接近或超过 UPM 的字形宽度统一设为精确 UPM 值（2048）
  - `hhea.advanceWidthMax` 设为精确匹配 UPM，而非取字形宽度最大值
  - 修正 `OS/2.fsSelection` 位：bit5（Bold）和 bit6（Regular）按字重互斥，符合 OpenType 规范
  - `xAvgCharWidth` 设为 UPM 的一半，修正 CJK 字体偏移问题

### Fixed

- Fix monospace detection failures in JetBrains IDEs and Warp terminal caused by incorrect font metadata:
  - Clamp all glyph advance widths near or above UPM to the exact value (2048), resolving 1-unit deviations (2046/2047/2049) introduced by font-patcher
  - Set `hhea.advanceWidthMax` to exactly match UPM instead of the computed max from glyph advances
  - Fix `OS/2.fsSelection` bits: bit5 (Bold) and bit6 (Regular) are now mutually exclusive per weight, as required by the OpenType spec
  - Set correct `xAvgCharWidth` to half of UPM for CJK fonts

## [1.0.0] - 2026-03-31

### 新增

- 基于 [Cascadia Next](https://github.com/microsoft/cascadia-code/releases/tag/cascadia-next) 打上完整 [Nerd Fonts](https://www.nerdfonts.com/) 补丁，支持简中（SC）/ 繁中（TC）/ 日文（JP）三个变体，共 7 个字重

### 安装

**macOS（推荐）**
```bash
brew tap LiLittleCat/tap
# SC 简中
brew install --cask font-cascadia-next-sc-nerd-font
# TC 繁中
brew install --cask font-cascadia-next-tc-nerd-font
# JP 日文
brew install --cask font-cascadia-next-jp-nerd-font
```

**Linux**
```bash
cp *.ttf ~/.local/share/fonts/ && fc-cache -fv
```

**Windows**：右键 `.ttf` / `.ttc` → 为所有用户安装

---

### 下载

| 文件 | 说明 |
| ---- | ---- |
| `CascadiaNextSCNF-ttf.zip` | SC 简中，7 个 TTF |
| `CascadiaNextSCNF-ttc.zip` | SC 简中，TTC 合集 |
| `CascadiaNextTCNF-ttf.zip` | TC 繁中，7 个 TTF |
| `CascadiaNextTCNF-ttc.zip` | TC 繁中，TTC 合集 |
| `CascadiaNextJPNF-ttf.zip` | JP 日文，7 个 TTF |
| `CascadiaNextJPNF-ttc.zip` | JP 日文，TTC 合集 |

同时提供 `.tar.gz` 格式。

### 字重

ExtraLight · Light · Regular · Medium · SemiBold · Bold · ExtraBold

### 上游版本

- Cascadia Next：[cascadia-next](https://github.com/microsoft/cascadia-code/releases/tag/cascadia-next)
- Nerd Fonts font-patcher：[v3.4.0](https://github.com/ryanoasis/nerd-fonts/releases/tag/v3.4.0)

### 许可证

字体文件遵循 [SIL Open Font License 1.1](https://github.com/LiLittleCat/Cascadia-Next-Nerd-Font/blob/main/LICENSE-OFL)。

---

### Added

- Three CJK variants with full Nerd Fonts patches built on [Cascadia Next](https://github.com/microsoft/cascadia-code/releases/tag/cascadia-next): SC (Simplified Chinese), TC (Traditional Chinese), JP (Japanese), 7 weights each

### Installation

**macOS (recommended)**
```bash
brew tap LiLittleCat/tap
# SC Simplified Chinese
brew install --cask font-cascadia-next-sc-nerd-font
# TC Traditional Chinese
brew install --cask font-cascadia-next-tc-nerd-font
# JP Japanese
brew install --cask font-cascadia-next-jp-nerd-font
```

**Linux**
```bash
cp *.ttf ~/.local/share/fonts/ && fc-cache -fv
```

**Windows**: Right-click `.ttf` / `.ttc` → Install for all users

---

### Downloads

| File | Description |
| ---- | ----------- |
| `CascadiaNextSCNF-ttf.zip` | SC, 7 TTF files |
| `CascadiaNextSCNF-ttc.zip` | SC, TTC collection |
| `CascadiaNextTCNF-ttf.zip` | TC, 7 TTF files |
| `CascadiaNextTCNF-ttc.zip` | TC, TTC collection |
| `CascadiaNextJPNF-ttf.zip` | JP, 7 TTF files |
| `CascadiaNextJPNF-ttc.zip` | JP, TTC collection |

Also available in `.tar.gz` format.

### Weights

ExtraLight · Light · Regular · Medium · SemiBold · Bold · ExtraBold

### Upstream Versions

- Cascadia Next: [cascadia-next](https://github.com/microsoft/cascadia-code/releases/tag/cascadia-next)
- Nerd Fonts font-patcher: [v3.4.0](https://github.com/ryanoasis/nerd-fonts/releases/tag/v3.4.0)

### License

Font files are licensed under [SIL Open Font License 1.1](https://github.com/LiLittleCat/Cascadia-Next-Nerd-Font/blob/main/LICENSE-OFL).

[Unreleased]: https://github.com/LiLittleCat/Cascadia-Next-Nerd-Font/compare/v1.0.1...HEAD
[1.0.1]: https://github.com/LiLittleCat/Cascadia-Next-Nerd-Font/compare/v1.0.0...v1.0.1
[1.0.0]: https://github.com/LiLittleCat/Cascadia-Next-Nerd-Font/releases/tag/v1.0.0
