# Majestic Roofing

Website comercial para Majestic Roofing, Inc., basado en el prototipo ChatGPT Sites.

Stack: **ASP.NET Core 8 MVC + Razor + CSS + JavaScript** — mismo enfoque que `manuela-ruiz-realty` / `safe-project`. El prototipo queda como especificación visual; no es la base de producción.

Por agilidad, **no hay base de datos**. Los leads de formularios viven en memoria (`LeadStore`) y se ven en `/ops`.

## Correr

Requisito: .NET 8 SDK.

```bash
cd /Users/mac/Projects/majestic-roofing
dotnet run --project src/MajesticRoofing.Web --urls http://localhost:5130
```

Abre `http://localhost:5130`.

## Demo 1 (sandbox)

1. Home alineada al prototipo (hero, servicios, planner, tune-up, emergency tarp, galería, FAQ, contacto)
2. Páginas: `/roof-insurance-claim-charlotte-nc`, páginas de emergencia (leak, tree, hail, wind, chimney, open hole), `/roofing-charlotte-nc`, `/roofing-rock-hill-sc`, `/roofing-systems-charlotte-nc`
3. Idioma EN/ES con cookie `mj.lang` (inglés por defecto)
4. Formularios → `LeadStore` in-memory → tablero `/ops`
5. Calculadora de rango de reemplazo en el navegador (misma fórmula del prototipo)

**No activado:** CRM, email transaccional, ni envío real a la aseguradora.

## Prototipo de referencia

https://majestic-roofing.jrricardo29.chatgpt.site
