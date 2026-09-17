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

## Publicar (Azure App Service)

Cada push a `main` despliega con GitHub Actions (`.github/workflows/deploy-azure.yml`).

1. En Azure Portal → App Service `roofing` → **Get publish profile** → descarga el `.PublishSettings`
2. En GitHub → repo → **Settings → Secrets and variables → Actions** → New repository secret:
   - Name: `AZURE_WEBAPP_PUBLISH_PROFILE`
   - Value: pega el contenido completo del archivo `.PublishSettings`
3. Push a `main` (o **Actions → Deploy Majestic Roofing to Azure → Run workflow**)

App URL: `https://roofing-hzhfdxf8cpazgzet.canadacentral-01.azurewebsites.net`

## Publicar (gratis en Render)

Alternativa: Blueprint en [Render](https://dashboard.render.com/blueprint/new?repo=https://github.com/CarlosCortes641/majestic-roofing) con `render.yaml`. El plan free se duerme sin tráfico.

## Prototipo de referencia

https://majestic-roofing.jrricardo29.chatgpt.site
