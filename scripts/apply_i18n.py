#!/usr/bin/env python3
"""Wrap leftover English copy and generate CopyCatalog.cs."""
from __future__ import annotations

import json
import re
from html import unescape, escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VIEWS = ROOT / "src/MajesticRoofing.Web/Views"
CATALOG = ROOT / "src/MajesticRoofing.Web/Infrastructure/CopyCatalog.cs"

SKIP_FILES = {
    "_ViewImports.cshtml",
    "_ViewStart.cshtml",
    "_ValidationScriptsPartial.cshtml",
    "Error.cshtml",
}

SKIP_TEXT = {
    "CALL MAJESTIC",
    "EMAIL",
    "MAJESTIC",
    "ROOFING, INC.",
    "EN / ES",
    "FREE",
    "10 YEAR",
    "STATE FARM",
    "ALLSTATE",
    "LIBERTY MUTUAL",
    "AND OTHER CARRIERS",
    "INSTAGRAM",
    "CHARMECK ALERTS",
    "CHARMECK ALERTS",
    "OFFICIAL LOCAL RESOURCE",
    "Ops",
    "English",
    "Español",
}

import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from i18n_map import ES  # type: ignore


def csharp_escape(value: str) -> str:
    return value.replace("\\", "\\\\").replace('"', '\\"')


def razor_call(en: str) -> str:
    return f'@Lang.T("{csharp_escape(en)}")'


def strip_chrome(html: str) -> str:
    html = re.sub(r'<div class="claim-alert">.*?</div></div>', "", html, count=1, flags=re.S)
    html = re.sub(r'<header class="claim-header">.*?</header>', "", html, count=1, flags=re.S)
    html = re.sub(r'<footer class="claim-footer">.*?</footer>', "", html, count=1, flags=re.S)
    return html


def wrap_html(html: str, mapping: dict[str, str]) -> str:
    items = sorted(mapping.items(), key=lambda kv: len(kv[0]), reverse=True)
    for en, _es in items:
        if len(en) < 3 or en in SKIP_TEXT:
            continue
        call = razor_call(en)
        variants = [en]
        amp = escape(en, quote=False)
        if amp != en:
            variants.append(amp)
        for variant in variants:
            html = html.replace(f">{variant}<", f">{call}<")
            html = html.replace(f">{variant} <", f">{call} <")
            html = html.replace(f'placeholder="{variant}"', f'placeholder="{call}"')
            html = html.replace(f'alt="{variant}"', f'alt="{call}"')
            html = html.replace(f'aria-label="{variant}"', f'aria-label="{call}"')
            if len(variant) >= 40:
                pieces = re.split(r'(@Lang\.T\("(?:\\.|[^"\\])*"(?:\s*,\s*"(?:\\.|[^"\\])*")?\))', html)
                rebuilt = []
                for idx, piece in enumerate(pieces):
                    if idx % 2 == 1:
                        rebuilt.append(piece)
                    else:
                        rebuilt.append(piece.replace(variant, call))
                html = "".join(rebuilt)
    return html


def write_catalog(mapping: dict[str, str]) -> None:
    lines = [
        "using System.Collections.Generic;",
        "",
        "namespace MajesticRoofing.Web.Infrastructure;",
        "",
        "public static class CopyCatalog",
        "{",
        "    public static readonly IReadOnlyDictionary<string, string> Es = new Dictionary<string, string>",
        "    {",
    ]
    for en, es in mapping.items():
        lines.append(f'        ["{csharp_escape(en)}"] = "{csharp_escape(es)}",')
    lines.append("    };")
    lines.append("}")
    lines.append("")
    CATALOG.write_text("\n".join(lines))
    print("wrote", CATALOG, "entries", len(mapping))


def leftover(html: str) -> list[str]:
    html = re.sub(r'@Lang\.T\("(?:\\.|[^"\\])*"(?:\s*,\s*"(?:\\.|[^"\\])*")?\)', "", html)
    found = []
    for raw in re.findall(r">([^<]{8,})<", html):
        text = re.sub(r"\s+", " ", unescape(raw)).strip()
        if not text or text in SKIP_TEXT:
            continue
        if text.startswith("@") or "AntiForgery" in text or text.startswith("}"):
            continue
        if re.fullmatch(r"[\d$×·•—–→✓⌁●↗+\-\s\.,:/()A-Z]+", text) and " " not in text.strip():
            continue
        found.append(text)
    return found


def main() -> None:
    mapping = dict(ES)
    write_catalog(mapping)
    leftovers: dict[str, list[str]] = {}
    for path in sorted(VIEWS.rglob("*.cshtml")):
        if path.name in SKIP_FILES:
            continue
        html = path.read_text()
        if path.parent.name == "Pages":
            html = strip_chrome(html)
        html = wrap_html(html, mapping)
        path.write_text(html)
        extra = leftover(html)
        if extra:
            leftovers[str(path.relative_to(VIEWS))] = extra
            print(path.name, "leftover", len(extra))
        else:
            print("ok", path.name)
    (ROOT / "scripts/i18n_leftover.json").write_text(json.dumps(leftovers, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
