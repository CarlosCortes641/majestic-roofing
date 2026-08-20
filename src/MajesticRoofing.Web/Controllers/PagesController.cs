using Microsoft.AspNetCore.Mvc;

namespace MajesticRoofing.Web.Controllers;

public class PagesController : Controller
{
    [HttpGet("/roof-insurance-claim-charlotte-nc")]
    public IActionResult StormClaim() => View("roof_insurance_claim_charlotte_nc");

    [HttpGet("/active-roof-leak-repair-charlotte-nc")]
    public IActionResult ActiveLeak() => View("active_roof_leak_repair_charlotte_nc");

    [HttpGet("/chimney-flashing-leak-repair-charlotte-nc")]
    public IActionResult ChimneyFlashing() => View("chimney_flashing_leak_repair_charlotte_nc");

    [HttpGet("/hail-damage-roof-inspection-charlotte-nc")]
    public IActionResult HailDamage() => View("hail_damage_roof_inspection_charlotte_nc");

    [HttpGet("/open-roof-hole-decking-repair-charlotte-nc")]
    public IActionResult OpenHole() => View("open_roof_hole_decking_repair_charlotte_nc");

    [HttpGet("/tree-roof-damage-charlotte-nc")]
    public IActionResult TreeDamage() => View("tree_roof_damage_charlotte_nc");

    [HttpGet("/wind-missing-shingles-repair-charlotte-nc")]
    public IActionResult WindShingles() => View("wind_missing_shingles_repair_charlotte_nc");

    [HttpGet("/roofing-charlotte-nc")]
    public IActionResult Charlotte() => View("roofing_charlotte_nc");

    [HttpGet("/roofing-rock-hill-sc")]
    public IActionResult RockHill() => View("roofing_rock_hill_sc");

    [HttpGet("/roofing-systems-charlotte-nc")]
    public IActionResult Systems() => View("roofing_systems_charlotte_nc");
}
