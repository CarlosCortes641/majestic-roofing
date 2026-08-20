using Microsoft.AspNetCore.Mvc;
using MajesticRoofing.Web.Demo;
using MajesticRoofing.Web.ViewModels;

namespace MajesticRoofing.Web.Controllers;

public class LeadsController : Controller
{
    private readonly LeadStore _leads;

    public LeadsController(LeadStore leads) => _leads = leads;

    [HttpPost("/leads/contact")]
    [ValidateAntiForgeryToken]
    public IActionResult Contact(ContactLeadForm form)
    {
        var back = LocalBack("/#contact");
        if (!ModelState.IsValid)
        {
            TempData["LeadError"] = "contact";
            return Redirect(back);
        }

        _leads.Add(LeadKind.Contact, new Dictionary<string, string?>
        {
            ["name"] = form.Name,
            ["phone"] = form.Phone,
            ["email"] = form.Email,
            ["address"] = form.Address,
            ["service"] = form.Service,
            ["issue"] = form.Issue,
            ["details"] = form.Details,
            ["language"] = form.Language,
            ["plannerRange"] = form.PlannerRange
        });

        TempData["LeadOk"] = "contact";
        return Redirect(back);
    }

    private string LocalBack(string fallback)
    {
        var referer = Request.Headers.Referer.ToString();
        if (string.IsNullOrWhiteSpace(referer))
        {
            return fallback;
        }

        if (!Uri.TryCreate(referer, UriKind.Absolute, out var uri))
        {
            return fallback;
        }

        var current = $"{Request.Scheme}://{Request.Host}";
        if (!referer.StartsWith(current, StringComparison.OrdinalIgnoreCase))
        {
            return fallback;
        }

        return uri.PathAndQuery;
    }
}
