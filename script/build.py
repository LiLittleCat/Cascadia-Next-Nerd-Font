#!/usr/bin/env python3
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import tarfile
import zipfile
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

from fontTools.ttLib import TTFont, TTCollection
from fontTools.ttLib.tables._n_a_m_e import NameRecord
from fontTools.varLib.instancer import instantiateVariableFont


# ── ANSI colors ──────────────────────────────────────────────────────────────
_RST  = "\033[0m"
_BOLD = "\033[1m"
_RED  = "\033[31m"
_GRN  = "\033[32m"
_YLW  = "\033[33m"
_CYN  = "\033[36m"


def _c(text: object, *codes: str) -> str:
    return "".join(codes) + str(text) + _RST


WEIGHT_TO_STYLE: Dict[int, str] = {
    100: "Thin",
    200: "ExtraLight",
    300: "Light",
    400: "Regular",
    500: "Medium",
    600: "SemiBold",
    700: "Bold",
    800: "ExtraBold",
    900: "Black",
}

SUPPORTED_FONTS: Dict[str, str] = {
    "CascadiaNextSC": "Cascadia Next SC NF",
    "CascadiaNextTC": "Cascadia Next TC NF",
    "CascadiaNextJP": "Cascadia Next JP NF",
}

SHORT_NAMES: Dict[str, str] = {
    "CascadiaNextSC": "CNextSCNF",
    "CascadiaNextTC": "CNextTCNF",
    "CascadiaNextJP": "CNextJPNF",
}


def run(cmd: list[str], cwd: Path | None = None) -> None:
    print("+", " ".join(str(x) for x in cmd))
    subprocess.run(cmd, cwd=str(cwd) if cwd else None, check=True)


def find_ffpython(explicit: str | None) -> str:
    if explicit:
        return explicit
    for candidate in ("ffpython", "ffpython.exe"):
        found = shutil.which(candidate)
        if found:
            return found
    raise FileNotFoundError(
        "ffpython not found. Make sure FontForge is installed and ffpython is on PATH, "
        "or specify it with --ffpython."
    )


def find_font_patcher(explicit: str | None) -> Path:
    if explicit:
        path = Path(explicit).expanduser().resolve()
        if not path.exists():
            raise FileNotFoundError(f"找不到 font-patcher: {path}")
        return path

    _project_root = Path(__file__).resolve().parent.parent
    _candidates = [
        "font-patcher",
        "font-patcher.py",
        str(_project_root / "FontPatcher" / "font-patcher"),
        str(_project_root / "FontPatcher" / "font-patcher.py"),
    ]
    for candidate in _candidates:
        path = Path(candidate).resolve()
        if path.exists():
            return path

    raise FileNotFoundError(
        "font-patcher not found. Place it in the current directory, under FontPatcher/, "
        "or specify it with --font-patcher."
    )


def get_font_info(font_path: Path) -> Tuple[str, str]:
    for prefix, family in SUPPORTED_FONTS.items():
        if font_path.name.startswith(prefix):
            return prefix, family
    raise ValueError(
        f"Unsupported font filename: {font_path.name}\n"
        f"Supported prefixes: {', '.join(SUPPORTED_FONTS.keys())}"
    )


def build_static_instance(vf_path: Path, source_prefix: str, weight: int, temp_dir: Path) -> Path:
    style = WEIGHT_TO_STYLE.get(weight, f"W{weight}")
    output_path = temp_dir / f"{source_prefix}-{style}.ttf"

    print(_c("Instantiating:", _CYN), f"{vf_path.name} → {output_path.name}  (wght={weight})")
    vf = TTFont(str(vf_path))
    static_font = instantiateVariableFont(
        vf,
        {"wght": weight},
        inplace=False,
        overlap=True,
    )
    static_font.save(str(output_path))
    static_font.close()
    vf.close()
    return output_path


