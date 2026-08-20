#!/usr/bin/env python3
"""Generate Razor views and assets from the ChatGPT prototype cache."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / ".proto-cache"
WEB = ROOT / "src" / "MajesticRoofing.Web"
VIEWS = WEB / "Views"
WWW = WEB / "wwwroot"


def extract_main(html: str) -> str:
    m = re.search(r"<main[^>]*>(.*)</main>", html, re.S)
    main = m.group(1) if m else html
    main = re.sub(r"<script[\s\S]*?</script>", "", main)
    main = main.replace("/projects/", "/img/projects/")
    main = main.replace("<!-- -->", "")
    return main


def home_body(main: str) -> str:
    m = re.search(r'<section class="hero"', main)
    start = m.start() if m else 0
    f = main.find('<footer class="site-footer"')
    body = main[start : f if f > 0 else None]
    # Wire contact form to LeadStore
    body = re.sub(
        r'<form class="contact-form">',
        '<form class="contact-form" method="post" action="/leads/contact">\n'
        "@Html.AntiForgeryToken()\n"
        '<input type="hidden" name="language" value="@(Lang.IsSpanish ? "Español" : "English")" />\n'
        '<input type="hidden" name="plannerRange" data-planner-range />\n',
        body,
        count=1,
    )
    body = body.replace(
        'Submitting opens your email app with your project details addressed to Majestic Roofing.',
        '@Lang.T("This sandbox stores your request in memory for the /ops board. No email is sent.", "Este sandbox guarda tu solicitud en memoria para el tablero /ops. No se envía correo.")',
    )
    body = body.replace(
        'Email my request',
        '@Lang.T("Send my request", "Enviar mi solicitud")',
    )
    body = body.replace(
        'type="submit">@Lang.T("Send my request", "Enviar mi solicitud")',
        'type="submit">@Lang.T("Send my request", "Enviar mi solicitud")',
    )
    # Pitch buttons need data attributes for JS
    body = body.replace(
        'class="pitch-option" type="button" aria-pressed="false"><span class="pitch-shape pitch-low"',
        'class="pitch-option" type="button" data-pitch="low" aria-pressed="false"><span class="pitch-shape pitch-low"',
    )
    body = body.replace(
        'class="pitch-option active" type="button" aria-pressed="true"><span class="pitch-shape pitch-standard"',
        'class="pitch-option active" type="button" data-pitch="standard" aria-pressed="true"><span class="pitch-shape pitch-standard"',
    )
    body = body.replace(
        'class="pitch-option" type="button" aria-pressed="false"><span class="pitch-shape pitch-steep"',
        'class="pitch-option" type="button" data-pitch="steep" aria-pressed="false"><span class="pitch-shape pitch-steep"',
    )
    # Calculator fields data attrs
    body = body.replace(
        'placeholder="2000" value="2000"/>',
        'placeholder="2000" value="2000" data-home-size />',
    )
    body = body.replace(
        '<label><span>Stories</span><select>',
        '<label><span>@Lang.T("Stories", "Niveles")</span><select data-stories>',
    )
    body = body.replace(
        '<label><span>Roof material</span><select>',
        '<label><span>@Lang.T("Roof material", "Material del techo")</span><select data-material>',
    )
    body = body.replace(
        '<label><span>Roof shape</span><select>',
        '<label><span>@Lang.T("Roof shape", "Forma del techo")</span><select data-shape>',
    )
    body = body.replace(
        '<label class="checkbox-field"><input type="checkbox" checked=""/>',
        '<label class="checkbox-field"><input type="checkbox" checked data-tearoff />',
    )
    body = body.replace(
        '<div class="calculator-card">',
        '<div class="calculator-card" data-roof-planner>',
    )
    body = body.replace(
        '<div class="calculator-header"><span>Your planning range</span><strong>$16,961 <i>—</i> $21,704</strong><small>Estimated roof area: 2875 sq ft · 28.7 squares</small></div>',
        '<div class="calculator-header"><span>@Lang.T("Your planning range", "Su rango de planificación")</span>'
        '<strong data-range>$16,961 <i>—</i> $21,704</strong>'
        '<small data-area>@Lang.T("Estimated roof area", "Área estimada del techo"): 2,875 sq ft · 28.7 squares</small></div>',
    )
    return body


PAGE_META = {
    "roof-insurance-claim-charlotte-nc": (
        "Roof Insurance Claim Documentation | Charlotte & Rock Hill",
        "Documentación de reclamos de seguro de techo | Charlotte y Rock Hill",
    ),
    "active-roof-leak-repair-charlotte-nc": (
        "Active Roof Leak Repair | Charlotte NC",
        "Reparación de goteras activas | Charlotte NC",
    ),
    "chimney-flashing-leak-repair-charlotte-nc": (
        "Chimney & Flashing Leak Repair | Charlotte NC",
        "Reparación de goteras en chimenea y flashing | Charlotte NC",
    ),
    "hail-damage-roof-inspection-charlotte-nc": (
        "Hail Damage Roof Inspection | Charlotte NC",
        "Inspección de techo por granizo | Charlotte NC",
    ),
    "open-roof-hole-decking-repair-charlotte-nc": (
        "Open Roof Hole & Decking Repair | Charlotte NC",
        "Hueco abierto y reparación de decking | Charlotte NC",
    ),
    "tree-roof-damage-charlotte-nc": (
        "Tree Roof Damage | Charlotte NC",
        "Daño de árbol en el techo | Charlotte NC",
    ),
    "wind-missing-shingles-repair-charlotte-nc": (
        "Wind & Missing Shingles Repair | Charlotte NC",
        "Reparación por viento y shingles faltantes | Charlotte NC",
    ),
    "roofing-charlotte-nc": (
        "Roofing Charlotte NC | Majestic Roofing",
        "Techado Charlotte NC | Majestic Roofing",
    ),
    "roofing-rock-hill-sc": (
        "Roofing Rock Hill SC | Majestic Roofing",
        "Techado Rock Hill SC | Majestic Roofing",
    ),
    "roofing-systems-charlotte-nc": (
        "Roofing Systems Charlotte NC | Majestic Roofing",
        "Sistemas de techo Charlotte NC | Majestic Roofing",
    ),
}


def razor_escape_at(text: str) -> str:
    """Escape @ for Razor (e.g. Instagram handles) while restoring injected directives."""
    markers: dict[str, str] = {}

    def stash(value: str) -> str:
        key = f"§RAZOR{len(markers)}§"
        markers[key] = value
        return key

    # Stash intentional Razor we inject before escaping.
    patterns = [
        r"@Html\.AntiForgeryToken\(\)",
        r"@Lang\.T\([^)]*\)",
        r"@\(Lang\.IsSpanish \? \"[^\"]*\" : \"[^\"]*\"\)",
        r"@Lang\.[A-Za-z]+",
    ]
    for pat in patterns:
        text = re.sub(pat, lambda m: stash(m.group(0)), text)

    text = text.replace("@", "@@")
    for key, value in markers.items():
        text = text.replace(key, value)
    return text


def write_home():
    html = (CACHE / "index.html").read_text(errors="ignore")
    body = home_body(extract_main(html))
    body = razor_escape_at(body)
    content = (
        "@{\n"
        '    ViewData["Title"] = Lang.T(\n'
        '        "Majestic Roofing | Roof Insurance Claims Charlotte & Rock Hill",\n'
        '        "Majestic Roofing | Reclamos de seguro de techo Charlotte y Rock Hill");\n'
        "}\n"
        + body
        + "\n"
    )
    (VIEWS / "Home" / "Index.cshtml").write_text(content)
    print("wrote Home/Index.cshtml", len(content))


def write_pages():
    pages_dir = VIEWS / "Pages"
    pages_dir.mkdir(parents=True, exist_ok=True)
    for path in sorted((CACHE / "pages").glob("*.html")):
        slug = path.stem
        main = extract_main(path.read_text(errors="ignore"))
        # Wire any contact forms if present
        if 'class="contact-form"' in main and "action=" not in main.split('class="contact-form"', 1)[1][:80]:
            main = main.replace(
                '<form class="contact-form">',
                '<form class="contact-form" method="post" action="/leads/contact">\n'
                "@Html.AntiForgeryToken()\n"
                '<input type="hidden" name="language" value="@(Lang.IsSpanish ? "Español" : "English")" />\n',
                1,
            )
        main = razor_escape_at(main)
        en, es = PAGE_META.get(slug, (slug.replace("-", " ").title(), slug.replace("-", " ").title()))
        # View name: Pascal without hyphens is awkward; use slug as filename with underscores
        view_name = slug.replace("-", "_")
        content = (
            "@{\n"
            f'    ViewData["Title"] = Lang.T("{en}", "{es}");\n'
            "}\n"
            + main
            + "\n"
        )
        (pages_dir / f"{view_name}.cshtml").write_text(content)
        print("wrote", view_name, len(content))


def write_i18n_json():
    js = (CACHE / "page.js").read_text(errors="ignore")
    pairs = re.findall(r"e===`en`\?`([^`]*)`:`([^`]*)`", js)
    seen = set()
    clean = []
    for en, es in pairs:
        if en in seen or en.startswith("/") or en in ("es", "en") or len(en) < 3:
            continue
        seen.add(en)
        clean.append([en, es])
    out = CACHE / "extracted" / "i18n.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(clean, ensure_ascii=False, indent=2))
    print("i18n pairs", len(clean))


def main():
    write_i18n_json()
    write_home()
    write_pages()


if __name__ == "__main__":
    main()
