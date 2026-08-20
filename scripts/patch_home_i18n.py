#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HOME = ROOT / "src/MajesticRoofing.Web/Views/Home/Index.cshtml"

# Rebuild clean home first via build_views
import subprocess
subprocess.check_call(["python3", str(ROOT / "scripts/build_views.py")], cwd=ROOT)

t = HOME.read_text()
repls = [
    (
        "Roof insurance claim documentation · Charlotte &amp; Rock Hill",
        '@Lang.T("Roof insurance claim documentation · Charlotte & Rock Hill", "Documentación de reclamos de seguro de techo · Charlotte y Rock Hill")',
    ),
    (
        "Roof evidence. Clear scope. Professional roofing.",
        '@Lang.T("Roof evidence. Clear scope. Professional roofing.", "Evidencia del techo. Alcance claro. Techado profesional.")',
    ),
    (
        "Free inspections, factual storm-damage documentation, contractor supplements, roof replacement, repairs, gutters and fascia—with same-business-day response from a fully insured bilingual team.",
        '@Lang.T("Free inspections, factual storm-damage documentation, contractor supplements, roof replacement, repairs, gutters and fascia—with same-business-day response from a fully insured bilingual team.", "Inspecciones gratis, documentación factual de daño por tormenta, suplementos del contratista, reemplazo, reparaciones, canaletas y fascia—con respuesta el mismo día hábil de un equipo bilingüe asegurado.")',
    ),
    (
        "Plan my roof project",
        '@Lang.T("Plan my roof project", "Planear mi proyecto")',
    ),
    (
        "Request an inspection",
        '@Lang.T("Request an inspection", "Pedir una inspección")',
    ),
    (
        "One roofing team. The work that keeps your home protected.",
        '@Lang.T("One roofing team. The work that keeps your home protected.", "Un equipo de techos. El trabajo que protege su hogar.")',
    ),
    (
        "Get a useful price range before you talk to anyone.",
        '@Lang.T("Get a useful price range before you talk to anyone.", "Obtenga un rango útil antes de hablar con nadie.")',
    ),
    (
        "Tell us what is happening above your home.",
        '@Lang.T("Tell us what is happening above your home.", "Cuéntenos qué está pasando arriba de su casa.")',
    ),
]

for a, b in repls:
    if a in t:
        t = t.replace(a, b, 1)
        print("ok", a[:48])
    else:
        print("miss", a[:48])

HOME.write_text(t)
print("done", HOME.stat().st_size)
