namespace MajesticRoofing.Web.Infrastructure;

public sealed class SiteLanguage
{
    public const string CookieName = "mj.lang";

    public SiteLanguage(IHttpContextAccessor accessor)
    {
        var value = accessor.HttpContext?.Request.Cookies[CookieName];
        IsSpanish = string.Equals(value, "es", StringComparison.OrdinalIgnoreCase);
    }

    public bool IsSpanish { get; }
    public string HtmlLang => IsSpanish ? "es" : "en";
    public string OtherCode => IsSpanish ? "en" : "es";
    public string ToggleLabel => IsSpanish ? "EN" : "ES";

    public string T(string english, string? spanish = null)
    {
        if (!IsSpanish)
        {
            return english;
        }

        if (!string.IsNullOrEmpty(spanish))
        {
            return spanish;
        }

        return CopyCatalog.Es.TryGetValue(english, out var mapped) ? mapped : english;
    }
}
