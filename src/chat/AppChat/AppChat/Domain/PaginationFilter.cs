using System.Text.Json.Serialization;

namespace AppChat.Domain
{
    public class PaginationFilter
    {
        [JsonPropertyName("page")] public int Page { get; set; }
        [JsonPropertyName("per_page")] public int PerPage { get; set; }
    }
}