def patch_nerd_font(
    ffpython: str,
    font_patcher: Path,
    static_font_path: Path,
    temp_dir: Path,
    temp_name: str,
) -> Path:
    before = {p.resolve() for p in temp_dir.glob("*.ttf")}

    cmd = [
        ffpython,
        str(font_patcher),
        str(static_font_path),
        "--complete",
        "--name",
        temp_name,
        "--outputdir",
        str(temp_dir),
    ]
    run(cmd)

    after = [p.resolve() for p in temp_dir.glob("*.ttf")]
    new_files = [Path(p) for p in after if p not in before and Path(p).name != static_font_path.name]

    if new_files:
        new_files.sort(key=lambda p: p.stat().st_mtime, reverse=True)
        return new_files[0]

    candidates = sorted(
        [p for p in temp_dir.glob("*.ttf") if p.name != static_font_path.name],
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    if not candidates:
        raise FileNotFoundError(f"没有在 {temp_dir} 找到 patch 后的 ttf 文件")
    return candidates[0]


def _remove_name_records(font: TTFont, name_ids: Iterable[int]) -> None:
    remove_ids = set(name_ids)
    font["name"].names = [n for n in font["name"].names if n.nameID not in remove_ids]


def _set_name_record(
    font: TTFont,
    name_id: int,
    value: str,
    platform_id: int,
    plat_enc_id: int,
    lang_id: int,
) -> None:
    record = NameRecord()
    record.nameID = name_id
    record.platformID = platform_id
    record.platEncID = plat_enc_id
    record.langID = lang_id

    if platform_id == 3:
        record.string = value.encode("utf-16-be")
    else:
        record.string = value.encode("mac_roman", errors="replace")

    font["name"].names.append(record)


def set_font_names(font_path: Path, final_family: str, style_name: str, output_path: Path) -> Path:
    family_compact = final_family.replace(" ", "")
    ps_name = f"{family_compact}-{style_name.replace(' ', '')}"
    full_name = final_family if style_name == "Regular" else f"{final_family} {style_name}"

    font = TTFont(str(font_path))
    _remove_name_records(font, [1, 2, 4, 6, 16, 17])

    for lang_id in (0x0409,):
        _set_name_record(font, 1, final_family, 3, 1, lang_id)
        _set_name_record(font, 2, style_name, 3, 1, lang_id)
        _set_name_record(font, 4, full_name, 3, 1, lang_id)
        _set_name_record(font, 6, ps_name, 3, 1, lang_id)
        _set_name_record(font, 16, final_family, 3, 1, lang_id)
        _set_name_record(font, 17, style_name, 3, 1, lang_id)

    for lang_id in (0,):
        _set_name_record(font, 1, final_family, 1, 0, lang_id)
        _set_name_record(font, 2, style_name, 1, 0, lang_id)
        _set_name_record(font, 4, full_name, 1, 0, lang_id)
        _set_name_record(font, 6, ps_name, 1, 0, lang_id)
        _set_name_record(font, 16, final_family, 1, 0, lang_id)
        _set_name_record(font, 17, style_name, 1, 0, lang_id)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    font.save(str(output_path))
    font.close()
    return output_path


def build_ttc(ttf_files: List[Path], ttc_path: Path) -> None:
    ttc_path.parent.mkdir(parents=True, exist_ok=True)
    if ttc_path.exists():
        ttc_path.unlink()

    collection = TTCollection()
    collection.fonts = [TTFont(str(p)) for p in ttf_files]
    try:
        collection.save(str(ttc_path))
    finally:
        for font in collection.fonts:
            font.close()


def create_zip(source_dir: Path, zip_path: Path) -> None:
    zip_path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for path in sorted(source_dir.rglob("*")):
            if path.is_file():
                zf.write(path, arcname=path.relative_to(source_dir))


def create_tar_gz(source_dir: Path, tar_gz_path: Path) -> None:
    tar_gz_path.parent.mkdir(parents=True, exist_ok=True)
    with tarfile.open(tar_gz_path, "w:gz") as tf:
        for path in sorted(source_dir.rglob("*")):
            tf.add(path, arcname=path.relative_to(source_dir))


def clean_dir(path: Path) -> None:
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True, exist_ok=True)


