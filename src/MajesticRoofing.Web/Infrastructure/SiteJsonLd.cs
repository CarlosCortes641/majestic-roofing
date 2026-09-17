using System.Text.Json;

namespace MajesticRoofing.Web.Infrastructure;

public static class SiteJsonLd
{
    private static readonly JsonSerializerOptions Options = new()
    {
        PropertyNamingPolicy = null,
        WriteIndented = false
    };

    public static string Business(string siteUrl)
    {
        var root = siteUrl.TrimEnd('/');
        var businessId = $"{root}/#business";
        var doc = new Dictionary<string, object?>
        {
            ["@context"] = "https://schema.org",
            ["@graph"] = new object[]
            {
                new Dictionary<string, object?>
                {
                    ["@type"] = new[] { "RoofingContractor", "LocalBusiness", "Organization" },
                    ["@id"] = businessId,
                    ["name"] = SiteInfo.ShortName,
                    ["legalName"] = SiteInfo.Name,
                    ["url"] = root + "/",
                    ["telephone"] = SiteInfo.PhoneTel,
                    ["email"] = SiteInfo.Email,
                    ["foundingDate"] = SiteInfo.Founded,
                    ["priceRange"] = "$$",
                    ["currenciesAccepted"] = "USD",
                    ["image"] = root + "/img/projects/roof-project-11.jpeg",
                    ["logo"] = root + "/favicon.svg",
                    ["sameAs"] = new[] { SiteInfo.Instagram },
                    ["description"] =
                        "Bilingual roof insurance claim documentation, free storm inspections, roof replacement, repairs, emergency tarping, gutters and fascia in Charlotte, NC and Rock Hill, SC.",
                    ["availableLanguage"] = new object[]
                    {
                        new Dictionary<string, object?> { ["@type"] = "Language", ["name"] = "English" },
                        new Dictionary<string, object?> { ["@type"] = "Language", ["name"] = "Spanish" }
                    },
                    ["address"] = new Dictionary<string, object?>
                    {
                        ["@type"] = "PostalAddress",
                        ["streetAddress"] = "5122 Belstone Lane",
                        ["addressLocality"] = "Charlotte",
                        ["addressRegion"] = "NC",
                        ["postalCode"] = "28215",
                        ["addressCountry"] = "US"
                    },
                    ["geo"] = new Dictionary<string, object?>
                    {
                        ["@type"] = "GeoCoordinates",
                        ["latitude"] = 35.2271,
                        ["longitude"] = -80.8431
                    },
                    ["areaServed"] = new object[]
                    {
                        new Dictionary<string, object?>
                        {
                            ["@type"] = "City",
                            ["name"] = "Charlotte",
                            ["containedInPlace"] = new Dictionary<string, object?>
                            {
                                ["@type"] = "State",
                                ["name"] = "North Carolina"
                            }
                        },
                        new Dictionary<string, object?>
                        {
                            ["@type"] = "City",
                            ["name"] = "Rock Hill",
                            ["containedInPlace"] = new Dictionary<string, object?>
                            {
                                ["@type"] = "State",
                                ["name"] = "South Carolina"
                            }
                        },
                        new Dictionary<string, object?>
                        {
                            ["@type"] = "GeoCircle",
                            ["name"] = "Approximately 90 minutes from Charlotte or Rock Hill",
                            ["geoMidpoint"] = new Dictionary<string, object?>
                            {
                                ["@type"] = "GeoCoordinates",
                                ["latitude"] = 35.2271,
                                ["longitude"] = -80.8431
                            },
                            ["geoRadius"] = "144841"
                        }
                    },
                    ["knowsAbout"] = new[]
                    {
                        "Roof insurance claim documentation",
                        "Storm damage roof inspection",
                        "Roof replacement",
                        "Roof repair",
                        "Emergency roof tarp",
                        "Hail damage",
                        "Wind damage",
                        "Gutters and fascia"
                    },
                    ["hasOfferCatalog"] = new Dictionary<string, object?>
                    {
                        ["@type"] = "OfferCatalog",
                        ["name"] = "Majestic Roofing services",
                        ["itemListElement"] = new object[]
                        {
                            Offer("Roof inspection", root + "/"),
                            Offer("Roof replacement", root + "/roofing-systems-charlotte-nc"),
                            Offer("Storm / insurance documentation", root + "/roof-insurance-claim-charlotte-nc"),
                            Offer("Emergency tarp", root + "/active-roof-leak-repair-charlotte-nc"),
                            Offer("Charlotte roofing", root + "/roofing-charlotte-nc"),
                            Offer("Rock Hill roofing", root + "/roofing-rock-hill-sc")
                        }
                    },
                    ["contactPoint"] = new Dictionary<string, object?>
                    {
                        ["@type"] = "ContactPoint",
                        ["telephone"] = SiteInfo.PhoneTel,
                        ["contactType"] = "customer service",
                        ["areaServed"] = new[] { "US-NC", "US-SC" },
                        ["availableLanguage"] = new[] { "English", "Spanish" }
                    }
                },
                new Dictionary<string, object?>
                {
                    ["@type"] = "WebSite",
                    ["@id"] = $"{root}/#website",
                    ["url"] = root + "/",
                    ["name"] = SiteInfo.ShortName,
                    ["publisher"] = new Dictionary<string, object?> { ["@id"] = businessId },
                    ["inLanguage"] = new[] { "en", "es" }
                }
            }
        };

        return JsonSerializer.Serialize(doc, Options);
    }

    private static Dictionary<string, object?> Offer(string name, string url) => new()
    {
        ["@type"] = "Offer",
        ["itemOffered"] = new Dictionary<string, object?>
        {
            ["@type"] = "Service",
            ["name"] = name,
            ["url"] = url
        }
    };
}
