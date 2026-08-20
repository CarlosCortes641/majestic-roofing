using System.Globalization;
using MajesticRoofing.Web.Demo;
using MajesticRoofing.Web.Infrastructure;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddHttpContextAccessor();
builder.Services.AddControllersWithViews();
builder.Services.AddSingleton<LeadStore>();
builder.Services.AddScoped<SiteLanguage>();

var app = builder.Build();

if (!app.Environment.IsDevelopment())
{
    app.UseExceptionHandler("/Home/Error");
    app.UseHsts();
}

app.UseStaticFiles();
app.Use(async (context, next) =>
{
    var code = string.Equals(context.Request.Cookies[SiteLanguage.CookieName], "es", StringComparison.OrdinalIgnoreCase)
        ? "es-US"
        : "en-US";
    var culture = CultureInfo.GetCultureInfo(code);
    CultureInfo.CurrentCulture = culture;
    CultureInfo.CurrentUICulture = culture;
    await next();
});
app.UseRouting();
app.UseAuthorization();

app.MapControllerRoute(
    name: "default",
    pattern: "{controller=Home}/{action=Index}/{id?}");

app.Run();