def process_one_font(
    vf_path: Path,
    weights: Iterable[int],
    ffpython: str,
    font_patcher: Path,
    dist_root: Path,
    temp_root: Path,
) -> None:
    source_prefix, final_family = get_font_info(vf_path)
    family_compact = final_family.replace(" ", "")
    short_name = SHORT_NAMES[source_prefix]

    family_dist = dist_root / source_prefix
    ttf_dir = family_dist / "ttf"
    ttc_dir = family_dist / "ttc"
    archives_dir = family_dist / "archives"

    clean_dir(ttf_dir)
    clean_dir(ttc_dir)
    clean_dir(archives_dir)

    work_dir = temp_root / source_prefix
    clean_dir(work_dir)

    built_ttf_files: List[Path] = []

    for weight in weights:
        style_name = WEIGHT_TO_STYLE.get(weight, f"W{weight}")
        static_font = build_static_instance(vf_path, source_prefix, weight, work_dir)
        patched_font = patch_nerd_font(ffpython, font_patcher, static_font, work_dir, short_name)

        final_ttf = ttf_dir / f"{family_compact}-{style_name}.ttf"
        set_font_names(patched_font, final_family, style_name, final_ttf)
        built_ttf_files.append(final_ttf)
        print(_c("✓ TTF:", _GRN, _BOLD), str(final_ttf))

        for temp_file in (static_font, patched_font):
            if temp_file.exists():
                try:
                    temp_file.unlink()
                except OSError:
                    pass

    ttc_path = ttc_dir / f"{family_compact}.ttc"
    build_ttc(sorted(built_ttf_files), ttc_path)
    print(_c("✓ TTC:", _GRN, _BOLD), str(ttc_path))

    zip_ttf = archives_dir / f"{family_compact}-ttf.zip"
    targz_ttf = archives_dir / f"{family_compact}-ttf.tar.gz"
    zip_ttc = archives_dir / f"{family_compact}-ttc.zip"
    targz_ttc = archives_dir / f"{family_compact}-ttc.tar.gz"

    create_zip(ttf_dir, zip_ttf)
    create_tar_gz(ttf_dir, targz_ttf)
    create_zip(ttc_dir, zip_ttc)
    create_tar_gz(ttc_dir, targz_ttc)

    for _arc in (zip_ttf, targz_ttf, zip_ttc, targz_ttc):
        print(_c("✓ Archive:", _GRN), str(_arc))

    if work_dir.exists():
        shutil.rmtree(work_dir)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Instantiate CascadiaNextSC/TC/JP.wght.ttf into static weights and apply full Nerd Font patches, output to dist/"
    )
    parser.add_argument(
        "fonts",
        nargs="*",
        default=[
            "CascadiaNextSC.wght.ttf",
            "CascadiaNextTC.wght.ttf",
            "CascadiaNextJP.wght.ttf",
        ],
        help="Variable font files to process (default: SC/TC/JP all three in original/)",
    )
    parser.add_argument(
        "--weights",
        nargs="+",
        type=int,
        default=[200, 300, 400, 500, 600, 700, 800],
        help="Weights to generate (default: 200 300 400 500 600 700 800)",
    )
    parser.add_argument(
        "--ffpython",
        default=None,
        help="Full path to ffpython; auto-detected from PATH if omitted",
    )
    parser.add_argument(
        "--font-patcher",
        default=None,
        help="Path to font-patcher; searched in cwd and FontPatcher/ if omitted",
    )
    parser.add_argument(
        "--out",
        default="dist",
        help="Output root directory (default: dist)",
    )
    parser.add_argument(
        "--temp",
        default=".build_temp",
        help="Temporary working directory (default: .build_temp)",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    ffpython = find_ffpython(args.ffpython)
    font_patcher = find_font_patcher(args.font_patcher)

    dist_root = Path(args.out).expanduser().resolve()
    temp_root = Path(args.temp).expanduser().resolve()
    dist_root.mkdir(parents=True, exist_ok=True)
    temp_root.mkdir(parents=True, exist_ok=True)

    _script_dir = Path(__file__).resolve().parent
    _project_root = _script_dir.parent
    _default_font_dir = _project_root / "original"

    font_files = [
        ((_default_font_dir / p) if not Path(p).is_absolute() and not Path(p).exists() else Path(p))
        .expanduser().resolve()
        for p in args.fonts
    ]

    missing = [str(p) for p in font_files if not p.exists()]
    if missing:
        print(_c("The following font files do not exist:", _RED, _BOLD), file=sys.stderr)
        for item in missing:
            print(f"  {item}", file=sys.stderr)
        return 2

    for font_file in font_files:
        try:
            print(_c("=" * 80, _BOLD))
            print(_c("Processing:", _CYN, _BOLD), str(font_file))
            process_one_font(
                vf_path=font_file,
                weights=args.weights,
                ffpython=ffpython,
                font_patcher=font_patcher,
                dist_root=dist_root,
                temp_root=temp_root,
            )
        except Exception as exc:
            print(_c(f"Failed: {font_file} → {exc}", _RED), file=sys.stderr)
            return 1

    if temp_root.exists():
        shutil.rmtree(temp_root)

    print(_c("=" * 80, _BOLD))
    print(_c(f"All done. Output: {dist_root}", _GRN, _BOLD))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
