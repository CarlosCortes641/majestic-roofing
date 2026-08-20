using System.Collections.Concurrent;

namespace MajesticRoofing.Web.Demo;

public enum LeadKind
{
    Contact
}

public sealed class LeadRecord
{
    public string Id { get; init; } = "";
    public LeadKind Kind { get; init; }
    public DateTimeOffset CreatedAt { get; init; }
    public string Name { get; init; } = "";
    public string Email { get; init; } = "";
    public string Phone { get; init; } = "";
    public string Language { get; init; } = "";
    public string Summary { get; init; } = "";
    public Dictionary<string, string> Fields { get; init; } = new();
}

public sealed class LeadStore
{
    private readonly ConcurrentDictionary<string, LeadRecord> _leads = new();

    public LeadRecord Add(LeadKind kind, IDictionary<string, string?> fields)
    {
        var clean = fields
            .Where(kv => !string.IsNullOrWhiteSpace(kv.Value))
            .ToDictionary(kv => kv.Key, kv => kv.Value!.Trim(), StringComparer.OrdinalIgnoreCase);

        clean.TryGetValue("name", out var name);
        clean.TryGetValue("email", out var email);
        clean.TryGetValue("phone", out var phone);
        clean.TryGetValue("language", out var language);

        var id = $"MJ-{DateTime.UtcNow:yyyyMMdd}-{_leads.Count + 1:000}";
        var summary =
            $"{clean.GetValueOrDefault("service")} · {clean.GetValueOrDefault("issue")} · {clean.GetValueOrDefault("address")}";

        var lead = new LeadRecord
        {
            Id = id,
            Kind = kind,
            CreatedAt = DateTimeOffset.UtcNow,
            Name = name ?? "",
            Email = email ?? "",
            Phone = phone ?? "",
            Language = language ?? "",
            Summary = summary.Trim(' ', '·'),
            Fields = clean
        };

        _leads[id] = lead;
        return lead;
    }

    public IReadOnlyList<LeadRecord> All() =>
        _leads.Values.OrderByDescending(l => l.CreatedAt).ToList();
}
