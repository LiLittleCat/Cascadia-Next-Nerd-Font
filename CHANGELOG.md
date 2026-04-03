# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.1] - 2026-04-03

### Fixed

- Fix monospace detection failures in JetBrains IDEs and Warp terminal caused by incorrect font metadata:
  - Clamp all glyph advance widths that are near or above UPM to the exact UPM value (2048), resolving 1-unit deviations (2046/2047/2049) introduced by font-patcher
  - Set `hhea.advanceWidthMax` to exactly match UPM instead of the computed max from glyph advances
  - Fix `OS/2.fsSelection` bits: bit5 (Bold) and bit6 (Regular) are now mutually exclusive per weight, as required by the OpenType spec
  - Set correct `xAvgCharWidth` to half of UPM for CJK fonts
- Fix `OS/2.fsSelection` for all weight variants: Bold sets bit5 only, Regular sets bit6 only, all other weights clear both bits

## [1.0.0] - 2026-03-31

### Added

- Initial release: Cascadia Next + Nerd Fonts with CJK support
- Build script (`script/build.py`) for patching variable weights into static TTF and merging into TTC
- Three CJK variants: Cascadia Next SC NF (Simplified Chinese), TC NF (Traditional Chinese), JP NF (Japanese)
- 7 weights per variant: ExtraLight, Light, Regular, Medium, SemiBold, Bold, ExtraBold
- GitHub Actions workflow for automated font builds
- Homebrew tap support for macOS installation
- TTF, TTC, zip, and tar.gz output formats

[Unreleased]: https://github.com/LiLittleCat/Cascadia-Next-Nerd-Font/compare/v1.0.1...HEAD
[1.0.1]: https://github.com/LiLittleCat/Cascadia-Next-Nerd-Font/compare/v1.0.0...v1.0.1
[1.0.0]: https://github.com/LiLittleCat/Cascadia-Next-Nerd-Font/releases/tag/v1.0.0
