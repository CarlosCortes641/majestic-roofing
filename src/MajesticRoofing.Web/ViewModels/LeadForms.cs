using System.ComponentModel.DataAnnotations;

namespace MajesticRoofing.Web.ViewModels;

public sealed class ContactLeadForm
{
    [Required] public string Name { get; set; } = "";
    [Required] public string Phone { get; set; } = "";
    [EmailAddress] public string? Email { get; set; }
    [Required] public string Address { get; set; } = "";
    public string? Service { get; set; }
    public string? Issue { get; set; }
    public string? Details { get; set; }
    public string? Language { get; set; }
    public string? PlannerRange { get; set; }
}
